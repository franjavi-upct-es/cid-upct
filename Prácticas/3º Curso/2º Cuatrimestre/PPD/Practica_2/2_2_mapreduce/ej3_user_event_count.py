from mrjob.job import MRJob


class MRUserEventCount(MRJob):
    def mapper(self, _, line):
        """
        Mapper:
        - Lee cada línea del txt
        - Ignora líneas corruptas o cabecera
        - Extrae user_id
        - Yield (user_id, envent_type, 1)
        """
        fields = line.strip().split(",")

        # Ignorar cabecera y líneas corruptas (mínimo 8 campos)
        if len(fields) < 8 or fields[0] == "event_time":
            return

        event_type = fields[1].strip()  # event_type está en la columna 1
        user_id = fields[7].strip()  # user_id está en la columna 7

        if user_id and event_type:
            yield (user_id, event_type), 1

    def reducer(self, key, values):
        """
        Reducer:
        - Suma todos los valores asociados a cada user_id, event_type
        """
        yield key, sum(values)


if __name__ == "__main__":
    MRUserEventCount.run()
