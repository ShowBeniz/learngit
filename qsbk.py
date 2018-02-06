#!usr/bin/python
#_*_ coding:utf-8 _*_

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import urllib2
import re
import thread
import time

#糗事百科爬虫类
class QSBK:

	#初始化方法，定义一些变量
	def __init__(self):
		self.pageIndex = 1
		#初始化headers
		self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'
		self.headers = {'User-Agent':self.user_agent}
		#存放段子的变量
		self.stories = []
		#存放程序是否继续运行的变量
		self.enable = False


	#传入某一页面的索引，获得页面代码
	def getPage(self,pageIndex):
		try:
			#pageIndex = self.pageIndex
			url = 'http://www.qiushibaike.com/hot/page/' + str(self.pageIndex)
			#构建Request
			req = urllib2.Request(url,headers=self.headers)
			#获取页面代码
			response = urllib2.urlopen(req)
			#将代码转化为utf-8编码
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print u"连接糗事百科失败，错误原因", e.reason
				return None


    #传入某一页的代码，返回本页不带图片的段子列表
	def getPageItems(self,pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print("页面加载失败......")
			return None

		#pattern = re.compile('<div.*?author.*?>.*?<a href.*?><h2>(.*?)</h2>.*?'+
		#	'content">(.*?)<!--(.*?)--><div(.*?)<div class="stats".*?class="number">(.*?)</i>',re.S)
		pattern = re.compile('<div class="article.*?<h2>(.*?)</h2>.*?content".*?<span>(.*?)</span>.*?<!--(.*?)-->(.*?)</div>.*?class="number">(.*?)</i>',re.S)
		items = re.findall(pattern,pageCode)
		#用来存储每页的段子们
		pageStories = []
		#遍历正则表达式匹配的信息，并进行存储
		for item in items:
			#是否含有图片
			haveImg = re.search("img",item[3])
			#如果不含有图片，加入到列表中
			if not haveImg:
				replaceBR = re.compile('<br/>')
				text = re.sub(replaceBR,"\n",item[1])
				#item[0]是发布者，item[1]是发布内容，item[2]和[3]是图片，item[4]是点赞数
				story = {'发布人':item[0].strip(),'发布内容':text.strip(),'点赞数':item[4].strip()}
				pageStories.append(story)
		return pageStories


	#加载并提取页面的内容，并加入到列表中
	def loadPage(self):
		#如果队列中剩下的段子数只剩一个，则加载新的一页
		if self.enable == True:
			if len(self.stories) < 2:
				#获取新的一页
				pageStories = self.getPageItems(self.pageIndex)
				#将该页的段子存到全局列表中
				if pageStories:
					self.stories.append(pageStories)
					#下次读取下一页
					self.pageIndex += 1


	#调用该方法，每次敲回车，打印输出一个段子
	def getOneStory(self,pageStories,page):
		#遍历一页的段子
		for story in pageStories:
			#等待用户输入
			input = raw_input()
			#每当输入回车一次，判断一次是否需要加载新页面
			self.loadPage()
			#如果输入Q，程序结束
			if input == 'q':
				self.enable = False
				return
			
			print("\n第" + str(page) + "页")
			print("\n发布者：" + story['发布人'])
			print("\n发布内容：" + story['发布内容'])
			print("\n点赞数：" + story['点赞数'])
			#print u"第%d页\t发布人:%s\t发布内容%s\t点赞数%s\n%s" %(page,story[0],story[1],story[2])


	#开始方法
	def start(self):
		print("正在读取糗事百科段子，按回车查看新段子，按q退出")
		#使变量变成True，可以正常运行程序
		self.enable = True
		#先加载一页内容
		self.loadPage()
		#局部变量，控制当前读到了第几页
		nowPage = 0
		while self.enable:
			if len(self.stories) > 0:
				#从全局list中获取一页的段子
				pageStories = self.stories[0]
				#当前读到的页数加1
				nowPage += 1
				#将全局list中第一个元素删除，因为已经取出
				del self.stories[0]
				#输出该页的段子
				self.getOneStory(pageStories,nowPage)


spider = QSBK()
spider.start()
