#!/usr/bin/env bash
set -euo pipefail

# Docker Engine install for Ubuntu 24.04 on WSL
# - Uses official Docker repo
# - Adds current user to docker group
# - Handles systemd vs non-systemd WSL setups

log() { echo -e "\n[+] $*\n"; }
warn() { echo -e "\n[!] $*\n"; }

if [[ $EUID -eq 0 ]]; then
  warn "No ejecutes este script como root. Ejecuta como tu usuario normal: ./install-docker-wsl-ubuntu2404.sh"
  exit 1
fi

log "Actualizando paquetes y dependencias..."
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release

log "Creando directorio de keyrings..."
sudo install -m 0755 -d /etc/apt/keyrings

log "Añadiendo la clave GPG oficial de Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

UBU_CODENAME="$(. /etc/os-release && echo "${VERSION_CODENAME}")"
ARCH="$(dpkg --print-architecture)"

log "Configurando el repositorio de Docker para Ubuntu (${UBU_CODENAME})..."
echo \
  "deb [arch=${ARCH} signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  ${UBU_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

log "Instalando Docker Engine..."
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

log "Añadiendo tu usuario al grupo docker (para usar docker sin sudo)..."
sudo usermod -aG docker "$USER"

log "Comprobando si systemd está activo..."
if command -v systemctl >/dev/null 2>&1 && systemctl is-system-running >/dev/null 2>&1; then
  log "systemd está activo. Habilitando y arrancando docker con systemd..."
  sudo systemctl enable --now docker
else
  warn "Parece que systemd NO está activo en tu WSL."
  warn "En ese caso, el daemon de Docker no arranca con systemctl."
  log "Probando arranque manual del daemon (dockerd) en segundo plano..."
  if pgrep -x dockerd >/dev/null 2>&1; then
    log "dockerd ya está corriendo."
  else
    sudo dockerd >/tmp/dockerd.log 2>&1 &
    sleep 2
    if pgrep -x dockerd >/dev/null 2>&1; then
      log "dockerd arrancó correctamente. Log: /tmp/dockerd.log"
    else
      warn "dockerd no parece haber arrancado. Revisa el log: /tmp/dockerd.log"
    fi
  fi

  warn "Opcional: para arrancar Docker al abrir tu shell en WSL, añade esto a ~/.bashrc o ~/.zshrc:"
  cat <<'EOF'

sudo apt-get install -y nfs-common

# --- Auto-start Docker in WSL (optional) ---
if ! pgrep -x dockerd >/dev/null 2>&1; then
  sudo dockerd >/tmp/dockerd.log 2>&1 &
fi
# ------------------------------------------
EOF
fi

log "Verificando instalación..."
# Necesitas cerrar sesión y volver a entrar para que el grupo docker se aplique.
warn "IMPORTANTE: Para que 'docker' funcione sin sudo, CIERRA esta terminal WSL y ábrela de nuevo."

# Prueba con sudo para evitar depender del refresh de grupos
sudo docker version || true
sudo docker run --rm hello-world || true

log "Listo. Si 'hello-world' imprimió el mensaje, Docker está funcionando."
