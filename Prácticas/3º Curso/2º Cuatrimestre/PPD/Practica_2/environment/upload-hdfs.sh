#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
  set -a
  . "${SCRIPT_DIR}/.env"
  set +a
fi

: "${HDFS_MOUNT_USER:=luser}"

usage() {
  echo "Uso: $(basename "$0") <ruta_local> [destino_hdfs]"
  echo
  echo "Ejemplos:"
  echo "  ./$(basename "$0") ./libros"
  echo "  ./$(basename "$0") ./libros /user/${HDFS_MOUNT_USER}/datasets"
  echo "  ./$(basename "$0") ./libros datasets"
  echo
  echo "Si destino_hdfs es relativo, se toma respecto a /user/${HDFS_MOUNT_USER}."
}

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  usage
  exit 1
fi

SRC_PATH="$1"
if [ ! -e "${SRC_PATH}" ]; then
  echo "No existe la ruta local: ${SRC_PATH}"
  exit 1
fi

SRC_BASE="$(basename "${SRC_PATH%/}")"
HDFS_USER_HOME="/user/${HDFS_MOUNT_USER}"
HDFS_DEST_DIR="${2:-${HDFS_USER_HOME}}"
if [[ "${HDFS_DEST_DIR}" != /* ]]; then
  HDFS_DEST_DIR="${HDFS_USER_HOME}/${HDFS_DEST_DIR}"
fi

COMPOSE=(docker compose -f "${SCRIPT_DIR}/docker-compose.yml")
WORKBENCH_SERVICE="workbench"
TMP_CONTAINER_DIR="/tmp/upload-hdfs-${SRC_BASE}-$$"
TMP_CONTAINER_SRC="${TMP_CONTAINER_DIR}/${SRC_BASE}"

cleanup() {
  "${COMPOSE[@]}" exec -T "${WORKBENCH_SERVICE}" rm -rf "${TMP_CONTAINER_DIR}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "Copiando al contenedor ${WORKBENCH_SERVICE}: ${SRC_PATH}"
"${COMPOSE[@]}" exec -T "${WORKBENCH_SERVICE}" mkdir -p "${TMP_CONTAINER_DIR}"
"${COMPOSE[@]}" cp "${SRC_PATH}" "${WORKBENCH_SERVICE}:${TMP_CONTAINER_DIR}/"

echo "Subiendo a HDFS: ${HDFS_DEST_DIR}/${SRC_BASE}"
"${COMPOSE[@]}" exec -T "${WORKBENCH_SERVICE}" hdfs dfs -mkdir -p "${HDFS_DEST_DIR}"
"${COMPOSE[@]}" exec -T "${WORKBENCH_SERVICE}" hdfs dfs -rm -r -f "${HDFS_DEST_DIR}/${SRC_BASE}" >/dev/null 2>&1 || true
"${COMPOSE[@]}" exec -T "${WORKBENCH_SERVICE}" hdfs dfs -put -f "${TMP_CONTAINER_SRC}" "${HDFS_DEST_DIR}/"
"${COMPOSE[@]}" exec -T "${WORKBENCH_SERVICE}" hdfs dfs -ls "${HDFS_DEST_DIR}/${SRC_BASE}"

echo "OK. Carga completada en HDFS."
