# -*- coding: utf-8 -*-
import requests
import os
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
			'Referer': "https://bb.br8.club/thread0806.php?fid=16"}
root_url = 'https://bb.br8.club/'

class Spider(object):
	def __init__(self,page_count, topic_count, pic_count):
		self.page_count = page_count
		self.topic_count = topic_count
		self.pic_count = pic_count
		self.page_urls = []
		self.topic_urls = []
		self.topic_name = []
		self.pic_urls = []

	#获取每个页面的url
	def get_page_urls(self):
		for n in range(1, int(self.page_count)+1):
			page_url = root_url + 'thread0806.php?fid=16&search=&page=' + str(n)
			self.page_urls.append(page_url)

		# print(self.page_urls)

	def get_topic_urls(self):
		for page_url in self.page_urls:
			html = requests.get(page_url)
			selector = etree.HTML(html.content)
			self.topic_urls += selector.xpath('//*[@id="ajaxtable"]//tr/td[2]/h3/a/@href')
		
		#前9个帖子无图，删除
		for i in range(9):			
			del self.topic_urls[0]

		for i in range(len(self.topic_urls)):
			self.topic_urls[i] = root_url + self.topic_urls[i]

		# self.topic_urls = self.topic_urls[:self.topic_count]

		# print(self.topic_urls)

	def get_pic_urls(self):
		for topic_url in self.topic_urls[:self.topic_count]:
			html = requests.get(topic_url)
			selector = etree.HTML(html.content)
			self.pic_urls = selector.xpath('//*[@id="main"]/div[3]/table/tr[1]/th[2]/table/tr/td/div[4]/input/@data-src')
			global pic_num
			pic_num = len(self.pic_urls)

			if int(self.pic_count) < int(pic_num):
				pic_num = self.pic_count
			pic_num = int(pic_num)

			self.topic_name = selector.xpath('//div[@id="main"]/div/table/tr/th[2]/table/tr/td/h4/text()')[0]
			#tbody是浏览器规范化额外加上去的标签，实际的网页源码并没有
			#所以使用xpath时需要省略tbody

			# print(self.pic_urls[9])

			self.mk_pic_path()

			try:
				self.download_pic()
			except Exception as e:
				print("保存失败" + str(e))



	def mk_pic_path(self):
		if not os.path.exists('1024'):
			os.mkdir('1024')
		global root_path
		root_path = os.path.join(os.getcwd(), '1024/')

		try:
			os.mkdir(root_path)
		except:
			pass
		
		global topic_path
		topic_path = root_path + self.topic_name

		try:
			os.mkdir(topic_path)
		except Exception as e:
			print("{}目录已存在".format(self.topic_name))


	def download_pic(self):
		img_name = 1
		for pic_url in self.pic_urls[:pic_num]:						#选择下载图片数量,
			img_data = requests.get(pic_url, headers=headers)
			pic_path = topic_path + '/' + str(img_name)+'.jpg'
			if os.path.isfile(pic_path):
				print("{}第{}张已存在".format(self.topic_name, img_name))
				pass
			else:
				with open(pic_path, 'wb') as f:
					f.write(img_data.content)
					print("正在保存{}第{}张".format(self.topic_name, img_name))
					f.close()
			img_name += 1


	def start(self):
		self.get_page_urls()
		self.get_topic_urls()
		self.get_pic_urls()

if __name__ == '__main__':
	page_count = input("请输入需要下载的页数：")
	topic_count = input("请输入需要下载帖子的个数：")
	pic_count = input("请输入需要下载每个帖子照片的张数：")
	page_count = int(page_count)
	topic_count = int(topic_count)
	pic_count = int(pic_count)
	spider = Spider(page_count,topic_count,pic_count) #页数，帖子数,每个帖子下载图片数量
	spider.start()
