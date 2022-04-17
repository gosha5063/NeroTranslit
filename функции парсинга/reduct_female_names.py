with open('russian_names_female.txt') as file:
    arr = []
    for i in file:
        note = file.readline()
        try:
            arr.append(str(note).split()[0]+ '\n')
        except:
            arr.append(str(note) + '\n')
    print(arr, len(arr))
file = open('russian_names_female.txt','w')
for i in arr:
    file.write(i)