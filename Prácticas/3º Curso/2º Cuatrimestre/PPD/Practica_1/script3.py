import os

print(f'hello from script 3, executed by process {os.getpid()}.')
f= open("file3.txt","w+")
f.write("hello from script 3")
f.close()
