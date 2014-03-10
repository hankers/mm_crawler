1.概述
抓取美女图片的爬虫程序

2.实现思路
  
  线程池模块
  
  WorkManager类   线程池管理者类
  Work类		  线程类
  使用WorkManager制定任务量和线程数，线程池中的每个线程从任务队列中获取任务并执行，直到其任务队列中没有任务
  线程池的使用可实现重复利用线程来执行任务，减少系统资源开销。
  
  爬虫模块
  1.使用正则匹配实现一个网页上所有网页链接和所有美女图片链接的获取
  2.爬虫过程采用BFS算法实现美女图片搜集过程
	给定目标网址
	线程的工作队列用于存储即将爬取其所有网址链接的网址
	线程的结果队列用于存储工作队列中得到的网址链接结果
	取出结果队列中网址依次爬取其上所有美女图片

3.使用说明

  usage: spider.py [-h] [-u URL] [-n THREAD] [-l IMAGE] [-o PATH]

  optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     target url
  -n THREAD, --thread THREAD
		                thread pool(default: 10)
  -i IMAGE, --image IMAGE
	                    the number of image
  -o PATH, --output path PATH
					    output path (default: /pics)
  实例： python spider.py -u http://22mm.cc -n 15 -i 100 
