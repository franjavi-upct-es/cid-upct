#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
  set -a
  . "${SCRIPT_DIR}/.env"
  set +a
fi

: "${HDFS_MOUNT_USER:=luser}"

if [ "$#" -gt 1 ]; then
  echo "Uso: $(basename "$0") [test_file]"
  echo "Este script no acepta carpeta de montaje; usa siempre \$HOME/hdfs."
  exit 1
fi

if [ "$(id -u)" -eq 0 ]; then
  echo "No ejecutes $(basename "$0") con sudo ni como root."
  echo "Ejecutalo como usuario normal: ./$(basename "$0") [test_file]"
  exit 1
fi

TARGET_USER="${SUDO_USER:-$(id -un)}"
TARGET_HOME="$(getent passwd "${TARGET_USER}" | cut -d: -f6)"
if [ -z "${TARGET_HOME}" ]; then
  echo "No se pudo resolver el home para el usuario: ${TARGET_USER}"
  exit 1
fi

MOUNT_DIR="${TARGET_HOME}/hdfs"
TEST_FILE="${1:-hello-$(date +%Y%m%d%H%M%S)-$$.txt}"
TEST_CONTENT="hello hdfs $(date -Iseconds)"
TEST_PATH="${MOUNT_DIR}/${TEST_FILE}"
HDFS_PATH="/user/${HDFS_MOUNT_USER}/${TEST_FILE}"
MOUNT_SCRIPT="${SCRIPT_DIR}/mount-hdfs.sh"

is_mounted() {
  mountpoint -q "$1" 2>/dev/null
}

run_with_timeout() {
  if command -v timeout >/dev/null 2>&1; then
    timeout 3s "$@"
  else
    "$@"
  fi
}

mount_with_retry() {
  local tries=10
  local delay=3
  local attempt=1
  while [ "${attempt}" -le "${tries}" ]; do
    if run_mount; then
      return 0
    fi
    echo "==> Mount failed (attempt ${attempt}/${tries}), retrying in ${delay}s..."
    sleep "${delay}"
    attempt=$((attempt + 1))
  done
  return 1
}

run_mount() {
  if [ "$(id -u)" -eq 0 ]; then
    "${MOUNT_SCRIPT}" mount
  else
    sudo "${MOUNT_SCRIPT}" mount
  fi
}

run_umount() {
  if [ "$(id -u)" -eq 0 ]; then
    "${MOUNT_SCRIPT}" umount
  else
    sudo "${MOUNT_SCRIPT}" umount
  fi
}

check_mount_write() {
  local dir="$1"
  local probe="${dir}/.hdfs-probe-$$"
  if echo "probe" > "${probe}" 2>/dev/null; then
    cat "${probe}" >/dev/null 2>&1 || true
    rm -f "${probe}" >/dev/null 2>&1 || true
    return 0
  fi
  rm -f "${probe}" >/dev/null 2>&1 || true
  return 1
}

try_unmount() {
  local dir="$1"
  if run_umount; then
    return 0
  fi
  echo "==> Regular umount failed, trying lazy umount"
  if [ "$(id -u)" -eq 0 ]; then
    umount -l "${dir}"
  else
    sudo umount -l "${dir}"
  fi
}

ensure_mount() {
  local dir="$1"
  if is_mounted "${dir}"; then
    if check_mount_write "${dir}"; then
      echo "==> ${dir} is already mounted, skipping mount"
    else
      echo "==> ${dir} is mounted but not writable/responding, remounting"
      if ! try_unmount "${dir}"; then
        echo "==> Failed to unmount ${dir}. Close any processes using it and retry."
        exit 1
      fi
      mount_with_retry
    fi
  else
    mount_with_retry
  fi
}

recover_lease() {
  if docker compose exec workbench bash -lc "hdfs dfs -test -e ${HDFS_PATH}"; then
    docker compose exec workbench bash -lc "hdfs debug recoverLease -path ${HDFS_PATH} -retries 5" || true
  fi
}

wait_for_port() {
  local host="$1" port="$2" name="${3:-$host:$port}"
  local tries=60
  echo "==> Waiting for ${name}..."
  for _ in $(seq 1 "${tries}"); do
    if command -v nc >/dev/null 2>&1; then
      if nc -z "${host}" "${port}" >/dev/null 2>&1; then
        echo "==> ${name} is ready"
        return 0
      fi
    else
      if (echo >/dev/tcp/"${host}"/"${port}") >/dev/null 2>&1; then
        echo "==> ${name} is ready"
        return 0
      fi
    fi
    sleep 1
  done
  echo "==> Timeout waiting for ${name}"
  return 1
}

echo "==> Mounting HDFS at ${MOUNT_DIR}"
ensure_mount "${MOUNT_DIR}"

if [ -e "${TEST_PATH}" ]; then
  if ! run_with_timeout cat "${TEST_PATH}" >/dev/null 2>&1; then
    echo "==> ${TEST_PATH} looks stale, remounting"
    try_unmount "${MOUNT_DIR}"
    run_mount
  fi
fi

echo "==> Writing test file"
if [ ! -w "${MOUNT_DIR}" ]; then
  echo "==> ${MOUNT_DIR} is not writable"
  exit 1
fi
if [ -e "${TEST_PATH}" ]; then
  rm -f "${TEST_PATH}" || true
fi
echo "${TEST_CONTENT}" > "${TEST_PATH}"
ls -la "${MOUNT_DIR}"

echo "==> Verifying via HDFS client"
recover_lease
docker compose exec workbench bash -lc "hdfs dfs -ls /user/${HDFS_MOUNT_USER} && hdfs dfs -cat /user/${HDFS_MOUNT_USER}/${TEST_FILE}"

echo "==> Unmounting ${MOUNT_DIR}"
if is_mounted "${MOUNT_DIR}"; then
  try_unmount "${MOUNT_DIR}"
else
  echo "==> ${MOUNT_DIR} is not mounted, skipping umount"
fi

echo "==> Restarting cluster (without removing volumes)"
docker compose down
docker compose up -d

wait_for_port 127.0.0.1 2049 "NFS (2049)"
wait_for_port 127.0.0.1 4242 "mountd (4242)"

echo "==> Remounting and rechecking"
ensure_mount "${MOUNT_DIR}"
cat "${TEST_PATH}"

echo "==> Done."
