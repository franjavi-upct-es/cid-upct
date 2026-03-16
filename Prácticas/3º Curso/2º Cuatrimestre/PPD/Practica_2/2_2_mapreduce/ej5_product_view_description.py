from mrjob.job import MRJob
from mrjob.step import MRStep

TOP_N = 10

class MRTopViewedProducts(MRJob):

    def mapper(self, _, line):
        """
        Mapper:
        - Lee cada línea del txt
        - Ignora líneas corruptas o cabecera
        - Extrae event_type, product_id, category_code, brand
        - Si event_type == "view", emite (product_id, (1, category_code, brand))
        """
        fields = line.strip().split(",")

        # Ignorar cabecera y líneas corruptas (mínimo 8 campos)
        if len(fields) < 8 or fields[0] == "event_time":
            return
        
        event_type = fields[1].strip()
        product_id = fields[2].strip()
        category_code = fields[4].strip()
        brand = fields[5].strip()

        # Solo nos interesan los eventos de tipo "view"
        if event_type == "view" and product_id:
            yield product_id, (1, category_code, brand)


    def reducer_count(self, product_id, values):
        """
        Reducer:
        - Suma el total de views para cada product_id y obtiene category_code y brand
        - Necesita iterar sobre todos los valores del tipo (count, category_code, brand) para sumar counts y obtener la info del producto
        - Emite (None, (total_views, product_id, category_code, brand))
        """
        total = 0
        category_code = ""
        brand = ""

        for count, cat, br in values:
            total += count
            # Guarda la primera categoría/marca no vacía encontrada
            if not category_code and cat:
                category_code = cat
            if not brand and br:
                brand = br

        # Clave None ⟶ todo va al mismo reducer_top_n
        yield None, (total, product_id, category_code, brand)
        
 
    def reducer_top_n(self, _, values):
        """
        Reducer:
        - Recibe (None, (total_views, product_id, category_code, brand)) para todos los productos
        - Ordena por total_views y emite los TOP_N productos más vistos
        """
        top = sorted(values, key=lambda x: x[0], reverse=True)[:TOP_N]

        for total_views, product_id, category_code, brand in top:
            yield product_id, [total_views, category_code, brand]
       
    
    # -------------------------
    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                reducer=self.reducer_count
            ),
            MRStep(
                reducer=self.reducer_top_n
            )
        ]


if __name__ == '__main__':
    MRTopViewedProducts.run()