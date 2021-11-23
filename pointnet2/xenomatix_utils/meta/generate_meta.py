import os
file = open("anno_paths.txt", "a")
path = "/home/test/Pointnet_Pointnet2_pytorch/pointnet2/sample/data"
for f in os.listdir(path):
    sub = os.path.join(path, f)
    cnt = 0
    if os.path.isdir(sub):
        for i in os.listdir(sub):
            file.write(os.path.join(f, i, "Annotations"))
            file.write("\n")