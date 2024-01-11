class Empty(Exception):
    pass

class ArrayStack:
    def __init__(self):
        self._data = []
    
    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, e):
        return self._data.append(e)

    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1]

    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop()

    def __str__(self):
        return ','.join(str(self._data[j]) for j in range(len(self._data)))

    

if __name__ == '__main__':
    S = ArrayStack()
    
    S.push(5)
    S.push(3)
    print(len(S))
    print(S.pop())
    print(f'[{S}]')
    print(S.is_empty())
    print(S.pop())
    print(S.is_empty())
    S.push(7)
    S.push(9)
    print(S.top())
    S.push(4)
    print(len(S))
    print(S.pop())
    S.push(6)
    S.push(8)
    print(S.pop())