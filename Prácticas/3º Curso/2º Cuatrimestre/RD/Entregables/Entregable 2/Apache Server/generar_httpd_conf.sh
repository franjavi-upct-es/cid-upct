#!/usr/bin/env bash
# ============================================================
# generar_httpd_conf.sh
# ============================================================
# Genera httpd.conf con AllowOverride All a partir del conf
# original de la imagen httpd.
# ============================================================
set -e

echo "[1/2] Extrayendo httpd.conf original..."
docker run --rm httpd cat /usr/local/apache2/conf/httpd.conf >httpd.conf.original

echo "[2/2] Aplicando AllowOverride All..."
sed 's/AllowOverride None/AllowOverride All/g' httpd.conf.original >httpd.conf
rm httpd.conf.original

echo "OK. Generado httpd.conf con AllowOverride All."
