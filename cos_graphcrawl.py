from re import I
import requests
import sys
import os
import shutil
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import threading
import concurrent.futures
import chromedriver_autoinstaller as chromedriver




def get_data(web):
    option = ChromeOptions()
    # option.add_argument('--headless')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    browser = Chrome(options=option)
    huge_urls_set = []
    webs = []

    while not webs:
        try:
            browser.get(web)
            xp = '//*[@id="paginator"]/span/a'
            element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, xp)))
            webs = browser.find_elements(by='xpath', value=xp)
            
            browser.execute_script("window.stop();")
        except:
            continue
    
    huge_urls_set = []
    nums=[]
    for element in webs:
        
        try:
            nums.append(int(element.text) )
        except:
            continue
        
    huge_urls_set += [f'{web[:-2]}'+f'{i}' for i in range(1, max(nums)+1)]
    print(huge_urls_set)
    return huge_urls_set

def get_graph(web):
    j=0
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    for i in web:
        try:
            kei=i.split('/')
            content=kei[-1]
            option = ChromeOptions()
            option.add_argument('--headless')

            
            print('downloading....%s : NO.%s' % (content,str(j)))
            r = requests.get(url=i, headers=headers).content
            with open(f'./image/{content}', 'wb') as f:
                f.write(r)   
            j+= 1
        except:
            print(f'Error at {kei[-1]}')

    print('Partial Download Complete')

def Download(url):
    option = ChromeOptions()
    # option.add_argument('--headless')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')

    web_data=[]
    res = []
    browser=Chrome(options=option)

    
    while not res:
        try:
            browser.get(url)
            xp = '//*[@id="display_image_detail"]/div/a[1]/img'
            element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, xp)))
            res = browser.find_elements(by='xpath', value=xp)

            
            browser.execute_script("window.stop();")
        except:
            continue

    
    web_data = [element.get_attribute('src') for element in res]
    
    get_graph(web_data)


def remove_file(old_path, new_path, partial):

    filelist = os.listdir(old_path) #列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    
    for file in filelist:
        
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)

        shutil.move(src, dst)
    print(partial+'Copy complete')

def download_all_images(huge_urls_set):
    
    
    works = len(huge_urls_set)
    with concurrent.futures.ThreadPoolExecutor(works) as exector:
        for url in huge_urls_set:
            exector.submit(Download, url)


if __name__ == '__main__':
    chromedriver.install()
    old_path='./image'
    web_url = []
    folder_name=[]

    
    for num in range(len(web_url)):
        new_path=f"D:/BaiduNetdiskDownload/manca/cosplay/{folder_name[num]}"

        if not os.path.exists(new_path):

            os.makedirs(new_path)
        if not os.path.exists('./image'):

            os.makedirs('./image')
        data = get_data(web_url[num])

        download_all_images(data)

        remove_file(old_path, new_path, f'{num+1}/{len(web_url)}')

