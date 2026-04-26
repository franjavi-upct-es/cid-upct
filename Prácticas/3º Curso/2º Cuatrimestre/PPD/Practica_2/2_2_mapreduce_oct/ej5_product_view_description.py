"""
EJERCICIO 5: Top 10 productos más vistos junto con su categoría y
marca, sobre 2019-Oct.csv.

Filtra eventos de tipo 'view' y calcula los TOP_N productos con mayor
número de visualizaciones, devolviendo además category_code y brand.
"""

import csv
import io

from mrjob.job import MRJob
from mrjob.step import MRStep

TOP_N = 10


class MRTopViewedProducts(MRJob):

    def mapper(self, _, line):
        """
        Mapper:
        - Parsea cada línea como CSV.
        - Ignora cabecera y líneas corruptas.
        - Sólo procesa eventos 'view'.
        - Emite (product_id, (1, category_code, brand)).
        """
        try:
            fields = next(csv.reader(io.StringIO(line)))
        except Exception:
            return

        if len(fields) < 9 or fields[0] == "event_time":
            return

        event_type = fields[1].strip()
        product_id = fields[2].strip()
        category_code = fields[4].strip()
        brand = fields[5].strip()

        if event_type == "view" and product_id:
            yield product_id, (1, category_code, brand)

    def reducer_count(self, product_id, values):
        """
        Reducer parcial:
        - Suma el total de views por product_id.
        - Conserva la primera category_code y brand no vacías.
        - Emite (None, (total_views, product_id, category_code, brand)).
        """
        total = 0
        category_code = ""
        brand = ""

        for count, cat, br in values:
            total += count
            if not category_code and cat:
                category_code = cat
            if not brand and br:
                brand = br

        yield None, (total, product_id, category_code, brand)

    def reducer_top_n(self, _, values):
        """
        Reducer final:
        - Ordena los productos por total_views descendente.
        - Emite los TOP_N como (product_id, [total_views, category_code, brand]).
        """
        top = sorted(values, key=lambda x: x[0], reverse=True)[:TOP_N]
        for total_views, product_id, category_code, brand in top:
            yield product_id, [total_views, category_code, brand]

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer_count),
            MRStep(reducer=self.reducer_top_n),
        ]


if __name__ == "__main__":
    MRTopViewedProducts.run()
