import requests
from bs4 import BeautifulSoup



url = 'https://kto-chto-gde.ru/names/female/'

request = requests.get(url)
soap = BeautifulSoup(request.text, 'html.parser')

arr = []
for i in soap.find_all('ul',class_ = 'list-name'):
    for j in i.find_all('li', class_ = 'list-name__item'):
        arr.append(i.text)

print(arr, type(arr))
with open('russian_names_female.txt', 'w', encoding="utf-8") as f:
    for i in arr:
        f.write(i)

