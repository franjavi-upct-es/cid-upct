import math

class Exception(Exception):
    pass

class ArrayStack:
    def __init__(self, maxlen):
        self._maxlen = maxlen
        self._data = [None] * self._maxlen
        self._top = -1

    def __len__(self):
        return self._top + 1

    def is_empty(self):
        return self._top == -1

    def push(self, e):
        if self._top == self._maxlen - 1:
            raise Exception('Stack is full')
        self._top += 1
        self._data[self._top] = e

    def top(self):
        if self.is_empty():
            raise Exception('Stack is empty')
        return self._data[self._top]

    def pop(self):
        if self.is_empty():
            raise Exception('Stack is empty')
        answer = self._data[self._top]
        self._data[self._top] = None
        self._top -= 1
        return answer

    def __str__(self):
        return str(self._data)

if __name__ == '__main__':
    S = ArrayStack(4)
    S.push(5)
    S.push(3)
    print(f'{S}')
    print(S.pop())
    S.push(2)
    S.push(8)
    print(f'{S}')
    print(S.pop())
    print(S.pop())
    S.push(9)
    S.push(1)
    print(f'{S}')
    print(S.pop())
    S.push(7)
    S.push(6)
    print(S.pop())
    S.push(4)
    print(f'{S}')
    print(S.pop())
    print(S.pop())
    print(f'{S}')