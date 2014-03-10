#coding=UTF-8
#*********************************
#  Author: hanker
#   Email: hanpeiyi1@gmail.com
#*********************************
"""
网络爬虫
"""

import sys
import time, urllib, urllib2
import argparse
import workerthreading
import re,os

def init():
	#获取命令行参数
	newParser = argparse.ArgumentParser()
	newParser.add_argument("-u","--url", dest = "url", help = "target url")
	newParser.add_argument("-n","--thread", type=int, dest = "thread", help = "thread pool(default: 10)")
	newParser.add_argument("-i","--image", type=int, dest = "image", help = "the number of image")
	newParser.add_argument("-o","--output path", dest = "path", help = "output path (default: /pics)")
	args = newParser.parse_args()
	argsDict = args.__dict__
	
	#图片网址
	url = ""
	if argsDict["url"] == None:
		print "Please input parsement,for example: python spider.py -u http://www.baidu.com"
		return 
	else:	
		url = argsDict["url"]
	
	#线程数目
	threadNum = 10
	if	argsDict["thread"] != None:
		threadNum = argsDict["thread"]

	#下载图片数目
	imgNum = 100000
	if argsDict["image"] != None:
		imgNum = argsDict["image"]
	
	#下载文件路径
	outfile = "pics/"
	if argsDict["path"] != None:
		outfile = argsDict["path"]
	
	return url, threadNum, imgNum, outfile

"""
抓取网页的链接地址
"""
def get_url(url):

	try:
		content = urllib2.urlopen(url,None,5).read()
		urls = re.findall('<a href=\\"(/.*?)\\".*?',content)
		list = []
		for u in urls:
			u = url + u
			list.append(u)	
		return list
	except urllib2.URLError,e:
		print "url=",url,"exception=",str(e)
	except urllib2.HTTPError,e:
		print "url=",url,"exception=",str(e)

"""
下载网页的照片	
"""
def getimage(url,outfile,imgNum):

	global imgScanNum
	try:
		content = urllib2.urlopen(url,None,5).read()
		images = re.findall('<img .*? src=\\"(\S+?\.jpg)\\".*?>',content)
	except urllib2.URLError,e:
		print "url=",url,"exception=",str(e)
	except urllib2.HTTPError,e:
		print "url=",url,"exception=",str(e)
	
	if os.path.exists(outfile):
		for img in images:
			if imgScanNum >= imgNum:
				return 
			print "Download: %s" %img
			imgname = img.split("/")
			imgname = '_'.join(imgname[2:])
			filename = outfile + imgname
			urllib.urlretrieve(img,filename,None)
			imgScanNum += 1
			print "IMG",imgScanNum,imgname
	else:
		print outfile,"is not exists."
"""
网络爬虫主函数
"""
def download():

	global imgScanNum
	#初始化
	url, threadNum, imgNum, outfile = init()
	print '.....Start spidering.....'
	url_list1 = []										#初始任务
	url_list2 = []										#任务队列
	url_list1.append(url)
	#爬虫过程
	while len(url_list1) and imgScanNum <= imgNum:
		url_list3 = []									#处理队列
		url_list2 = url_list1
		url_list1 = []
		
		url_list2_num = len(url_list2)
		for i in range(url_list2_num):
			url_list3.append(url_list2.pop())
			if i == (url_list2_num - 1):
				threadpool = workerthreading.WorkerManager(threadNum)
				for j in range(len(url_list3)):
					url = url_list3.pop()
					threadpool.add_job(get_url,url)		#向工作队列中添加工作
				threadpool.wait_for_complete()
				result_queue =	threadpool.get_result()
				while result_queue.empty() != True and imgScanNum < imgNum:		#取出结果队列执行工作
					urllist = result_queue.get()
					if urllist == None:
						continue
					for url in urllist:
						url_list1.append(url)
						getimage(url,outfile,imgNum)
						if imgScanNum >= imgNum:
							break
	print 'The spider has downloaded about',imgScanNum,'images.'
	print '.....End Spidering.....'

imgScanNum = 0
"""
开始下载
"""
download()
