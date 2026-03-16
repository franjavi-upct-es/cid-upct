#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
  set -a
  . "${SCRIPT_DIR}/.env"
  set +a
fi

TARGET_PATH="${1:-/}"
RECOVER_RETRIES="${2:-5}"
NAMENODE_SERVICE="${HDFS_RECOVERY_NAMENODE_SERVICE:-namenode}"
HDFS_SUPERUSER="${HDFS_RECOVERY_SUPERUSER:-hdadmin}"
ALLOW_EMACS_LOCK_CLEANUP="${HDFS_RECOVERY_REMOVE_EMACS_LOCKS:-1}"
COMPOSE=(docker compose -f "${SCRIPT_DIR}/docker-compose.yml")

usage() {
  echo "Uso: $(basename "$0") [hdfs_path] [reintentos]"
  echo
  echo "Ejemplos:"
  echo "  ./$(basename "$0")"
  echo "  ./$(basename "$0") /user/luser"
  echo "  ./$(basename "$0") /user/luser/libros 8"
}

if [ "${TARGET_PATH}" = "-h" ] || [ "${TARGET_PATH}" = "--help" ]; then
  usage
  exit 0
fi

if ! [[ "${RECOVER_RETRIES}" =~ ^[0-9]+$ ]] || [ "${RECOVER_RETRIES}" -lt 1 ]; then
  echo "Valor invalido de reintentos: ${RECOVER_RETRIES}"
  usage
  exit 2
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "No se encontro el comando docker."
  exit 2
fi

list_open_files() {
  local list_cmd
  printf -v list_cmd "hdfs dfsadmin -listOpenFiles -path %q" "${TARGET_PATH}"

  "${COMPOSE[@]}" exec -T "${NAMENODE_SERVICE}" su - "${HDFS_SUPERUSER}" -c "${list_cmd}" \
    | awk -F'\t' '
      NR > 1 {
        path = $NF
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", path)
        if (path ~ /^\//) print path
      }
    '
}

get_open_files_or_die() {
  local raw_output
  if ! raw_output="$(list_open_files 2>&1)"; then
    echo "${raw_output}" >&2
    echo "No se pudo listar ficheros abiertos. Verifica Docker Compose y permisos de acceso al daemon." >&2
    exit 2
  fi
  mapfile -t OPEN_FILES_BUFFER < <(printf '%s\n' "${raw_output}" | sed '/^$/d')
}

run_recover_lease() {
  local path="$1"
  local recover_cmd
  printf -v recover_cmd "hdfs debug recoverLease -path %q -retries %q" "${path}" "${RECOVER_RETRIES}"

  "${COMPOSE[@]}" exec -T "${NAMENODE_SERVICE}" su - "${HDFS_SUPERUSER}" -c "${recover_cmd}"
}

remove_hdfs_path() {
  local path="$1"
  local rm_cmd
  printf -v rm_cmd "hdfs dfs -rm -skipTrash %q" "${path}"
  "${COMPOSE[@]}" exec -T "${NAMENODE_SERVICE}" su - "${HDFS_SUPERUSER}" -c "${rm_cmd}"
}

is_emacs_lock_file() {
  local path="$1"
  local base="${path##*/}"
  [[ "${base}" == \#*\# ]]
}

echo "Buscando ficheros abiertos bajo: ${TARGET_PATH}"
OPEN_FILES_BUFFER=()
get_open_files_or_die
open_files=("${OPEN_FILES_BUFFER[@]}")

if [ "${#open_files[@]}" -eq 0 ]; then
  echo "No hay ficheros abiertos pendientes."
  exit 0
fi

echo "Se detectaron ${#open_files[@]} fichero(s) abierto(s)."
recovered=0
failed=0

for path in "${open_files[@]}"; do
  echo
  echo "Recuperando lease: ${path}"
  if output="$(run_recover_lease "${path}" 2>&1)"; then
    echo "${output}"
    if printf '%s\n' "${output}" | grep -Eqi "recoverLease SUCCEEDED|recoverLease returned true"; then
      recovered=$((recovered + 1))
      continue
    fi
    if printf '%s\n' "${output}" | grep -qi "recoverLease returned false"; then
      failed=$((failed + 1))
      continue
    fi
    # Comportamiento inesperado: se revalida en el resumen final.
    continue
  fi

  echo "${output}"
  if printf '%s\n' "${output}" | grep -q "URISyntaxException" \
    && is_emacs_lock_file "${path}" \
    && [ "${ALLOW_EMACS_LOCK_CLEANUP}" = "1" ]; then
    echo "Fallback: eliminando lock temporal de Emacs con caracteres no URI: ${path}"
    if rm_output="$(remove_hdfs_path "${path}" 2>&1)"; then
      echo "${rm_output}"
      recovered=$((recovered + 1))
      continue
    fi
    echo "${rm_output}"
  fi
  failed=$((failed + 1))
done

echo
echo "Revalidando leases abiertas..."
OPEN_FILES_BUFFER=()
get_open_files_or_die
remaining_files=("${OPEN_FILES_BUFFER[@]}")

if [ "${#remaining_files[@]}" -eq 0 ]; then
  echo "OK. No quedan ficheros abiertos."
  echo "Resumen: detectados=${#open_files[@]}, recuperados=${recovered}, fallidos=${failed}"
  exit 0
fi

echo "Quedan ${#remaining_files[@]} fichero(s) abierto(s):"
printf ' - %s\n' "${remaining_files[@]}"
echo "Resumen: detectados=${#open_files[@]}, recuperados=${recovered}, fallidos=${failed}"
exit 1
