#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: luozaibo
# date : 2019-08-15 20:46:31
import requests
from lxml import etree
import aiohttp
from pprint import pprint
from fake_useragent import UserAgent
import asyncio
import time
import re
import json
from pathlib import Path
from multiprocessing import Pool
from urllib.parse import quote

def get_onepage_urls(url, keyword):
    headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'referer': f'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&istype=2&ie=utf-8&word={quote(keyword)}&oq={quote(keyword)}&rsp=-1'
            }
    response = requests.get(url, headers=headers)
    item = response.json()
    listNum = item['listNum']
    urls = item['data'][:30]
    urls = [i['objURL'] for i in urls]
    urls = [decode_url(url) for url in urls]
    return listNum, urls

def decode_url(obj_url):
    intab = '0123456789abcdefghijklmnopqrstuvw'
    outab = '7dgjmoru140852vsnkheb963wtqplifca'
    trans = obj_url.maketrans(intab, outab)
    str_tab = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
    for k, v in str_tab.items():
        obj_url = obj_url.replace(k, v)
    url = obj_url.translate(trans)
    return url

def download_img(url, i, keyword):
    headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'referer': f'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&istype=2&ie=utf-8&word={quote(keyword)}&oq={quote(keyword)}&rsp=-1'
            }
    try:
        time.sleep(1)
        response = requests.get(url, headers=headers, timeout=3)
        content = response.content
        name = url.split('/')[-1]
        with open(f'./Pic/{keyword}/{i}_{name}', 'wb') as f:
            f.write(content)
    except:
        print(f'error--       {url}')

    

def main(keyword):
    offset = 0
    total_page = 0
    pool = Pool(8)
    while offset*30 <= 40:
        # url = f'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ie=utf-8&word={quote(keyword)}&pn={offset*30}'
        url = f'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ie=utf-8&word={quote(keyword)}&pn={offset*30}&width=1920&height=1080'
        listNum, urls = get_onepage_urls(url, keyword)
        for i,url in enumerate(urls):
            pool.apply_async(download_img, (url,i,keyword))
        offset += 1
    pool.close()
    pool.join()


if __name__ == '__main__':
    t0 = time.time()
    keyword_list = input('input keyword: ').split()
    for keyword in keyword_list:
        Path(f'./Pic/{keyword}').mkdir(parents=True, exist_ok=True)
        main(keyword)
    print(time.time() - t0)
