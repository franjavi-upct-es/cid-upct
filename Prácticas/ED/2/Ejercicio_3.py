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

if __name__ == '__main__':
    s = ArrayStack(10)
    for i in range(10):
        s.push(i)
    print(s.top())
    print(s.pop())
    print(s.is_empty())
    print(len(s))
    print(s.top())
    print(s.pop())