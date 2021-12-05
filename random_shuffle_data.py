from posixpath import join
import random
import sys
import os
import shutil 


TRAIN_RATIO = 0.8
EVAL_RATIO = 0.1

def random_shuffle(raw_folder, out_folder):
    all_files = [f for f in os.listdir(raw_folder)]

    num_files = len(all_files)
    num_train = int(TRAIN_RATIO * num_files)
    num_eval = int(EVAL_RATIO * num_files)
    num_test = num_files - num_train - num_eval

    index = [i for i in range(num_files)]
    random.shuffle(index)
    train_index = index[:num_train]
    eval_index = index[num_train: num_train + num_eval]
    test_index = index[num_train + num_eval:]

    train_path = os.path.join(out_folder, 'train')
    os.makedirs(train_path, exist_ok=True)
    for i in range(num_train):
        dirname = all_files[train_index[i]]
        src = os.path.join(raw_folder, dirname)
        dst = os.path.join(train_path, dirname)
        shutil.copytree(src, dst)
    
    eval_path = os.path.join(out_folder, 'eval')
    os.makedirs(eval_path, exist_ok=True)
    for i in range(num_eval):
        dirname = all_files[eval_index[i]]
        src = os.path.join(raw_folder, dirname)
        dst = os.path.join(eval_path, dirname)
        shutil.copytree(src, dst)

    test_path = os.path.join(out_folder, 'test')
    os.makedirs(test_path, exist_ok=True)
    for i in range(num_test):
        dirname = all_files[test_index[i]]
        src = os.path.join(raw_folder, dirname)
        dst = os.path.join(test_path, dirname)
        shutil.copytree(src, dst)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python random_shuffle_data.py <path to raw data> <path to processed data>")
        exit(0)
    
    raw_folder, out_folder = sys.argv[1:]
    random_shuffle(raw_folder, out_folder)