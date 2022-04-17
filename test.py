from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = 'http://translit-online.ru/'
browser = webdriver.Chrome(executable_path="D:\\translit\chromedriver.exe")
file = open("russian_names_female.txt")
file2 = open("female_names_data.txt",'w')
arr = []
for i in file:
    try:
        browser.get(url)
        browser.find_element(By.XPATH, '/html/body/div/div[3]/form/textarea[1]').send_keys(i)
        browser.find_element(By.XPATH, '/html/body/div/div[3]/form/div[2]/div/input[1]').click()
        info = browser.find_element(By.XPATH, '/html/body/div/div[3]/form/textarea[2]').text
        time.sleep(2)
        print(info)
        arr.append(str(info) + '\n')
        print(arr)
    except:
        print('oops')
for i in arr:
    file2.write(i)
