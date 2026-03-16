from mrjob.job import MRJob

class MRUserEventCount(MRJob):

    def mapper(self, _, line):
        """
        Mapper:
        - Lee cada línea del txt
        - Ignora líneas corruptas o cabecera
        - Extrae user_id
        - Yield (user_id, 1)
        """
        fields = line.strip().split(",")

        # Ignorar cabecera y líneas corruptas (mínimo 5 campos)
        if len(fields) < 8 or fields[0] == "event_type":
            return
        
        user_id = fields[7].strip() # user_id está en la columna 4

        if user_id:
            yield user_id, 1

    def reducer(self, key, values):
        """
        Reducer:
        - Suma todos los valores asociados a cada user_id
        """
        yield key, sum(values)

if __name__ == '__main__':
    MRUserEventCount.run()