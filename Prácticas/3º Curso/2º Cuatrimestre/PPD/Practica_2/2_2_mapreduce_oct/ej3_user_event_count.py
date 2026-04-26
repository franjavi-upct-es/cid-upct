"""
EJERCICIO 3: Contador de interacciones por usuario y tipo de evento
sobre 2019-Oct.csv.

Para cada par (user_id, event_type) calcula cuántas veces ese usuario
ha realizado ese tipo de evento.
"""

import csv
import io

from mrjob.job import MRJob


class MRUserEventCount(MRJob):

    def mapper(self, _, line):
        """
        Mapper:
        - Parsea cada línea como CSV.
        - Ignora cabecera y líneas corruptas.
        - Emite ((user_id, event_type), 1).
        """
        try:
            fields = next(csv.reader(io.StringIO(line)))
        except Exception:
            return

        if len(fields) < 9 or fields[0] == "event_time":
            return

        event_type = fields[1].strip()
        user_id = fields[7].strip()

        if user_id and event_type:
            yield (user_id, event_type), 1

    def reducer(self, key, values):
        """
        Reducer:
        - Suma las ocurrencias de cada (user_id, event_type).
        """
        yield key, sum(values)


if __name__ == "__main__":
    MRUserEventCount.run()
