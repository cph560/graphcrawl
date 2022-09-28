from re import I
import requests

import os
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions

import concurrent.futures
import chromedriver_autoinstaller as chromedriver



def get_data():
    option = ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    browser=Chrome(options=option)
    mainw='https://e-hentai.org/g/2335475/65110d4f5e/'
    browser.get(mainw)
    xp='/html/body/div[4]/table/tbody/tr/td/a'
    webs=browser.find_elements(by='xpath', value=xp)
    nums=[]
    for element in webs:
        if element.text != ">":
        
            nums.append(int(element.text) )
    huge_urls_set=[ f'{mainw}'+f'?p={i}' for i in range(max(nums))]
    
    
    return huge_urls_set

def download(url):
    option = ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')

    web_data=[]
    
    
    Xpath='//*[@id="gdt"]/div/div/a'
    browser=Chrome(options=option)
    browser.get(url)

    res=browser.find_elements(by='xpath', value=Xpath)
    web_data+=[element.get_attribute('href') for element in res]

    get_graph(web_data)


def get_graph(web):
    j=0
    for i in web:
        try:
            kei=i.split('/')
            content=kei[-1]
            option = ChromeOptions()
            option.add_argument('--headless')
            url=i
            Xpath='//*[@id="img"]'
            browser=Chrome(options=option)
            browser.get(url)

            res=browser.find_elements(by='xpath', value=Xpath)
            
            src=res[0].get_attribute('src')
            print('downloading....%s : NO.%s' % (content,str(j)))
            r = requests.get(src)
            with open(f'./image/{content}.jpg', 'wb') as f:
                f.write(r.content)   
            j+= 1
        except:
            print(f'Error at {kei[-1]}')

    print('Download Complete')


def remove_file(old_path, new_path):

    filelist = os.listdir(old_path) #列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    
    for file in filelist:
        
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)

        shutil.move(src, dst)
    print('Copy complete')


def download_all_images(huge_urls_set):
    
    
    works = len(huge_urls_set)
    with concurrent.futures.ThreadPoolExecutor(works) as exector:
        for url in huge_urls_set:
            exector.submit(download,url)

if __name__ == '__main__':
    chromedriver.install()
    old_path='./image'
    folder_name='The Goblin'
    new_path=f"D:/BaiduNetdiskDownload/manca/Artist/{folder_name}"
    if not os.path.exists(new_path):
    
        os.makedirs(new_path)
    if not os.path.exists('./image'):
    
        os.makedirs('./image')
    data=get_data()
    
    download_all_images(data)

    remove_file(old_path, new_path)

    