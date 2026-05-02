# coding=utf-8
#!/usr/bin/env python3
"""
Servidor HTTP en Python sobre sockets TCP.

Funcionalidades:
    * Serivicio de contenido estático via GET.
    * Procesamiento de formularios via POST (/accion_form.html).
    * Gestión de cookies (cookie_counter_XXYY) con límite de accesos
    * Conexiones persistentes HTTP (Keep-Alive) con timeout
    * Servidor concurrente mediante `os.fork()`
    * Errores HTTP 400, 403, 404, 405, 505
"""

import argparse
import logging
import os
import select
import socket
import sys
from datetime import datetime, timezone
from urllib.parse import unquote_plus

# ============================================================
# CONFIGURACIÓN DE GRUPO
# ============================================================
# XX y YY son las dos últimas cigras del DNI de cada miembro
XX = "10"  # <-- Francisco Javier Mercader Martínez, DNI 26649110E
YY = "49"  # <-- Mauro Martínez Cazaux, DNI 49273021Y

# Construcción automática de la cookie y del timeout según el enunciado.
# timeout = X + X + Y + Y + 10 (suma de cada una de las cuatro cifras)
COOKIE_NAME = f"cookie_counter_{XX}_{YY}"
TIMEOUT_CONNECTION = sum(int(c) for c in (XX + YY) if c.isdigit()) + 10

# ============================================================
# CONSTANTES
# ============================================================
BUFSIZE = 8192  # Tamaño máximo de buffer
MAX_ACCESOS = 5  # Accesos máximos antes de bloquear
COOKIE_MAX_AGE = 120  # Caducidad de la cookie (2 minutos)

# Extensiones admitidas (ext, MIME)
filetypes = {
    "gif": "image/gif",
    "jpg": "image/jpg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "htm": "text/htm",
    "html": "text/html",
    "css": "text/css",
    "js": "text/js",
}

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)03d] [%(levelname)-7s] [pid=%(process)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()


# ============================================================
# FUNCIONES BASICAS DE SOCKET
# ============================================================
def enviar_mensaje(cs, data):
    """Envia datos a traves del socket cs. Devuelve numero de bytes enviados."""
    cs.sendall(data)
    return len(data)


def recibir_mensaje(cs):
    """Recibe datos a traves del socket cs. Devuelve un objeto bytes."""
    return cs.recv(BUFSIZE)


def cerrar_conexion(cs):
    """Cierra una conexion activa."""
    try:
        cs.close()
    except Exception:
        pass


# ============================================================
# UTILIDAD: Fecha en formato HTTP (RFC 7231)
# ============================================================
def http_date():
    return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")


# ============================================================
# RESPUESTAS DE ERROR
# ============================================================
def enviar_error(cs, code, reason, message, keep_alive=False):
    """Envia una respuesta HTTP de error con una pagina HTML informativa."""
    body = (
        f'<html><head><meta charset="UTF-8"><title>{code} {reason}</title></head>'
        f"<body><h1>{code} {reason}</h1><p>{message}</p>"
        f"<hr><i>webRD_python</i></body></html>"
    ).encode("utf-8")

    if keep_alive:
        connection_h = (
            "Connection: keep-alive\r\n"
            f"Keep-Alive: timeout={TIMEOUT_CONNECTION}\r\n"
        )
    else:
        connection_h = "Connection: close\r\n"

    headers = (
        f"HTTP/1.1 {code} {reason}\r\n"
        f"Date: {http_date()}\r\n"
        "Server: webRD_python\r\n"
        f"{connection_h}"
        f"Content-Length: {len(body)}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "\r\n"
    ).encode("utf-8")

    enviar_mensaje(cs, headers + body)


# ============================================================
# COOKIES
# ============================================================
def process_cookies(headers, cs):
    """
    Procesa la cabecera Cookie en busca de la cookie de control de accesos.

    Reglas:
      * Si no se encuentra cookie_counter_XXYY -> devuelve 1 (primer acceso).
      * Si esta y vale MAX_ACCESOS -> devuelve MAX_ACCESOS.
      * Si esta y 1 <= valor < MAX_ACCESOS -> devuelve valor + 1.
    """
    for h in headers:
        if h.lower().startswith("cookie:"):
            valor_completo = h.split(":", 1)[1].strip()
            # Pueden coexistir varias cookies separadas por ";"
            for cookie in valor_completo.split(";"):
                cookie = cookie.strip()
                if cookie.startswith(COOKIE_NAME + "="):
                    try:
                        n = int(cookie.split("=", 1)[1])
                    except ValueError:
                        return 1
                    if n >= MAX_ACCESOS:
                        return MAX_ACCESOS
                    return n + 1
    return 1


# ============================================================
# RESPUESTA A POST: validacion del formulario
# ============================================================
def procesar_post_form(cs, body_text, keep_alive):
    """
    Procesa el formulario enviado via POST con application/x-www-form-urlencoded.
    Espera un campo 'email'. Valida si el dominio es @edu.upct.es.
    """
    email = ""
    for par in body_text.split("&"):
        if "=" in par:
            k, v = par.split("=", 1)
            if k.lower() == "email":
                email = unquote_plus(v)
                break

    correcto = email.lower().endswith("@edu.upct.es")

    if correcto:
        body = (
            '<html><head><meta charset="UTF-8">'
            "<title>Correo correcto</title></head>"
            "<body><h1>Correo correcto</h1>"
            f"<p>El correo <b>{email}</b> pertenece al dominio "
            "<code>@edu.upct.es</code>.</p>"
            '<p><a href="/">Volver al inicio</a></p>'
            "</body></html>"
        ).encode("utf-8")
    else:
        mostrado = email if email else "(vacio)"
        body = (
            '<html><head><meta charset="UTF-8">'
            "<title>Correo incorrecto</title></head>"
            "<body><h1>Correo incorrecto</h1>"
            f"<p>El correo <b>{mostrado}</b> NO pertenece al dominio "
            "<code>@edu.upct.es</code>.</p>"
            '<p><a href="/">Volver al inicio</a></p>'
            "</body></html>"
        ).encode("utf-8")

    if keep_alive:
        connection_h = (
            "Connection: keep-alive\r\n"
            f"Keep-Alive: timeout={TIMEOUT_CONNECTION}\r\n"
        )
    else:
        connection_h = "Connection: close\r\n"

    headers = (
        "HTTP/1.1 200 OK\r\n"
        f"Date: {http_date()}\r\n"
        "Server: webRD_python\r\n"
        f"{connection_h}"
        f"Content-Length: {len(body)}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "\r\n"
    ).encode("utf-8")

    enviar_mensaje(cs, headers + body)


# ============================================================
# PROCESAMIENTO PRINCIPAL DE LA PETICION
# ============================================================
def process_web_request(cs, files):
    """
    Procesa una o varias peticiones HTTP en una conexion TCP.

    Bucle Keep-Alive con select() y timeout. Sale del bucle cuando:
      * Se alcanza TIMEOUT_CONNECTION sin recibir datos
      * El cliente cierra la conexion
      * Se recibe Connection: close
      * Ocurre un error grave
    """
    while True:
        # ----------------------------------------------------------
        # 1) Esperar datos en el socket con timeout (Keep-Alive)
        # ----------------------------------------------------------
        rlist, _, _ = select.select([cs], [], [], TIMEOUT_CONNECTION)
        if not rlist:
            logger.info("Timeout de conexion alcanzado, cerrando...")
            break

        # ----------------------------------------------------------
        # 2) Leer la peticion
        # ----------------------------------------------------------
        raw = recibir_mensaje(cs)
        if not raw:
            logger.info("Cliente cerro la conexion (recv vacio).")
            break

        try:
            req_text = raw.decode("utf-8", errors="replace")
        except Exception as e:
            logger.error(f"Error decodificando peticion: {e}")
            enviar_error(cs, 400, "Bad Request", "Mensaje no decodificable")
            break

        # ----------------------------------------------------------
        # 3) Separar cabeceras y body
        # ----------------------------------------------------------
        if "\r\n\r\n" in req_text:
            header_text, body_text = req_text.split("\r\n\r\n", 1)
        else:
            header_text = req_text
            body_text = ""

        lines = header_text.split("\r\n")
        if not lines or not lines[0].strip():
            enviar_error(cs, 400, "Bad Request", "Peticion vacia")
            break

        request_line = lines[0]
        logger.info(f"Request line: {request_line}")

        # ----------------------------------------------------------
        # 4) Parsear linea de solicitud: METHOD PATH VERSION
        # ----------------------------------------------------------
        partes = request_line.split()
        if len(partes) != 3:
            enviar_error(
                cs, 400, "Bad Request", "Linea de solicitud mal formada"
            )
            break
        method, path, version = partes

        if version != "HTTP/1.1":
            enviar_error(
                cs,
                505,
                "HTTP Version Not Supported",
                f"Solo se soporta HTTP/1.1 (recibido {version})",
            )
            break

        if method not in ("GET", "POST"):
            enviar_error(
                cs, 405, "Method Not Allowed", f"Metodo {method} no permitido"
            )
            break

        # ----------------------------------------------------------
        # 5) Detectar Connection (keep-alive por defecto en HTTP/1.1)
        # ----------------------------------------------------------
        keep_alive = True  # Por defecto en HTTP/1.1
        for h in lines[1:]:
            if h.lower().startswith("connection:"):
                valor = h.split(":", 1)[1].strip().lower()
                if "close" in valor:
                    keep_alive = False
                elif "keep-alive" in valor:
                    keep_alive = True

        # Logging de cabeceras (modo verbose)
        for h in lines[1:]:
            if h.strip():
                logger.debug(f"Header: {h}")

        # ----------------------------------------------------------
        # 6) POST: procesar formulario
        # ----------------------------------------------------------
        if method == "POST":
            content_length = 0
            for h in lines[1:]:
                if h.lower().startswith("content-length"):
                    try:
                        content_length = int(h.split(":", 1)[1].strip())
                    except ValueError:
                        content_length = 0
                    break

            # Asegurar que tenemos todo el body
            while len(body_text.encode("utf-8")) < content_length:
                more = recibir_mensaje(cs)
                if not more:
                    break
                body_text += more.decode("utf-8", errors="replace")

            logger.info(f"POST body: {body_text}")
            procesar_post_form(cs, body_text, keep_alive)

            if not keep_alive:
                break
            continue

        # ----------------------------------------------------------
        # 7) GET: servir fichero estatico
        # ----------------------------------------------------------
        # Eliminar query string
        if "?" in path:
            path = path.split("?", 1)[0]

        # / -> index.html
        if path == "/":
            resource = "index.html"
        else:
            resource = path.lstrip("/")

        # Seguridad minima: rechazar path traversal
        if ".." in resource or resource.startswith("\\") or ":" in resource:
            enviar_error(
                cs, 403, "Forbidden", "Acceso al recurso denegado", keep_alive
            )
            if not keep_alive:
                break
            continue

        filepath = os.path.join(files, resource)

        if not os.path.isfile(filepath):
            enviar_error(
                cs,
                404,
                "Not Found",
                f"El recurso solicitado no existe: /{resource}",
                keep_alive,
            )
            if not keep_alive:
                break
            continue

        # ----------------------------------------------------------
        # 8) Cookies: solo se incrementan al pedir index.html
        # ----------------------------------------------------------
        cookie_header = b""
        if resource == "index.html":
            n = process_cookies(lines[1:], cs)
            logger.info(f"{COOKIE_NAME} = {n}")

            if n >= MAX_ACCESOS:
                # Bloqueo: 403 Forbidden con pagina informativa
                body = (
                    '<html><head><meta charset="UTF-8">'
                    "<title>403 Forbidden</title></head>"
                    "<body><h1>403 Forbidden</h1>"
                    f"<p>Has alcanzado el numero maximo de accesos permitidos "
                    f"(<b>{MAX_ACCESOS}</b>) a esta pagina.</p>"
                    f"<p>Espera 2 minutos para que expire la cookie.</p>"
                    "<hr><i>webRD_python</i></body></html>"
                ).encode("utf-8")

                if keep_alive:
                    connection_h = (
                        "Connection: keep-alive\r\n"
                        f"Keep-Alive: timeout={TIMEOUT_CONNECTION}\r\n"
                    )
                else:
                    connection_h = "Connection: close\r\n"

                headers = (
                    "HTTP/1.1 403 Forbidden\r\n"
                    f"Date: {http_date()}\r\n"
                    "Server: webRD_python\r\n"
                    f"{connection_h}"
                    f"Set-Cookie: {COOKIE_NAME}={MAX_ACCESOS}; Max-Age={COOKIE_MAX_AGE}\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    "\r\n"
                ).encode("utf-8")
                enviar_mensaje(cs, headers + body)

                if not keep_alive:
                    break
                continue

            cookie_header = (
                f"Set-Cookie: {COOKIE_NAME}={n}; Max-Age={COOKIE_MAX_AGE}\r\n"
            ).encode("utf-8")

        # ----------------------------------------------------------
        # 9) Construir y enviar respuesta 200 OK
        # ----------------------------------------------------------
        ext = filepath.rsplit(".", 1)[-1].lower()
        content_type = filetypes.get(ext, "application/octet-stream")
        size = os.path.getsize(filepath)

        if keep_alive:
            connection_h = (
                "Connection: keep-alive\r\n"
                f"Keep-Alive: timeout={TIMEOUT_CONNECTION}\r\n"
            ).encode("utf-8")
        else:
            connection_h = b"Connection: close\r\n"

        # Charset solo para texto
        ct_header = content_type
        if content_type.startswith("text/"):
            ct_header += "; charset=utf-8"

        headers = (
            (
                "HTTP/1.1 200 OK\r\n"
                f"Date: {http_date()}\r\n"
                "Server: webRD_python\r\n"
            ).encode("utf-8")
            + connection_h
            + (
                f"Content-Length: {size}\r\nContent-Type: {ct_header}\r\n"
            ).encode("utf-8")
            + cookie_header
            + b"\r\n"
        )

        enviar_mensaje(cs, headers)

        # Enviar cuerpo en bloques de BUFSIZE bytes
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(BUFSIZE)
                if not chunk:
                    break
                enviar_mensaje(cs, chunk)

        # ----------------------------------------------------------
        # 10) Salir si no es keep-alive
        # ----------------------------------------------------------
        if not keep_alive:
            break

    cerrar_conexion(cs)


# ============================================================
# MAIN: servidor concurrente con fork
# ============================================================
def main():
    """Servidor web TCP concurrente."""
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-p", "--port", type=int, required=True, help="Puerto del servidor"
        )
        parser.add_argument(
            "-ip",
            "--host",
            required=True,
            help="Direccion IP del servidor o localhost",
        )
        parser.add_argument(
            "-f",
            "--files",
            help="Directorio base desde donde se sirven los ficheros",
        )
        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Imprimir mensajes de depuracion",
        )
        args = parser.parse_args()

        if args.verbose:
            logger.setLevel(logging.DEBUG)

        logger.info(
            f"Enabling server in address {args.host} and port {args.port}."
        )
        logger.info(f"Serving files from {args.files}")
        logger.info(f"COOKIE_NAME = {COOKIE_NAME}")
        logger.info(f"TIMEOUT_CONNECTION = {TIMEOUT_CONNECTION}s")

        # ----------------------------------------------------------
        # Crear socket TCP, permitir reuso de direccion, bind y listen
        # ----------------------------------------------------------
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((args.host, args.port))
        sock.listen()

        # ----------------------------------------------------------
        # Bucle principal: aceptar conexiones y bifurcar el proceso
        # ----------------------------------------------------------
        while True:
            cs, addr = sock.accept()
            logger.info(f"Accepted connection from {addr}")

            # Recolectar zombies de hijos previos sin bloquear
            try:
                while True:
                    wpid, _ = os.waitpid(-1, os.WNOHANG)
                    if wpid == 0:
                        break
            except (ChildProcessError, OSError):
                pass

            # fork() solo existe en sistemas POSIX (Linux contenedor Docker).
            # Si se ejecuta en Windows, se cae a modo iterativo.
            try:
                pid = os.fork()
            except (AttributeError, OSError):
                logger.warning("os.fork() no disponible, modo iterativo.")
                try:
                    process_web_request(cs, args.files)
                except Exception as e:
                    logger.exception(f"Error procesando peticion: {e}")
                finally:
                    cerrar_conexion(cs)
                continue

            if pid == 0:
                # PROCESO HIJO: cierra el socket de escucha del padre,
                # atiende la peticion y termina.
                sock.close()
                try:
                    process_web_request(cs, args.files)
                except Exception as e:
                    logger.exception(f"Error procesando peticion: {e}")
                finally:
                    cerrar_conexion(cs)
                sys.exit(0)
            else:
                # PROCESO PADRE: cierra el socket conectado y vuelve a esperar
                cerrar_conexion(cs)

    except KeyboardInterrupt:
        logger.info("Servidor detenido por el usuario.")
    except Exception as e:
        logger.exception(f"Error en main: {e}")


if __name__ == "__main__":
    main()
