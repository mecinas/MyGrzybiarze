import os

global_path = "/home/szymon/Desktop/7_Projekty 2021-2022Z/MyGrzybiarzeData/"
sufix = "/Test/"
directory_arr = ["Podgrzybek", "Kurka", "Muchomor sromotnikowy", "Muchomor sromotnikowy"]

correct = 0
all = 0
for directory_name in directory_arr:
    for file in os.listdir(global_path + directory_name + sufix):
        print(open(global_path + directory_name + sufix + file, 'rb').read())
