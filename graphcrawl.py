
from re import I
import requests
import sys
import os
import shutil
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

from tqdm import tqdm
import concurrent.futures
import chromedriver_autoinstaller as chromedriver



def get_data(web):
    option = ChromeOptions()
    option.add_argument('--headless')
    
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    browser=Chrome(service = Service('D:/python/Scripts/chromedriver.exe'), options=option)
    huge_urls_set = []
    mainw = web
    browser.get(mainw)
    
    
    # if browser.find_element("link text", "View Gallery"):
    #     browser.find_element("link text", "View Gallery").click()
    xp='/html/body/div[4]/table/tbody/tr/td/a'
    webs = browser.find_elements(by='xpath', value=xp)
    # print(webs)
    nums=[]
    for element in webs:
        
        # 如果int错误
        try:
            nums.append(int(element.text) )
        except:
            pass
    huge_urls_set += [ f'{mainw}'+f'?p={i}' for i in range(max(nums))]
    
    return huge_urls_set

def download(url):
    option = ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')

    web_data=[]

    Xpath='//*[@id="gdt"]/div/div/a'
    browser=Chrome(service = Service('D:/python/Scripts/chromedriver.exe'), options=option)
    browser.get(url)
    # if browser.find_element("link text", "View Gallery"):
    #     browser.find_element("link text", "View Gallery").click()

    res=browser.find_elements(by='xpath', value=Xpath)
    web_data+=[element.get_attribute('href') for element in res]
    # print(web_data)
    get_graph(web_data)


def get_graph(web):
    j=0
    with tqdm(total=len(web)) as pbar:
        for i in web:
            try:
                kei=i.split('/')
                content=kei[-1]
                option = ChromeOptions()
                option.add_argument('--headless')
                option.add_argument('--ignore-certificate-errors')
                option.add_argument('--ignore-ssl-errors')
                option.add_experimental_option('excludeSwitches', ['enable-logging'])

                url=i
                Xpath='//*[@id="img"]'
                browser=Chrome(service = Service('D:/python/Scripts/chromedriver.exe'), options=option)
                browser.get(url)

                res=browser.find_elements(by='xpath', value=Xpath)
                
                src=res[0].get_attribute('src')
                print('downloading....%s : NO.%s' % (content,str(j)))
                headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
                proxies={'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}

                r = requests.get(url=src, headers=headers, verify=False, proxies=proxies)
                
                with open(f'./image/{content}.jpg', 'wb') as f:
                    f.write(r.content)   
                    pbar.update(1)
                j+= 1

            except Exception as e:
                print(f'Error:  {e}  \n at {kei[-1]}')
       
    print('Partial Download Complete')


def remove_file(old_path, new_path, partial):

    filelist = os.listdir(old_path) #列出该目录下的所有文�?,listdir返回的文件列表是不包含路径的�?
    
    for file in filelist:
        
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)

        shutil.move(src, dst)
    print(partial+'Copy complete')
    

def download_all_images(huge_urls_set):
    
    
    works = len(huge_urls_set)
    with concurrent.futures.ThreadPoolExecutor(works) as exector:
        with tqdm(total=len(huge_urls_set)) as pbar:
            for url in huge_urls_set:
                exector.submit(download, url)
                pbar.update(1)
if __name__ == '__main__':
    # chromedriver.install()
    
    Chrome(service = Service('D:/python/Scripts/chromedriver.exe'))
    # os.system('cmd /c "pip install --upgrade -r requirements.txt"')
    old_path='./image'
    web_url = ['https://e-hentai.org/g/3039905/553c9cbf33/']
    folder_name=['[井上よしひさ] 潜入!淫縛女捜査官File4']

    if len(web_url) != len(folder_name):
        print(f'length of web_url:{len(web_url)} != length of folder_name:{len(folder_name)}')
        sys.exit()
        
        
    for num in range(len(web_url)):
        new_path=f"D:/BaiduNetdiskDownload/manca/井上/{folder_name[num]}"

        if not os.path.exists(new_path):

            os.makedirs(new_path)
        if not os.path.exists('./image'):

            os.makedirs('./image')
        data=get_data(web_url[num])
        
        download_all_images(data)
        
        remove_file(old_path, new_path, f'{num+1}/{len(web_url)}')

    
