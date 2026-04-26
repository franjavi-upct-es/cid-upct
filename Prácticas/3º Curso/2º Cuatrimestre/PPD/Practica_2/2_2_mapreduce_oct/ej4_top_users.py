"""
EJERCICIO 4: Top 10 usuarios con más interacciones sobre 2019-Oct.csv.

Calcula los TOP_N usuarios con mayor número de interacciones totales
(de cualquier tipo) usando dos pasos MapReduce:
    1) Conteo por user_id.
    2) Reducer único que ordena y selecciona los TOP_N.
"""

import csv
import io

from mrjob.job import MRJob
from mrjob.step import MRStep

TOP_N = 10


class MRTopUsers(MRJob):

    def mapper_count(self, _, line):
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

    def reducer_count(self, user_id, values):
        """
        Reducer parcial:
        - Suma las interacciones de cada user_id.
        - Emite (None, (total, user_id)) para forzar que todos los
          registros vayan al mismo reducer en el siguiente paso.
        """
        yield None, (sum(values), user_id)

    def reducer_topn(self, _, user_count_pairs):
        """
        Reducer final:
        - Recibe todos los (total, user_id) bajo la clave None.
        - Ordena por total descendente y emite los TOP_N.
        """
        top = sorted(user_count_pairs, key=lambda x: x[0], reverse=True)[:TOP_N]
        for total, user_id in top:
            yield user_id, total

    def steps(self):
        return [
            MRStep(mapper=self.mapper_count, reducer=self.reducer_count),
            MRStep(reducer=self.reducer_topn),
        ]


if __name__ == "__main__":
    MRTopUsers.run()
