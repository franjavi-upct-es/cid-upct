#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
  set -a
  . "${SCRIPT_DIR}/.env"
  set +a
fi

: "${HDFS_MOUNT_USER:=luser}"
# Debe coincidir con nfs.export.point en hdfs-site.xml.
: "${HDFS_NFS_EXPORT:=/user/${HDFS_MOUNT_USER}}"
# Para estabilidad: evita "soft,timeo=2" (puede provocar EIO en copias largas).
: "${HDFS_NFS_MOUNT_OPTS:=nfsvers=3,proto=tcp,mountproto=tcp,port=2049,mountport=4242,nolock,noacl,hard,timeo=150,retrans=5}"

if [ "$#" -ne 1 ]; then
  echo "Uso: $(basename "$0") <mount|umount>"
  echo "Este script monta o desmonta siempre en \$HOME/hdfs."
  exit 1
fi

ACTION="$1"
if [ "${ACTION}" != "mount" ] && [ "${ACTION}" != "umount" ]; then
  echo "Accion invalida: ${ACTION}"
  echo "Uso: $(basename "$0") <mount|umount>"
  exit 1
fi

TARGET_USER="${SUDO_USER:-$(id -un)}"
TARGET_HOME="$(getent passwd "${TARGET_USER}" | cut -d: -f6)"

if [ -z "${TARGET_HOME}" ]; then
  echo "No se pudo resolver el home para el usuario: ${TARGET_USER}"
  exit 1
fi

MOUNT_DIR="${TARGET_HOME}/hdfs"
EXPORT_PATH="${HDFS_NFS_EXPORT}"

if [ "$(id -u)" -eq 0 ]; then
  MOUNT_CMD=(mount)
  UMOUNT_CMD=(umount)
else
  if ! command -v sudo >/dev/null 2>&1; then
    echo "Este script necesita root o sudo para montar/desmontar NFS."
    exit 1
  fi
  MOUNT_CMD=(sudo mount)
  UMOUNT_CMD=(sudo umount)
fi

if [ "${ACTION}" = "mount" ]; then
  mkdir -p "$MOUNT_DIR"

  echo "Montando HDFS (vía NFS) en: $MOUNT_DIR"
  echo "Export: ${EXPORT_PATH}"
  echo "Opciones NFS: ${HDFS_NFS_MOUNT_OPTS}"
  echo "Necesitas nfs-common (Debian/Ubuntu) o nfs-utils (Fedora/RHEL)."
  echo

  "${MOUNT_CMD[@]}" -t nfs -o "${HDFS_NFS_MOUNT_OPTS}" 127.0.0.1:"${EXPORT_PATH}" "$MOUNT_DIR"

  echo
  echo "OK. Prueba: ls -la $MOUNT_DIR"
  echo "Para desmontar: $(basename "$0") umount"
  exit 0
fi

echo "Desmontando HDFS en: $MOUNT_DIR"
if mountpoint -q "${MOUNT_DIR}" 2>/dev/null; then
  "${UMOUNT_CMD[@]}" "${MOUNT_DIR}"
  echo "OK. Desmontado: ${MOUNT_DIR}"
else
  echo "Nada que desmontar: ${MOUNT_DIR} no esta montado."
fi
