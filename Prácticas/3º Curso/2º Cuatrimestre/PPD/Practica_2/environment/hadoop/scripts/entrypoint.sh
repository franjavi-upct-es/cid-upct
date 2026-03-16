#!/usr/bin/env bash
set -euo pipefail

: "${HADOOP_HOME:=/opt/hadoop}"
: "${HADOOP_CONF_DIR:=$HADOOP_HOME/etc/hadoop}"
: "${ROLE:=workbench}"
: "${CLUSTER_NAME:=hadoop-lab}"
: "${HOST_UID:=1000}"
: "${HOST_GID:=1000}"
: "${HDFS_MOUNT_USER:=luser}"

export HADOOP_HOME HADOOP_CONF_DIR

log() { echo "[$(date -Iseconds)] $*"; }

ensure_host_group() {
  : "${HOST_GID:=1000}"
  if ! getent group hostgrp >/dev/null; then
    groupadd -g "${HOST_GID}" hostgrp 2>/dev/null || true
  else
    current_gid="$(getent group hostgrp | cut -d: -f3)"
    if [ "${current_gid}" != "${HOST_GID}" ]; then
      groupmod -g "${HOST_GID}" hostgrp 2>/dev/null || true
    fi
  fi
}

ensure_user_in_host_group() {
  local user="$1"
  ensure_host_group
  if id "${user}" >/dev/null 2>&1; then
    usermod -a -G hostgrp "${user}" 2>/dev/null || true
  fi
}

fix_user_ids() {
  : "${HOST_UID:=1000}"
  : "${HOST_GID:=1000}"
  : "${HDFS_MOUNT_USER:=luser}"

  local existing_user existing_gid new_uid

  ensure_host_group

  # Libera HOST_UID si ya lo tiene otro usuario (p. ej., hdadmin).
  existing_user="$(getent passwd "${HOST_UID}" | cut -d: -f1 || true)"
  if [ -n "${existing_user}" ] && [ "${existing_user}" != "${HDFS_MOUNT_USER}" ]; then
    existing_gid="$(id -g "${existing_user}" 2>/dev/null || echo "${HOST_GID}")"
    new_uid="$(getent passwd | awk -F: 'BEGIN{max=2000} {if($3>=max)max=$3} END{print max+1}')"
    usermod -u "${new_uid}" "${existing_user}" 2>/dev/null || true
    if [ -d "/home/${existing_user}" ]; then
      chown -R "${new_uid}:${existing_gid}" "/home/${existing_user}" 2>/dev/null || true
    fi
  fi

  # Crea o ajusta el usuario del montaje NFS (por defecto: luser).
  if id "${HDFS_MOUNT_USER}" >/dev/null 2>&1; then
    usermod -u "${HOST_UID}" "${HDFS_MOUNT_USER}" 2>/dev/null || true
    usermod -g "${HOST_GID}" "${HDFS_MOUNT_USER}" 2>/dev/null || true
  else
    useradd -m -u "${HOST_UID}" -g "${HOST_GID}" -s /bin/bash "${HDFS_MOUNT_USER}"
  fi

  ensure_user_in_host_group "${HDFS_MOUNT_USER}"

  # Permisos mínimos para evitar fallos de logs en nfs3.
  mkdir -p /opt/hadoop/logs
  chown -R "${HOST_UID}:${HOST_GID}" "/home/${HDFS_MOUNT_USER}" /opt/hadoop/logs 2>/dev/null || true
  chmod 775 /opt/hadoop/logs 2>/dev/null || true
}

ensure_luser_uid() {
  # La doc del NFS Gateway exige que el UID/GID del cliente coincida con el del gateway
  if id "$HDFS_MOUNT_USER" >/dev/null 2>&1; then
    current_uid="$(id -u "$HDFS_MOUNT_USER")"
    current_gid="$(id -g "$HDFS_MOUNT_USER")"
    if [ "$current_gid" != "$HOST_GID" ]; then
      if getent group "$HOST_GID" >/dev/null; then
        groupmod -g "$((HOST_GID+1))" "$HDFS_MOUNT_USER" 2>/dev/null || true
      fi
      groupmod -g "$HOST_GID" "$HDFS_MOUNT_USER" 2>/dev/null || true
    fi
    if [ "$current_uid" != "$HOST_UID" ]; then
      usermod -u "$HOST_UID" "$HDFS_MOUNT_USER" 2>/dev/null || true
    fi
  else
    groupadd -g "$HOST_GID" "$HDFS_MOUNT_USER" 2>/dev/null || true
    useradd -m -u "$HOST_UID" -g "$HOST_GID" -s /bin/bash "$HDFS_MOUNT_USER"
  fi

  ensure_user_in_host_group "${HDFS_MOUNT_USER}"
}

wait_for_port() {
  local host="$1" port="$2" name="${3:-$host:$port}"
  log "Esperando a $name..."
  for _ in $(seq 1 120); do
    if nc -z "$host" "$port" >/dev/null 2>&1; then
      log "$name OK"
      return 0
    fi
    sleep 1
  done
  log "Timeout esperando a $name"
  return 1
}

init_hdfs_dirs() {
  log "Inicializando directorios HDFS (equivalente a Apartado 3.1) "
  local USER="${HDFS_MOUNT_USER:-luser}"
  su - hdadmin -c "hdfs dfs -test -d /user/hdadmin || hdfs dfs -mkdir -p /user/hdadmin"
  su - hdadmin -c "hdfs dfs -test -d /user/${USER} || hdfs dfs -mkdir -p /user/${USER}"
  su - hdadmin -c "hdfs dfs -chown ${USER}:supergroup /user/${USER} || true"
  # Entorno docente: lectura global por defecto sin abrir escritura.
  su - hdadmin -c "hdfs dfs -chmod 755 /user/${USER} || true"
  # Reaplica visibilidad sobre contenido existente al reiniciar el cluster.
  su - hdadmin -c "hdfs dfs -chmod -R a+rX /user/${USER} || true"
  # Intenta que nuevas entradas hereden permisos de lectura global (si ACL esta habilitado).
  su - hdadmin -c "hdfs dfs -setfacl -m default:user::rwx,default:group::r-x,default:other::r-x /user/${USER}" || true

  su - hdadmin -c "hdfs dfs -test -d /tmp/hadoop-yarn/staging || hdfs dfs -mkdir -p /tmp/hadoop-yarn/staging"
  su - hdadmin -c "hdfs dfs -chmod -R 1777 /tmp || true"

  # Para JobHistory
  su - hdadmin -c "hdfs dfs -test -d /mr-history/done || hdfs dfs -mkdir -p /mr-history/done"
  su - hdadmin -c "hdfs dfs -test -d /mr-history/tmp || hdfs dfs -mkdir -p /mr-history/tmp"
  su - hdadmin -c "hdfs dfs -chmod -R 1777 /mr-history || true"
}

case "$ROLE" in
  namenode)
    ensure_luser_uid
    mkdir -p /data/hdfs/namenode /data/tmp
    chown -R hdadmin:hadoop /data/hdfs/namenode /data/tmp

    if [ ! -d /data/hdfs/namenode/current ]; then
      log "Formateando NameNode (primera vez)..."
      su - hdadmin -c "hdfs namenode -format -nonInteractive ${CLUSTER_NAME}"
    fi

    log "Arrancando NameNode y ResourceManager..."
    su - hdadmin -c "hdfs --daemon start namenode"
    su - hdadmin -c "yarn --daemon start resourcemanager"

    # Espera a que salga de safe mode
    log "Esperando salida del safe mode..."
    su - hdadmin -c "hdfs dfsadmin -safemode wait" || true

    init_hdfs_dirs

    log "Listo. Interfaces: HDFS http://localhost:9870  |  YARN http://localhost:8088"
    tail -f /dev/null
    ;;
  datanode)
    ensure_luser_uid
    mkdir -p /data/hdfs/datanode /data/yarn/local /data/yarn/log
    chown -R hdadmin:hadoop /data/hdfs/datanode /data/yarn/local /data/yarn/log

    wait_for_port namenode 9000 "RPC del NameNode"
    wait_for_port resourcemanager 8032 "RPC del ResourceManager"

    log "Arrancando DataNode y NodeManager..."
    su - hdadmin -c "hdfs --daemon start datanode"
    su - hdadmin -c "yarn --daemon start nodemanager"

    tail -f /dev/null
    ;;
  historyserver)
    wait_for_port namenode 9000 "RPC del NameNode"
    wait_for_port resourcemanager 8032 "RPC del ResourceManager"

    log "Arrancando JobHistoryServer (historial de trabajos)..."
    su - hdadmin -c "mapred --daemon start historyserver"
    tail -f /dev/null
    ;;
  nfsgateway)
    fix_user_ids
    wait_for_port namenode 9000 "RPC del NameNode"

    rm -rf /tmp/.hdfs-nfs
    install -d -m 1777 -o hdadmin -g hadoop /tmp/.hdfs-nfs

    log "Arrancando portmap (111) y NFS Gateway (2049/4242)..."
    # Portmap necesita root para el puerto 111.
    if hdfs --daemon start portmap; then
      log "portmap (Hadoop) OK"
    else
      log "portmap (Hadoop) falló; iniciando rpcbind del sistema..."
      rpcbind -w || true
    fi

    # Asegura que los logs sean escribibles por el usuario que lanza nfs3 (hdadmin).
    mkdir -p /opt/hadoop/logs
    chown -R hdadmin:hadoop /opt/hadoop/logs
    chmod 775 /opt/hadoop/logs

    # NFS Gateway en modo no seguro debe iniciarse como el usuario proxy (aquí hdadmin)
    su - hdadmin -c "hdfs --daemon start nfs3"

    log "NFS listo. Monta en tu equipo: sudo mount -t nfs -o vers=3,proto=tcp,nolock,sync localhost:/user/${HDFS_MOUNT_USER:-luser} ./hdfs"
    tail -f /dev/null
    ;;
  workbench)
    ensure_luser_uid
    wait_for_port namenode 9000 "RPC del NameNode"
    log "Workbench listo. Entra con: docker compose exec workbench bash"
    tail -f /dev/null
    ;;
  *)
    log "ROLE desconocido: $ROLE"
    exit 1
    ;;
esac
