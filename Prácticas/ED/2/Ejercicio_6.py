class Empty(Exception):
    pass

class ArrayQueue:

    def __init__(self):
        self._data = []
        self._size = 0
        self._front = 0


    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def enqueue(self,e):
        self._data.append(e)
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front += 1
        self._size -= 1
        return answer

    def __str__(self):
        return str(self._data)

    def first(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._data[self._front]