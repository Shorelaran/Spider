import re
from multiprocessing import Pool
from urllib.parse import urlencode
import urllib.request
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import json
import os

GirlName = []
GirlCity = []
GirlId   = []
GirlUrl  = []
GirlHeight = []
GirlWeight = []

OutputDir = 'E:/tbmodlephoto/'
url_id = 'https://mm.taobao.com/self/aiShow.htm?spm=719.7763510.1998643336.1.dLKjVy&userId='

def get_page_index(index):
	data = {
		'q': '',
		'viewFlag': 'A',
		'sortType': 'default',
		'searchStyle': '',
		'searchRegion': 'city',
		'searchFansNum': '',
		'currentPage': index,
		'pageSize': '100'
	}
	page_url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8' + urlencode(data)
	return page_url

def get_page_detail(url):
	try:
		res = requests.get(url)
		if res.status_code == 200:
			return res.text
		return None
	except RequestException:
		print('请求详情页出错')
		return None

def get_girl_info(html):
	data = json.loads(html)
	if data and 'data' in data.keys():
		data_item =  data.get('data')
		for item in data_item.get('searchDOList'):
			GirlName.append(item.get('realName'))
			GirlCity.append(item.get('city'))
			GirlId.append(str(item.get('userId')))
			GirlHeight.append(item.get('height'))
			GirlWeight.append(item.get('weight'))

def mkdir(path):
	isExists = os.path.exists(path)
	if not isExists:
		os.makedirs(path)
		print('    创建文件夹' + path + '成功')
		return True
	else:
		return False

def download(path, url):
	html = get_page_detail(url)
	soup = BeautifulSoup(html, 'html.parser')
	imgs = soup.find_all("img", {"src": re.compile(".*\.jpg")})
	for i, img in enumerate(imgs[1:2]):
		try:
			html = urllib.request.urlopen('https:' + img['src'])
			data = html.read()
			file_name = "{}/{}.jpg".format(path, i + 1)
			if os.path.exists(file_name):
				print('    已经存在', img)
			else:
				with open(file_name, 'wb') as f:
					print('    正在下载', img)
					f.write(data)
		except Exception:
			print("    地址错误!")

def main(index):
	page_url = get_page_index(index)
	html = get_page_detail(page_url)
	get_girl_info(html)
	GirlUrl = [(url_id + i) for i in GirlId]
	GirlsInfo = zip(GirlName, GirlCity, GirlWeight, GirlHeight, GirlUrl)
	for Name, City, Weight, Height, Url in GirlsInfo:
		print('Girl:',Name, Height + '/' + Weight)
		path = OutputDir + Name + ' ' + City
		mkdir(path)
		print('    开始下载......')
		download(path, Url)
		print('    下载完成......')

GROUP_START = 1
GROUP_END   = 1

if __name__ == '__main__':
	# group = [x for x in range(GROUP_START, GROUP_END + 1)]
	# pool = Pool()
	# pool.map(main, group)
	main(1)