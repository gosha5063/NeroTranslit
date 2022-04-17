import requests
from bs4 import BeautifulSoup

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
common_url = 'https://imena-znachenie.ru/familii/russkie/muzhskie/'

arr = []
for i in range(125):
    if i == 0:
        url = common_url
    else:
        url = common_url + '?PAGEN_1=' + str(i+1)
        print(url)
    request = requests.get(url, headers=headers)
    soap = BeautifulSoup(request.text, 'html.parser').find('div', class_ = 'columns3')
    for i in soap.find_all('p', class_='news-item'):
        try:
            arr.append(i.find('a').text)
        except:
            pass
file = open('russian_last_names_male.txt','w')
for i in arr:
    file.write(i + '\n')
file.close()