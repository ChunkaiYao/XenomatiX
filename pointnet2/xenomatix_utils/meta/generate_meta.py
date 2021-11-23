import os
file = open("anno_paths.txt", "w")
# path = "/home/test/Pointnet_Pointnet2_pytorch/pointnet2/sample/data"
data_path = os.getcwd()
data_path = os.path.abspath(os.path.join(data_path, os.pardir, os.pardir))
data_path = os.path.join(data_path, 'sample', 'data')

for f in os.listdir(data_path):
    sub = os.path.join(data_path, f)
    cnt = 0
    if os.path.isdir(sub):
        for i in os.listdir(sub):
            file.write(os.path.join(f, i, "Annotations"))
            file.write("\n")