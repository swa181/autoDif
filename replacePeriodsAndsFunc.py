import os
import shutil

path = "C:/Users/WINWU/OneDrive - FLC/01 CF/01 AC/"
files = os.listdir(path)
for f in files:
    if not any(char.isdigit() for char in f) and "&" in f and os.path.isdir(path+ f):
            print(f)
            os.rename(path+ f, path+ f.replace('&','and'))


#for root, dirs, files in os.walk("C:/Users/WINWU/OneDrive - FLC/01 CF/01 AC/"):
#    root = root.replace('\\','/')
#    if ('/410 Meeting Agenda' in root): # and (os.path.isdir(root)) and ("01 Orphan clients" not in root) and ("02 Nancy Lee" not in root) and ("03 Closed prospect files" not in root):
#        print(root)
#        os.rename(root, root.replace('/410 Meeting Agenda','/Meeting Agenda'))
