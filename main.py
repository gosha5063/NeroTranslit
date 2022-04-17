import tensorflow
from matplotlib import pyplot as plt
import keras
from keras import layers
import numpy as np
from transliterate import translit
import math
import random
import time


"""нахождение максимального слова в массиве"""
def find_max_len(file):
    max_len = 0
    cnt = 0
    for i in file.read():
        if i != "\n":
            cnt += 1
            if max_len < cnt:
                max_len = cnt
        else:
            cnt = 0
    return max_len


# def to_eaqul(file, dict_ru):
#     arr = []
#     dop_arr = []
#
#     max_len = find_max_len(file)
#     file.seek(0)
#     cnt = 0
#     for i in file.read().upper():
#         if i in dict_ru.keys():
#             cnt += 1
#             dop_arr.append(float(dict_ru.get(i)))
#         else:
#             for j in range(max_len-cnt):
#                 dop_arr.append(0.0)
#             arr.append(dop_arr)
#             dop_arr = []
#             cnt = 0
#     return arr, max_len
#
#
# def to_eaqul1(file, dict_eng):
#     arr = []
#     dop_arr = []
#
#     max_len = find_max_len(file)
#     file.seek(0)
#     cnt = 0
#     for i in file.read().upper():
#         if i in dict_eng.keys():
#             cnt += 1
#             dop_arr.append(float(dict_eng.get(i)))
#         else:
#             for j in range(max_len-cnt):
#                 dop_arr.append(0.5)
#             arr.append(dop_arr)
#             dop_arr = []
#             cnt = 0
#     # print(arr[:2])
#     return arr, max_len
def to_eaqul(file, dict_ru):
    arr = []
    dop_arr = []
    cnt = 0
    max_cnt = 209
    file.seek(0)
    for i in file.read().upper():
        if i in dict_ru.keys():
            cnt += len(dict_ru.get(i))
            dop_arr += dict_ru.get(i)
        else:
            if cnt > max_cnt:
                max_cnt = cnt
            arr.append(dop_arr)
            dop_arr = []
            cnt = 0
    for i in arr:
        for j in range(max_cnt - len(i)):
            i.append(-1.0)

    return arr

def Cail(num):
  if 0.1 < num < 0.6:
    return 0.5
  elif num > 0.6:
    return 1.0
  else:
    return 0.0
def Decoder(arr, dict_ru):
    s  = ''

    arr2 = []
    dop_arr = []
    ans = []
    for i in arr:
        for elm in i:
            dop_arr.append(Cail(elm))
        arr2.append(dop_arr)
        dop_arr = []
    for i in arr2:
        for ind in range(len(i) // 11):
            for j in dict_ru:
                if dict_ru[j] == i[11 * ind:11 * (ind + 1)]:
                    s+= j
        ans.append(s)
        s = ''
    return ans
"""создание алфавита из float занчений"""
# def vectorise_ru_letter():
#     const = 33
#     dict_ru = dict()
#
#     for i in range(1,const):
#         dict_ru[chr(1040+i-1)] = i/33
#     dict_ru['Ё'] = 1
#     return  dict_ru
# def vectorise_eng_letter():
#     const = 26
#     dict_eng = dict()
#
#     for i in range(1, const + 1):
#         dict_eng[chr(65+i-1)] = i / 27
#     dict_eng["\'"] = 1
#     return dict_eng
def vectorise_ru_letter():
    const = 32
    dict_ru = dict()

    for i in range(1,const+1):
        cnt = 0
        arr = []
        for j in bin(ord(chr(1040+i-1))):
            if cnt > 1:
                if float(j):
                    arr.append(float(j))
                else:
                    arr.append(float(j)+0.5)

            cnt += 1
        dict_ru[chr(1040+i-1)] = arr

    dict_ru['Ё'] = [1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1]

    return dict_ru


def vectorise_eng_letter():
    const = 26
    dict_eng = dict()

    for i in range(1,const+1):
        cnt = 0
        arr = []

        for j in bin(ord(chr(65+i-1))):
            if cnt > 1:
                if float(j):
                    arr.append(float(j))
                else:
                    arr.append(float(j)+0.5)
            cnt += 1
        dict_eng[chr(65+i-1)] = arr

    dict_eng["\'"] = [1, 0.5, 0.5, 1, 1, 1]
    return dict_eng
"""код для присвоения букве числа от одного до 27"""
# def vectorise_eng_letter():
#     const = 26
#     dict_eng = dict()
#
#     for i in range(1, const+1):
#         dict_eng[chr(65+i-1)] = i
#     dict_eng["\'"] = 27
#
#     return dict_eng



"""код для превращения букв в огромные числа"""
# def eng_creation():
#     code_len_eng = 6
#     lens = 0
#     dict_eng = dict()
#     for i in product('23', repeat = code_len_eng):
#         if lens<26:
#             dict_eng[chr(lens+65)] = (''.join(i))
#             dict_eng[chr(lens + 65)] = int(dict_eng[chr(lens+65)])
#         else:
#             break
#         lens += 1
#     dict_eng["\'"] = 233232
#
#     return dict_eng


# def ru_creation():
#     code_len_ru = 8
#     lens = 0
#     dict_ru = dict()
#     for i in product('10', repeat = code_len_ru):
#         if lens < 32:
#             dict_ru[chr(1040+lens)] = ''.join(i)
#             dict_ru[chr(1040+lens)] = int(dict_ru[chr(1040+lens)])
#         else:
#             break
#         lens+=1
#     dict_ru['Ё'] = 11011111
#     return dict_ru

# def check(output, arr):
#     for file in output:
#         obs_error = 0
#         for i in arr:
#             error = 0
#             word = file
#             for j in range(len(i)):
#                 try:
#                     if i[j] != word[j].upper():
#                         error=1
#                 except:
#                     print(i, word, len(i), len(word))
#             obs_error+=error
#             print(error, i, word)
#         print(1-obs_error/len(output))
def translite(file, file1):
    dict_diff = {'A':'А','B': 'Б','V':'В','G':'Г','D':'Д','E':'Е','YE':'Ё','J':'Ж','Z':'З','I':'И','Y':'Й'
    ,'K':'К','L':'Л','M':'М','N':'Н','O':'О','P':'П','R':'Р','S':'С','T':'Т','U':'У','F':'Ф','KH':'Х','C':'Ц','CH':'Ч','SH':'Ш','SC':'Щ','EH':'Э','YU':'Ю','YA':'Я'}
    file.seek(0)
    for i in file:
        s = ''
        print(i)
        for j in i.upper():
            if j != 'Ы':
                for key, value in dict_diff.items():
                    if value == j:
                        s += key
                        break
            else: s += 'Y'
        file1.write(s+'\n')
    file1.close()

def check(output, arr):
    obs_error = 0
    for i in range(len(output)):
        word = output[i]
        error = 0
        try:
            if len(word) != len(arr[i]):
                print("разное количесво букв", arr[i], word)
                error = 1
                continue
            for j in range(len(output[i])):
                if word[i].upper() != arr[i][j]:
                    error = 1
            obs_error += error
            print(error, arr[i], word)
        except:
            print("какая-то ошибка", arr[i])
    print(1 - obs_error/len(output))


# class DataSet_method():
#     def __init__(self, dict_ru, dict_eng):
        # self.file_female_russian_names = open(file='D:\\translit\русские имена\\russian_names_female.txt', errors='ignore')
        # self.file_male_russian_names = open(file = 'D:\\translit\русские имена\\russian_names_male.txt',errors='ignore')
        # self.file_male_russian_last_names = open(file = 'D:\\translit\русские имена\\russian_last_names_male.txt',errors='ignore')
        # self.file_female_russian_last_names = open(file = 'русские имена/russian_last_names_female.txt',encoding='utf-8', errors='ignore')
        #
        # self.male_last_names = open(file = 'транслитирированнные имена/male_last_names_data.txt',encoding='utf-8',errors='ignore')
        # self.male_names = open(file = 'транслитирированнные имена/male_names_data.txt',encoding='utf-8',errors='ignore')
        # self.female_names = open(file='транслитирированнные имена/female_names_data.txt')
        # self.female_last_names = open(file='транслитирированнные имена/female_last_names_data.txt',encoding='utf-8',errors='ignore')

        # self.dict_eng = dict_eng
        # self.dict_ru = dict_ru
        #
        # self.file_female_russian_names_bin, self.max_female = to_eaqul(self.file_female_russian_names, self.dict_ru)
        # self.file_male_russian_names_bin,self.max_male = to_eaqul(self.file_male_russian_names,self.dict_ru)
        # self.file_male_russian_last_names_bin,self.max_last_male = to_eaqul(self.file_male_russian_last_names, self.dict_ru)
        # self.file_female_russian_last_names_bin,self.max_last_female = to_eaqul(self.file_female_russian_last_names, self.dict_ru)
        #
        # self.male_last_names_bin_test, self.max_last_male_bin = to_eaqul(self.male_last_names, self.dict_eng)
        # self.male_names_bin_test, self.max_male_bin = to_eaqul(self.male_names, self.dict_eng)
        # self.female_names_bin_test, self.max_female_bin = to_eaqul(self.female_names, self.dict_eng)
        # self.female_last_names_bin_test, self.max_last_female_bin = to_eaqul(self.female_last_names, self.dict_eng)
        #
        # self.common_input = self.male_last_names_bin_test + self.male_names_bin_test+self.female_names_bin_test+self.female_last_names_bin_test
        # self.common_output = self.file_male_russian_last_names_bin + self.file_male_russian_names_bin+self.file_female_russian_names_bin+self.file_female_russian_last_names_bin
        # # file_inp = open("common_input.txt", 'w', encoding='utf-8')

        # for i in self.common_input:
        #     for j in i:
        #         file_inp.write(str(j) + ' ')
        #     file_inp.write('\n')
        # file_inp.close()
    # def check(self):
    #     translite(self.file_female_russian_last_names)

    def init_all(self):
        file1 = open('транслитирированнные имена/female_last_names_data.txt', 'w',encoding='utf-8', errors='ignore')
        file2 = open('транслитирированнные имена/male_names_data.txt', 'w',errors='ignore')
        file3 = open('транслитирированнные имена/male_last_names_data.txt','w',encoding='utf-8',errors='ignore')
        file4 = open('транслитирированнные имена/female_names_data.txt','w')
        self.file_male_russian_names.seek(0)
        self.file_female_russian_last_names.seek(0)
        self.file_male_russian_last_names.seek(0)
        self.file_female_russian_names.seek(0)

        for i in self.file_female_russian_last_names:
            file1.write(translit(str(i), language_code='ru', reversed=True))
        for i in self.file_male_russian_names:
            file2.write(translit(str(i), language_code='ru', reversed=True))
        for i in self.file_male_russian_last_names:
            file3.write(translit(str(i),language_code='ru', reversed=True))
        for i in self.file_female_russian_names:
            file4.write(translit(str(i),language_code='ru', reversed=True))


    def init_common_russia(self):
        file1 = open("common_file_russian.txt", 'w')
        arr = [self.file_female_russian_names,
        self.file_male_russian_names,
        self.file_male_russian_last_names ,
        self.file_female_russian_last_names]
        for i in arr:
            i.seek(0)
            for name in i:
                if name != '\n':
                    file1.write(name)
        print(1)
    def init_common_eng(self):
        file1 = open("посторонние файлы, обобщающие/common_file_eng.txt", 'w')
        arr = [self.female_names ,
               self.male_names,
               self.male_last_names,
               self.file_female_russian_last_names]
        for i in arr:
            i.seek(0)
            for name in i:
                if name!='\n':
                    file1.write(name)
        print(1)

    def init_mistakes(self):
        pass
    def Neroset(self):
        input = np.array(self.female_names_bin_test)
        output = np.array(self.file_female_russian_names_bin)
        input = np.array(self.common_input)
        output = np.array(self.common_output)
        input2 = np.array(self.male_names_bin_test)
        model = keras.Sequential()
        # model.add(layers.Dense(units=209, activation="tanh"))
        #         # model.add(layers.Dense(units=256, activation="sigmoid"))
        #         # model.add(layers.Dense(units=256, activation="sigmoid"))
        #         # model.add(layers.Dense(units=209, activation='sigmoid'))

        # print(len(input2[0]))
        # print(len(input[0]))
        model.compile(optimizer='adam', loss = "mse", metrics=["accuracy"])
        fit_result = model.fit(x = input, y = output, epochs=100, batch_size=25)
        # plt.plot(fit_result.history["loss"], label = "train")


        model.save("refresh")
        model_ex = keras.models.load_model("refresh")
        # check(self.file_female_russian_names,Decoder(model_ex.predict(input), self.dict_ru))
        arr = []
        out_put = [open(file='russian_last_names_male.txt', errors='ignore'),
                   open(file='russian_names_male.txt', errors='ignore'),
                   open(file='russian_names_female.txt', errors='ignore'),
                   open(file='russian_last_names_female.txt', encoding='utf-8', errors='ignore')]
        for i in out_put:
            for j in i:
                arr.append(j)
        check(arr, Decoder(model_ex.predict(np.array(self.common_input[:5])), self.dict_ru))
        ans(model_ex.predict(self.common_input[:5]))

def ans(arr):
    for i in arr:
        for j in i:
            print(Cail(j), end = ' ')
        print()
        print()

if __name__ == '__main__':
    dict_ru = {'А':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5],
'Б':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 1.0],
'В':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 0.5],
'Г':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0],
'Д':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 0.5, 0.5],
'Е':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0],
'Ж':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 1.0, 0.5],
'З':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0],
'И':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, 0.5],
'Й':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, 1.0],
'К':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 0.5, 1.0, 0.5],
'Л':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 0.5, 1.0, 1.0],
'М':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 0.5, 0.5],
'Н':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 0.5, 1.0],
'О':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 0.5],
'П':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
'Р':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5],
'С':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 1.0],
'Т':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 1.0, 0.5],
'У':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 1.0, 1.0],
'Ф':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 0.5, 0.5],
'Х':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 0.5, 1.0],
'Ц':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0, 0.5],
'Ч':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0],
'Ш':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5],
'Щ':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 0.5, 0.5, 1.0],
'Ъ':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 0.5],
'Ы':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 1.0],
'Ь':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 1.0, 0.5, 0.5],
'Э':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 1.0, 0.5, 1.0],
'Ю':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0, 0.5],
'Я':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0],
'Ё':[1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1]}
    dict_eng = {'A':[1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0],
'B':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5],
'C':[1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0],
'D':[1.0, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5],
'E':[1.0, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0],
'F':[1.0, 0.5, 0.5, 0.5, 1.0, 1.0, 0.5],
'G':[1.0, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0],
'H':[1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5],
'I':[1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0],
'J':[1.0, 0.5, 0.5, 1.0, 0.5, 1.0, 0.5],
'K':[1.0, 0.5, 0.5, 1.0, 0.5, 1.0, 1.0],
'L':[1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5],
'M':[1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 1.0],
'N':[1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 0.5],
'O':[1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0],
'P':[1.0, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5],
'Q':[1.0, 0.5, 1.0, 0.5, 0.5, 0.5, 1.0],
'R':[1.0, 0.5, 1.0, 0.5, 0.5, 1.0, 0.5],
'S':[1.0, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0],
'T':[1.0, 0.5, 1.0, 0.5, 1.0, 0.5, 0.5],
'U':[1.0, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0],
'V':[1.0, 0.5, 1.0, 0.5, 1.0, 1.0, 0.5],
'W':[1.0, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0],
'X':[1.0, 0.5, 1.0, 1.0, 0.5, 0.5, 0.5],
'Y':[1.0, 0.5, 1.0, 1.0, 0.5, 0.5, 1.0],
'Z':[1.0, 0.5, 1.0, 1.0, 0.5, 1.0, 0.5],
'\'':[1, 0.5, 0.5, 1, 1, 1]}
    #
    # data = DataSet_method(dict_ru=dict_ru, dict_eng = dict_eng)
    # # data.Neroset()
    # data.check()
    #

