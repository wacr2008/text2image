#coding=utf-8
'''
Created on 2017年4月6日

@author: lenovo
'''
#######
#   
#
########
from bs4 import BeautifulSoup
import re
import sys,time
import urllib
from urllib.request import urlopen,urlretrieve
from urllib.parse import urlencode


def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    sys.stdout.write("\r%6.2f%%"% percent)
    sys.stdout.flush()


if __name__ == "__main__":
    
    BaseUrl = "http://pinyin.sogou.com"
    HomePageUrl = "http://pinyin.sogou.com/dict/"
    html = urlopen(HomePageUrl).read()
    
    soup = BeautifulSoup(html,"html.parser")
    soup =  soup.find(id="dict_category_show").find_all('div',class_='dict_category_list')
    
    fc = 0
    sc = 0
    tc = 0
    for ii in soup:
        fc+=1
        print("Level 1 :" + ii.find(class_='dict_category_list_title').find('a').contents[0])
        for k in ii.find(class_='catewords').find_all('a'):
            secondclass = k.contents[0]
            secondUrl = BaseUrl+"%s" % (k['href'])
            print( " " * 4 + "Level 2 :" + secondclass+ " " * 8 + secondUrl) 
            sc += 1
            
            soup2 = BeautifulSoup(urlopen(secondUrl).read(),"html.parser",from_encoding="utf8")
             
            totalpagenum = soup2.find(id='dict_page_list').find('ul').find_all('span')[-2].a.contents[0]
            
            for pageind in range(1, int(totalpagenum)+1):
                
                soup2 = BeautifulSoup(urlopen( "%s/default/%d" %  (secondUrl.replace("?rf=dictindex",""),pageind)  ).read(),"html.parser",from_encoding="utf8")
                for kk in soup2.find_all('div', class_='dict_detail_block') :
                    thirdclass = kk.find(class_='detail_title').find('a').contents[0]
                    thirdUrl = kk.find(class_='dict_dl_btn').a['href'] 
                    
                    
                    print( " " * 8 + "Level 3 :" + thirdclass + " " * 10 + "Downloading.....")
                    tc += 1 
                    urlretrieve(thirdUrl, "%s-%s.scel" % (secondclass,thirdclass),callbackfunc)
    print("Total :%d, %d, %d" % (fc, sc, tc))