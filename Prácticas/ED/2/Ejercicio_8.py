class Exception(Exception):
    pass

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:

    def __init__(self):
        self.head = None

    def insert(self, data):
        if not self.head :
            self.head = Node(data)
        else:
            current_node = self.head
            while current_node.next:
                current_node = current_node.next
            current_node.next = Node(data)

    def pop(self):
        if not self.head:
            return None
        else:
            data = self.head.data
            self.head = self.head.next
            return data

class LinkedQueue:
    
    def __init__(self):
        self._data = LinkedList()
        self._size = 0

    def __len__(self):
        return self._size

    def enqueue(self, e):
        self._data.insert(e)
        self._size += 1

    def is_empty(self):
        return self._size == 0

    def dequeue(self):
        if self.is_empty():
            return Exception("Queue is empty")
        else:
            self._size -= 1
            return self._data.pop()

    def first(self):
        if self.is_empty():
            return Exception("Queue is empty")
        else:
            return self._data.head.data

    def __str__(self):
        current_node = self._data.head
        elements = []
        while current_node:
            elements.append(str(current_node.data))
            current_node = current_node.next
        return ' -> '.join(elements)

if __name__ == '__main__':
    S = LinkedQueue()
    S.enqueue(5)
    S.enqueue(3)
    print(S.dequeue())
    S.enqueue(2)
    S.enqueue(8)
    print(S)
    print(S.dequeue())
    print(S.dequeue())
    S.enqueue(9)
    S.enqueue(1)
    print(S.dequeue())
    print(S.dequeue())
    S.enqueue(4)
    print(S.dequeue())
    print(S.dequeue())
    