import os

print(f'hello from script 2, executed by process {os.getpid()}.')
f= open("file2.txt","w+")
f.write("hello from script 2")
f.close()
