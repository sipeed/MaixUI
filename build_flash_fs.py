import os, re, shutil

def tree_files(dir_):
    if not os.path.isdir(dir_):
        return [dir_]
    res = []
    for item in os.listdir(dir_):
        item = os.path.join(dir_, item)
        res.extend(tree_files(item))
    return res

def get_file_type(file):
    return os.path.splitext(file)[-1]

def all_mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    return os.path.exists(path)

def extract_file_by_suffix(source_dir='/', exclude=[], goal_dir='result\\', file_set=['.txt', '.rst', '.md'], function=lambda t:t):
    files = tree_files(source_dir)
    # print(files)
    for fe in files:
        # print(fe, get_file_type(fe))
        if get_file_type(fe) in file_set:
            if not any(f in fe for f in exclude):
                print(fe)
                path = os.path.basename(fe)
                shutil.copyfile(fe, goal_dir + path)

if __name__ == "__main__":
    all_mkdir('./fs')
    extract_file_by_suffix(source_dir='./', exclude=['./app', './test', './fs', 'main.py', 'settings.json', './build_flash_fs.py', 'cube.config.json', 'amigo.config.json'], goal_dir='fs/', file_set=['.py', '.json'])
    # build flash fs
    shutil.copyfile('./app/app_cube.py', './fs/main.py')
    # created main.py
    shutil.copytree("./res","./fs/res")
    shutil.copytree("./imgs","./fs/imgs")
