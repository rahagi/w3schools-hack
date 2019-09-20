import os

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def write(dir, name, str):
    if not os.path.exists(dir):
        mkdir(dir)

    with open(dir + "/" + name , 'w') as f:
        f.write(str)

def cd(dir):
    if not os.path.exists(dir):
        print("directory doesn't exist")
    os.chdir(dir)