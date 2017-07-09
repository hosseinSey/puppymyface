
from shutil import copy2
from glob import glob
import os

# list all the files

source_path = "/Users/Hossein/Downloads/dogImages/train/"
dest_path = "/Users/Hossein/Desktop/dogImages/"

dir_list = glob(source_path + '*')

for source_dir in dir_list: 
    dest_file_path = dest_path + source_dir.split('/')[-1] + '/'
    print(dest_file_path)
    directory = os.path.dirname(dest_file_path)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)       

    file_list = glob(source_dir + '/*')
    for f in file_list[:5]: 
        copy2(f, dest_file_path)

