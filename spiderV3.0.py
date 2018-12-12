# -*- coding: utf-8 -*-
import requests
import os
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
            'Referer': "http://www.mmjpg.com"}

class Spider(object):
    def __init__(self,page_count, girl_count, pic_count):
        self.page_count = page_count
        self.girl_count = girl_count
        self.pic_count = pic_count
        self.page_urls = ['http://www.mmjpg.com/']
        self.girl_urls = []
        self.girl_name = ''
        self.pic_urls = []

    #获取页面url
    def get_page_urls(self):
        if int(self.page_count) > 1:
            for n in range(2, int(self.page_count)+1):
                page_url = 'http://www.mmjpg.com/home/' + str(n)
                self.page_urls.append(page_url)
        elif int(self.page_count) == 1:
            pass

        # print(self.page_urls)

    #获取图片集url
    def get_girl_urls(self):
        for page_url in self.page_urls:
            html = requests.get(page_url)
            selector = etree.HTML(html.content)
            # self.girl_urls.append(selector.xpath('//div[@class="pic"]/ul/li/a/@href'))
            self.girl_urls += selector.xpath('//div[@class="pic"]/ul/li/a/@href')            #返回多个列表，用+=拼接
        # self.girl_urls = self.girl_urls[:self.girl_count]
        # print(self.girl_urls[:self.girl_count])

    #获取图片url
    def get_pic_urls(self):
        for girl_url in self.girl_urls[:self.girl_count]:
            html = requests.get(girl_url)
            selector = etree.HTML(html.content)
            page_num = selector.xpath('//*[@id="page"]/a[last()-1]/text()')[0]               #获取页数

            if int(self.pic_count) < int(page_num):
                page_num = self.pic_count

            page_num = int(page_num)
            self.girl_name = selector.xpath('//div[@class="article"]/h2/text()')[0]          #有[0]返回字符串

            self.mk_pic_path()

            self.pic_urls = []
            #分别获取每一页图片url
            for i in range(1, page_num+1):
                girl_pic_url = girl_url + '/' + str(i) 
                # girl_pic_url = ''.join([girl_url, '/' + str(i)])
                html = requests.get(girl_pic_url)
                selector = etree.HTML(html.content)
                pic_url = selector.xpath('//div[@class="content"]/a/img/@src')[0]
                self.pic_urls.append(pic_url)
          
            # print(self.pic_urls)

            try:
                self.download_pic()
                # pass
            except Exception as e:
                print("保存失败" + str(e))
            


    def mk_pic_path(self):
        if not os.path.exists('pictures'):
            os.mkdir('pictures')
        global pictures_path
        pictures_path = os.path.join(os.getcwd(), 'pictures/')

        try:
            os.mkdir(pictures_path)
        except:
            pass
        
        global girl_path
        girl_path = pictures_path + self.girl_name

        try:
            os.mkdir(girl_path)
        except Exception as e:
            print("“{}”目录已存在".format(self.girl_name))


    def download_pic(self):
        img_name = 1
        for pic_url in self.pic_urls:
            img_data = requests.get(pic_url, headers=headers)
            pic_path = girl_path + '/' + str(img_name)+'.jpg'
            if os.path.isfile(pic_path):
                print("{}第{}张已存在".format(self.girl_name, img_name))
                pass
            else:
                with open(pic_path, 'wb') as f:
                    f.write(img_data.content)
                    print("正在保存{}第{}张".format(self.girl_name, img_name))
                    f.close()
            img_name += 1


    def start(self):
        self.get_page_urls()
        self.get_girl_urls()
        self.get_pic_urls()

if __name__ == '__main__':
    page_count = input("请输入需要下载的页数(每页有十五个美女）：")
    girl_count = input("请输入需要下载美女的个数：")
    pic_count = input("请输入需要下载每个女孩照片的张数：")
    page_count = int(page_count)
    girl_count = int(girl_count)
    pic_count = int(pic_count)
    spider = Spider(page_count,girl_count,pic_count)
    spider.start()

