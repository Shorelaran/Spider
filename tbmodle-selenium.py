import os
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
homePage = 'https://mm.taobao.com/search_tstar_model.htm?'
outputDir = 'E:/a/'
parser = 'html5lib'

def main():
	driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
	driver.set_window_size(1400, 900)
	driver.get(homePage)
	soup = BeautifulSoup(driver.page_source, parser)
	print("GET Page")
	GirlsList = driver.find_element_by_id('J_GirlsList').text.split('\n')
	imagesUrl = re.findall('\/\/gtd\.alicdn\.com\/sns_logo.*\.jpg', driver.page_source)
	girlsUrl = soup.find_all("a", {"href": re.compile("\/\/.*\.htm\?(userId=)\d*")})
	girlsNL = GirlsList[::3]
	girlsHW = GirlsList[1::3]
	girlsHURL = [('http:' + i['href']) for i in girlsUrl]
	girlsPhotoURL = [('https:' + i) for i in imagesUrl]
	girlsInfo = zip(girlsNL, girlsHW, girlsHURL, girlsPhotoURL)
	for girlNL, girlHW, girlHURL, girlCover in girlsInfo:
		print("Girl :", girlNL, girlHW)
		mkdir(outputDir + girlNL)
		print("    saving...")
		data = urlopen(girlCover).read()
		with open(outputDir + girlNL + '/cover.jpg', 'wb') as f:
			f.write(data)
		print("    Loading Cover... ")
		getImgs(girlHURL, outputDir + girlNL)
	driver.close()

def mkdir(path):
	isExists = os.path.exists(path)
	if not isExists:
		print("    新建文件夹", path)
		os.makedirs(path)
	else:
		print('    文件夹', path, '已创建')

def getImgs(url, path):
	driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
	driver.get(url)
	print("    Opening...")
	soup = BeautifulSoup(driver.page_source, parser)
	imgs = soup.find_all("img", {"src": re.compile(".*\.jpg")})
	for i, img in enumerate(imgs[1:]):
		try:
			html = urlopen('https:' + img['src'])
			data = html.read()
			fileName = "{}/{}.jpg".format(path, i + 1)
			print("    Loading...", fileName)
			with open(fileName, 'wb') as f:
				f.write(data)
		except Exception:
			print("    Address Error!")
	driver.close()

if __name__ == '__main__':
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)
	main()