import keras
import numpy as np
import main

model = keras.models.load_model(" model_common")

common_input = open("common_input.txt")
arr = []
out_put = [open(file='russian_last_names_male.txt', errors='ignore'),
           open(file='russian_names_male.txt', errors='ignore'), open(file='russian_names_female.txt', errors='ignore'),
           open(file='russian_last_names_female.txt', encoding='utf-8', errors='ignore')]
for i in out_put:
    for j in i:
        arr.append(j)
arr_out = []
for i in common_input:
    dop_arr = []
    for j in i.split():
        dop_arr.append(float(j))
    arr_out.append(dop_arr)
# print(np.array(model.predict(arr_out)))
print(arr, len(arr))
