import requests
from bs4 import BeautifulSoup

url = 'https://imenika.ru/guys/all'
request = requests.get(url)
soap = BeautifulSoup(request.text, 'html.parser').find('div', class_ = 'main_txt')

arr = []
for i in soap.find_all('ul'):
    for j in i.find_all('li'):
        try:
            arr.append(j.find('span',class_ = 'r4').text)
        except:
            print("t")



url ='https://ru.wikipedia.org/wiki/Список_имён_славянского_происхождения'
request = requests.get(url)
soup = BeautifulSoup(request.text, 'html.parser')
li_find = soup.find('div', class_='mw-parser-output').find_all('ul')[2:]
arr2 = []
for i in li_find:
    for j in i.find_all('li'):
        try:
            arr2.append(j.find('a').text)
        except:
            pass
arr2 = arr2[:432]
for i in range(len(arr)):
    arr2.append(arr[i])
arr2=sorted(arr2)
file = open("russian_names_male.txt", 'w')
for i in arr2:
    file.write(i + '\n')
