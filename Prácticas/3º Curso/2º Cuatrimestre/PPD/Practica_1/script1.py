import os
print(f'hello from script 1, executed by process {os.getpid()}.')
f= open("file1.txt","w+")
f.write("hello from script 1")
f.close()
