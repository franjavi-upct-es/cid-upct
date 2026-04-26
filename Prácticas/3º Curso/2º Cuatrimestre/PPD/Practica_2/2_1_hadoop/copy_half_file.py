#! /usr/bin/env python3
import shutil
import sys

from pyarrow.fs import FileInfo, FileSystem


def copy_half_file(uri1: str, uri2: str) -> None:
    fs1, path1 = FileSystem.from_uri(uri1)
    fs2, path2 = FileSystem.from_uri(uri2)

    # Obtener información del archivo en fs1
    f_info: FileInfo = fs1.get_file_info(path1)

    with (
        fs1.open_input_file(path1) as instream,
        fs2.open_output_stream(path2) as outstream,
    ):
        # Mover el puntero de instream a la mitad del archivo
        size = f_info.size
        instream.seek(size // 2)
        # Copiar el resto del archivo en outstream
        shutil.copyfileobj(instream, outstream)


if __name__ == "__main__":
    # Si no se proporcionan dos argumentos, se muestra un mensaje de error
    if len(sys.argv) != 3:
        print("Uso: {} <uri1> <uri2>".format(sys.argv[0]))
        sys.exit(1)

    copy_half_file(sys.argv[1], sys.argv[2])
