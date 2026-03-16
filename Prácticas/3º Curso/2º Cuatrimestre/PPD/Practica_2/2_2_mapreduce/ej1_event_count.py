from mrjob.job import MRJob
import csv

class MRCountEvents(MRJob):

    def mapper(self, _, line):
        """
        Mapper:
        - Lee cada línea del txt
        - Ignora líneas corruptas o cabecera
        - Extrae event_type
        - Yield (event_type, 1)
        """
        try:
            line = line.strip()
            parts = line.split(',')
            # línea corrupta o cabecera
            if len(parts) < 2 or parts[0] == 'event_time' or len(parts) < 8:
                return  
            
            event_type = parts[1]
            yield event_type, 1
        except Exception:
            # ignora líneas corruptas o cabecera
            pass

    def reducer(self, key, values):
        """
        Reducer:
        - Suma todos los valores asociados a cada event_type
        """
        yield key, sum(values)


if __name__ == '__main__':
    MRCountEvents.run()