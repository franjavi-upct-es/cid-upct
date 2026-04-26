"""
EJERCICIO 1: Contador de eventos sobre el dataset 2019-Oct.csv.

Cuenta cuántos eventos hay de cada tipo (view, cart, purchase) emitiendo
(event_type, 1) en el mapper y sumando en el reducer.
"""

import csv
import io

from mrjob.job import MRJob


class MRCountEvents(MRJob):

    def mapper(self, _, line):
        """
        Mapper:
        - Parsea cada línea como CSV (admite comas dentro de campos entrecomillados).
        - Ignora cabecera y líneas corruptas.
        - Emite (event_type, 1).
        """
        try:
            fields = next(csv.reader(io.StringIO(line)))
        except Exception:
            return

        # Cabecera o línea malformada
        if len(fields) < 9 or fields[0] == "event_time":
            return

        event_type = fields[1].strip()
        if event_type:
            yield event_type, 1

    def reducer(self, key, values):
        """
        Reducer:
        - Suma todos los valores asociados a cada event_type.
        """
        yield key, sum(values)


if __name__ == "__main__":
    MRCountEvents.run()
