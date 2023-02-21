import os


path = "/home/szymon/Desktop/Moje rzeczy/Projekty/7_Projekty 2021-2022Z/MyGrzybiarzeData/YOLOFormatDataset/Project_mushroom.v1i.yolov7pytorch"
test_path = "/test/labels/"
train_path = "/train/labels/"
valid_path = "/valid/labels/"

def changeDatasetCategory(complete_path_to_labels):
    for annotation_file_name in os.listdir(complete_path_to_labels):
        file = open(complete_path_to_labels + annotation_file_name, "r+")
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = '0' + lines[i][1:]
        file.seek(0)
        file.truncate()
        file.writelines(lines)
        file.close()

changeDatasetCategory(path + test_path)
changeDatasetCategory(path + train_path)
changeDatasetCategory(path + valid_path)