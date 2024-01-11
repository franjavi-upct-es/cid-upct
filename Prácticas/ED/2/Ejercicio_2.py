from Ejercicio_1 import *

class ArrayStack(ArrayStack):

    def __init__(self, maxlen):
        super().__init__()
        self._maxlen = maxlen

    def push(self, e):
        if len(self._data) == self._maxlen:
            raise Exception('Stack is full')
        return super().push(e)

    
if __name__ == '__main__':
    S = ArrayStack(5)
    
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
    print(f'[{S}]')
    S.push(1)
    print(S.pop())
    print(S.pop())
    print(S.pop())
    S.push(3)
    S.push(3)
    S.push(3)
    print(S.__len__())
    S.push(3)
    print(S.pop())
    print(S.pop())
    S.push(3)
    S.push(3)
    print(S.pop())
