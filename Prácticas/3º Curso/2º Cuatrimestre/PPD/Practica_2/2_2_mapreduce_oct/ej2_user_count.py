"""
EJERCICIO 2: Contador de interacciones por usuario sobre 2019-Oct.csv.

Para cada user_id, calcula el número total de interacciones con la
plataforma (independientemente del tipo de evento).
"""

import csv
import io

from mrjob.job import MRJob


class MRUserCount(MRJob):

    def mapper(self, _, line):
        """
        Mapper:
        - Parsea cada línea como CSV.
        - Ignora cabecera y líneas corruptas.
        - Emite (user_id, 1).
        """
        try:
            fields = next(csv.reader(io.StringIO(line)))
        except Exception:
            return

        if len(fields) < 9 or fields[0] == "event_time":
            return

        user_id = fields[7].strip()
        if user_id:
            yield user_id, 1

    def reducer(self, key, values):
        """
        Reducer:
        - Suma todas las interacciones de cada user_id.
        """
        yield key, sum(values)


if __name__ == "__main__":
    MRUserCount.run()
