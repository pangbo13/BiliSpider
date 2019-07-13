#coding=utf-8
import requests
import time
import threading
import sys


class Spider():
	def __init__(self,rid,thread_num=2):
		self.url = 'https://api.bilibili.com/x/web-interface/newlist?rid={}&pn={}'.format(rid,'{}')
		self.rid = rid
		self.thread_num = thread_num
	#初始化函数
	def prepare(self):
		threadLock = threading.Lock()
		threads = []
		errorlist = []
		now_pages = 1
		state_dict = {}
		#生成文件名
		filename = '-'.join(map(str,tuple(time.localtime())[:5])) + '({})'.format(self.rid) + '.txt'
		#打开文件			
		file = open(filename, 'a+',encoding='utf-8')
		#输出当前时间
		file.write(time.ctime(time.time()) + '\n')
		#封装全局变量
		self.global_var ={
			'threadLock' : threadLock,
			'threads' : threads,
			'errorlist' : errorlist,
			'now_pages' : now_pages,
			'state_dict' : state_dict,
			'file' : file,
			'url' : self.url
			}
	#获取总页数函数
	def get_all_pages(self):
		print('正在获取总页数:',end='')
		try:
			res = requests.get(self.url.format(r'1&ps=1'))
			all_pages = int(res.json()['data']['page']['count']/50) + 1
			print(all_pages)
			self.global_var['all_pages'] = all_pages
		except:
			print('获取总页数失败')
			print('服务器返回内容：')
			print(res.text)
			exit()
	def start(self):
		# 创建新线程
		threads = self.global_var['threads']
		threads.append(self.MonitorThread(0, 'Monitor', self))
		for i in range(1,self.thread_num+1):
			threads.append(self.SpiderThread(i, "SThread-{}".format(i), self))
		self.get_all_pages()
		# 开启新线程
		for t in threads:
			t.start()
	#等待函数
	def wait(self):
		# 等待所有线程完成
		threads = self.global_var['threads']
		for t in threads:
			t.join()
		
	#消息处理函数
	def Info(self,threadname,type,content):
		INFO_time = time.strftime('%H:%M:%S',time.localtime())
		if type == 'INFO':
			print('[{}][ INFO][{}]{}'.format(INFO_time,threadname,content))
		if type == 'ERROR':
			print('[{}][ERROR][{}]{}'.format(INFO_time,threadname,content))
		if type == 'DEBUG':
			print('[{}][DEBUG][{}]{}'.format(INFO_time,threadname,content))	
			
	class SpiderThread (threading.Thread):
		def __init__(self, threadID, name, father):
			threading.Thread.__init__(self)
			self.threadID = threadID
			self.name = name
			self.pagesget = 0
			self.father = father
			self.father.Info(self.name,'DEBUG','线程已创建！')
		def run(self): 
			Info = self.father.Info			#转存Info函数
			#转存全局参数
			var = self.father.global_var
			all_pages = var['all_pages']
			url = var['url']
			f = var['file']
			threadLock = var['threadLock']
			Info(self.name,'DEBUG','线程已开始运行！')
			time.sleep(0.5)
			#global all_pages,now_pages,f
			while 1:
				#转存全局变量
				threadLock.acquire()
				pages = var['now_pages']
				var['now_pages'] += 1
				threadLock.release()
				#判断是否继续
				if (pages>all_pages):
					break
				Info(self.name,'INFO','正在处理第{}页'.format(pages))
				#连接服务器
				s_time = time.time()*1000
				try:
					res = requests.get(url.format(pages),timeout = 2)
				except:
					Info(self.name,'ERROR','第{}页连接超时'.format(pages))
					try:
						time.sleep(2)
						res = requests.get(url.format(pages),timeout = 10)
						Info(self.name,'ERROR','第{}页连接第二次超时'.format(pages))
						#print(self.name+'第{}页连接第二次超时'.format(pages))
					except:
						errorlist.append(pages)
						continue
				e_time = time.time()*1000
				request_time =int( e_time - s_time )
				
				s_time = time.time()*1000
				out = ''
				#解析数据
				for vinfo in res.json()['data']['archives']:
					out += 	repr(vinfo['stat']['aid']) + ','
					out +=  repr(vinfo['stat']['view']) +  ','
					out +=  repr(vinfo['stat']['danmaku']) +  ','
					out +=  repr(vinfo['stat']['reply']) +  ','
					out +=  repr(vinfo['stat']['favorite']) +  ','
					out +=  repr(vinfo['stat']['coin']) +  ','
					out +=  repr(vinfo['stat']['share']) +  ','
					out +=  repr(vinfo['stat']['like']) +  ','
					out +=  repr(vinfo['stat']['dislike']) +  '\n'
				#写入数据
				threadLock.acquire()
				f.write(out)
				threadLock.release()
				e_time = time.time()*1000
				write_time =int( e_time - s_time )
				
				Info(self.name,'DEBUG','第{}页-{}ms,{}ms'.format(pages,request_time,write_time))
				time.sleep(0.2)
				self.pagesget += 1

	class MonitorThread (threading.Thread):
		def __init__(self, threadID, name, father):
			threading.Thread.__init__(self)
			self.threadID = threadID
			self.name = name
			self.father = father
			self.father.Info(self.name,'DEBUG','线程已创建！')
		def run(self):
			var = self.father.global_var
			threads = var['threads']
			#global threads,IF_finish
			
			# while IF_finish == 0 :
				# time.sleep(3)
				# out = ''
				# for t in threads:
					# out += str(t.threadID) +'-' + str(t.pagesget) + '\t'
				# Info(self.name,'INFO',out)

##################################
if len(sys.argv) > 1:
	rid = sys.argv[1]
else :
	rid = 30
spider1 = Spider(rid)
spider1.prepare()
spider1.start()
spider1.wait()
spider1.global_var['file'].close()
#################################
# while True:
	# cmd = input('>>>')
	# exec(cmd)
#################################	

# #处理错误
# for pages in errorlist:
	# try:
		# res = requests.get('https://api.bilibili.com/x/web-interface/newlist?rid=30&pn={}'.format(pages))
	# except:
		# try:
			# time.sleep(5)
			# res = requests.get('https://api.bilibili.com/x/web-interface/newlist?rid=30&pn={}'.format(pages))
		# except:
			# Info('Spider','ERROR','第{}页连接超时'.format(pages))
			# time.sleep(2)
			# continue
	# out = ''
# #解析数据
	# for vinfo in res.json()['data']['archives']:
		# out += 	repr(vinfo['stat']['aid']) + ','
		# out +=  repr(vinfo['stat']['view']) +  ','
		# out +=  repr(vinfo['stat']['danmaku']) +  ','
		# out +=  repr(vinfo['stat']['reply']) +  ','
		# out +=  repr(vinfo['stat']['favorite']) +  ','
		# out +=  repr(vinfo['stat']['coin']) +  ','
		# out +=  repr(vinfo['stat']['share']) +  ','
		# out +=  repr(vinfo['stat']['like']) +  ','
		# out +=  repr(vinfo['stat']['dislike']) +  '\n'
	# f.write(out)

# f.close()
# Info('SPIDER','INFO','主线程结束')