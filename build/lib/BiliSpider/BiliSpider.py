#coding=utf-8
import requests
import time
import threading
import os
import queue
import logging

class spider():
	'''
	爬虫类
	'''
	#构造函数
	def __init__(self,rid,config={}):
		'''
		爬虫类构造函数，接受参数：
		\t tid:分区id
		\t config:设置参数(dict类型)
		'''
		#更新状态
		self.status = {'process' : '__init__'}

		#创建数据文件夹
		if not os.path.exists(r'./data'):
			os.makedirs(r'./data')

		self.set_logger(config)

		self.url = 'https://api.bilibili.com/x/web-interface/newlist?rid={}&pn={}'.format(rid,'{}')
		self.rid = rid
		if rid not in config['tid']:
			self._logger.warning('分区id不一致，请检查设置')
		self.thread_num = config.get('thread_num',2)
		self.http_port = config.get('http',1214)

		# 配置高级设置
		advanced_setting = dict(config.get('advanced_setting',{}))
		self.RUN_CUSTOM_FUNC = advanced_setting.get("RUN_CUSTOM_FUNC",False)
		self.COLLECT_ITEMS = advanced_setting.get('COLLECT_ITEMS',('aid','view','danmaku','reply','favorite','coin','share','like','dislike',))
		self.CIRCLE_INTERVAL = advanced_setting.get('CIRCLE_INTERVAL',0.1)
		self.BAR_LENGTH = advanced_setting.get('BAR_LENGTH',50)
		# if isinstance(advanced_setting.get('CUSTOM_FUNC',None),type(self.SpiderThread.CUSTOM_FUNC)):
		# 	self.SpiderThread.CUSTOM_FUNC = advanced_setting['CUSTOM_FUNC']

		self._logger.debug("构造完成")

	def set_logger(self,config):
		#创建日志文件夹
		if not os.path.exists(r'./log'):
			os.makedirs(r'./log')

		#配置日志记录
		FORMAT = '[%(asctime)s][%(levelname)s] - %(message)s'
		FILENAME = r'./log/'+'-'.join(map(str,tuple(time.localtime())[:5])) + '.log'
		logger = logging.getLogger(__name__)
		if config.get('debug',False):
			logger.setLevel(level = logging.DEBUG)
		elif config.get('logmode',1) ==0 and config.get('output',1) == 0:
			logger.setLevel(level = logging.FATAL)
		else:
			logger.setLevel(level = logging.INFO)

		#配置输出日志文件
		file_log_level = (0,logging.ERROR,logging.DEBUG)[config.get('logmode',1)]
		if file_log_level != 0 :
			handler = logging.FileHandler(FILENAME,encoding='utf-8')
			handler.setLevel(file_log_level)
			handler.setFormatter(logging.Formatter(fmt = FORMAT,datefmt='%H:%M:%S'))
			logger.addHandler(handler)

		#配置控制台日志输出
		console = logging.StreamHandler()
		if config.get('output',1) != 1 :
			console.setLevel(logging.DEBUG)
		else:
			console.setLevel(logging.FATAL)
		console.setFormatter(logging.Formatter(fmt = FORMAT,datefmt='%H:%M:%S'))
		logger.addHandler(console)

		#配置进度条
		if config.get('output',1) == 1:
			self.SHOW_BAR = True
		else :
			self.SHOW_BAR = False

		if config.get('output',1) == 0:
			self.QUITE_MODE = True
		else :
			self.QUITE_MODE = False

		#日志配置完成
		logger.info("日志配置完毕")

		self._logger = logger
	
	#初始化函数
	def prepare(self):
		#更新状态
		self.status.update({'process' : 'prepare'})
		
		threadLock = threading.Lock()
		q = queue.Queue()
		#生成文件名
		FILENAME = r'./data/'+'-'.join(map(str,tuple(time.localtime())[:5])) + '({})'.format(self.rid) + '.txt'
		#打开文件			
		file = open(FILENAME, 'a+',encoding='utf-8')
		#输出当前时间
		file.write(time.ctime(time.time()) + '\n')
		#导入请求头
		from .headers import Api_headers as headers
		#封装全局变量
		self._global_var ={
			'threadLock' : threadLock,
			'queue' : q,
			'spider_threads' : [],
			'func_threads' : [],
			'got_pages' : 0,
			'file' : file,
			'url' : self.url,
			'headers' : headers,
			}
	#获取总页数函数
	def get_all_pages(self):
		'''
		获取总页数函数
		'''
		self._logger.debug("开始获取总页数")
		try:
			res = requests.get(self.url.format(r'1&ps=1'))
			all_pages = int(res.json()['data']['page']['count']/50) + 1
			self._logger.info("分区下总页数：{}".format(all_pages))
			self._global_var['all_pages'] = all_pages
			self._global_var['pages_list'] = list(range(1,all_pages+1))
			return all_pages
		except:
			self._logger.error("获取总页数失败",exc_info = True)
			self._logger.error("服务器返回内容：\n" + res.content.decode('utf-8'))
			return -1
	def start_spider(self):
		#更新状态
		self.status.update({'process' : 'start'})
		self.status['spider_thread_num'] = self.thread_num
		# 创建新线程
		spider_threads = self._global_var['spider_threads']
		func_threads = self._global_var['func_threads']

		for i in range(1,self.thread_num+1):
			spider_threads.append(self.SpiderThread(i, "SThread-{}".format(i), self))
		
		func_threads.append(self.MonitorThread(0, 'Monitor', self))
		if self.http_port != 0:
			try:
				requests.get('http://localhost:{}'.format(self.http_port),timeout=0.2)
			except:
				from .httpserver import start_server
				http_thread = threading.Thread(target=start_server,daemon=True,name='http',args=(self.http_port,))
				func_threads.append(http_thread)
		#获取总页数
		all_pages = self.get_all_pages()
		if all_pages == -1:
			self._logger.fatal("获取总页数失败，爬虫意外终止")
			exit()
		self.status['all_pages'] = all_pages
		self.status['got_pages'] = 0
		# 开启新线程
		for t in spider_threads:
			t.start()
		for t in func_threads:
			t.start()
	#等待函数
	def wait(self):
		'''
		等待函数，阻塞当前进程至所有爬虫线程结束
		'''
		#更新状态
		self.status.update({'process' : 'wait'})
		# 等待所有线程完成
		self._global_var['func_threads'][0].join()

	def close(self):
		'''
		进行后续操作
		'''
		self._global_var['file'].close()
	
	def auto_run(self):
		'''
		自动开始执行
		'''
		self.prepare()
		self.start_spider()
		self.wait()
		self.close()

	def set_custom_function(self,target):
		self.SpiderThread.CUSTOM_FUNC = target
		
	#运行时控制函数
	def set_pause(self,if_pause,thread_ids=0):
		if thread_ids == 0:
			thread_ids = range(self.thread_num)
		else:
			if max(map(int,thread_ids)) > self.thread_num:
				raise RuntimeError()
			thread_ids = map(lambda x:int(x)-1,thread_ids)
		for id in thread_ids:
			self._global_var['spider_threads'][id] = bool(if_pause)
	
	def get_pause(self):
		return tuple(t.PAUSE for t in self._global_var['spider_threads'])

	class SpiderThread (threading.Thread):
		'''
		爬虫线程类
		'''
		def __init__(self, threadID, name, father):
			'''
			爬虫线程类初始化函数
			参数为线程id(int),线程名(str),父类对象(class spider)
			'''
			threading.Thread.__init__(self)
			self.threadID = threadID
			self.name = name
			self.pagesget = 0
			self.PAUSE = False
			self.father = father
			self._logger = father._logger

			#转存高级设置
			self.RUN_CUSTOM_FUNC = father.RUN_CUSTOM_FUNC
			self.COLLECT_ITEMS = father.COLLECT_ITEMS

			self._logger.info(self.logformat("线程已创建！"))
		def logformat(self,msg):
			return '线程' + str(self.threadID) + ' - ' + msg

		def CUSTOM_FUNC(self,res,father,logger):
			logger.warning("用户选择运行自定义函数，但未指定自定义函数")

		def run(self): 
			#转存全局参数
			var = self.father._global_var
			url = var['url']
			queue = var['queue']
			pages_list = var['pages_list']
			logger = self._logger
			logformat = self.logformat
			logger.debug(logformat('线程已开始运行！'))
			time.sleep(0.1)
			while len(pages_list) > 0 :
				if self.PAUSE:
					logger.info(logformat("线程已暂停"))
					while self.PAUSE:
						time.sleep(0.2)
					logger.info(logformat("线程重新开始运行"))
				#从列表获取页数
				pages = pages_list.pop(0)
				logger.debug(logformat("正在处理第{}页".format(pages)))
				#连接服务器
				s_time = time.time()*1000
				try:
					res = requests.get(url.format(pages),timeout = 2,headers = var['headers'])
				except:
					logger.error(logformat('第{}页连接超时'.format(pages)))
					try:
						time.sleep(2)
						res = requests.get(url.format(pages),timeout = 10,headers = var['headers'])
					except:
						logger.error(logformat('第{}页连接第二次超时'.format(pages)))
						pages_list.append(pages)
						continue
				e_time = time.time()*1000
				request_time =int( e_time - s_time )
				
				s_time = time.time()*1000
				#items = ('aid','view','danmaku','reply','favorite','coin','share','like','dislike',)
				out = ''
				#解析数据
				try:
					for vinfo in res.json()['data']['archives']:
						out += ','.join(map(str,[vinfo['stat'][item] for item in self.COLLECT_ITEMS ])) + '\n'
				except:
					logger.error(logformat("第{}页数据解析失败".format(pages)))

				if self.RUN_CUSTOM_FUNC:
					try:
						s_time = time.time() * 1000
						self.CUSTOM_FUNC(res,father,logger)
						e_time = time.time() * 1000
					except:
						logger.warning(logformat("第{}页自定义函数调用出错".format(pages)))
					else:
						logger.debug(logformat("第{}页自定义函数调用结束，用时:{}ms".format(pages,int(e_time-s_time))))
				#写入数据
				queue.put(out,block=False)
				e_time = time.time()*1000
				write_time =int( e_time - s_time )
				logger.debug(logformat('第{}页-{}ms,{}ms'.format(pages,request_time,write_time)))
				var['got_pages'] += 1
				self.pagesget += 1
				time.sleep(0.2)

	class MonitorThread (threading.Thread):
		def __init__(self, threadID, name, father):
			threading.Thread.__init__(self)
			self.threadID = threadID
			self.name = name
			self.father = father
			self.SHOW_BAR = father.SHOW_BAR
			self.QUITE_MODE = father.QUITE_MODE
			self.http_port = father.http_port
			self._logger = father._logger

			# 转存高级设置
			self.BAR_LENGTH = father.BAR_LENGTH
			self.CIRCLE_INTERVAL = father.CIRCLE_INTERVAL

			self._logger.debug(self.logformat('线程已创建！'))
		def run(self):
			#设置进度条长度
			#BAR_LENGTH = self.BAR_LENGTH

			#全局变量
			status = {}
			var = self.father._global_var
			queue = var['queue']
			f = var['file']
			spider_threads = var['spider_threads']
			#启动时间
			self.father.status['start_time'] = time.time()*1000
			
			if self.SHOW_BAR:
				monitor_output = self.show_bar
			else:
				monitor_output = self.show_status

			#等待爬虫线程启动
			while not any(t.is_alive() for t in spider_threads):
				time.sleep(0.02)

			monitor_circles = -1
			while any(t.is_alive() for t in spider_threads):
				monitor_circles += 1
				if monitor_circles % 5 == 0:
					#显示进度条或输出状态
					if not self.QUITE_MODE :
						percentage = (var['got_pages'])/var['all_pages']
						monitor_output(percentage,monitor_circles)
				if monitor_circles % 2 == 0:
					#更新状态
					status['queue_len'] = queue.qsize()
					status['now_time'] = time.time()*1000
					status['pages_get_by_threads'] = [t.pagesget for t in spider_threads]
					status['got_pages'] = var['got_pages']
					status['percentage'] = (var['got_pages'])/var['all_pages']
					status['monitor_circles'] = monitor_circles
					self.father.status.update(status)
				if monitor_circles % 20 == 0:
					if self.http_port != 0:
						#发送当前状态
						threading.Thread(target=self.http_post_state,name='http_post',daemon=True).start()
				if monitor_circles % 50 == 0:
					#写入文件
					while not queue.empty():
						f.write(queue.get(block=False))
				time.sleep(self.CIRCLE_INTERVAL)
			
			#完成后再次执行一次循环
			#显示进度条或输出状态
			if not self.QUITE_MODE :
				percentage = (var['got_pages'])/var['all_pages']
				monitor_output(percentage,0)
			#更新状态
			status['queue_len'] = queue.qsize()
			status['now_time'] = time.time()*1000
			status['pages_get_by_threads'] = [t.pagesget for t in spider_threads]
			status['got_pages'] = var['got_pages']
			status['percentage'] = (var['got_pages'])/var['all_pages']
			status['monitor_circles'] = monitor_circles
			self.father.status.update(status)
			if self.http_port != 0:
				#发送当前状态
				threading.Thread(target=self.http_post_state,name='http_post',daemon=True).start()
			#写入文件
			while not queue.empty():
				f.write(queue.get(block=False))
			#最后一次循环完毕

			print('\n')

		def logformat(self,msg):
			return self.name + ' - ' + msg

		def show_bar(self,percentage,*args):
			BAR_LENGTH = self.BAR_LENGTH
			count = int(percentage*BAR_LENGTH)
			print('\r[{}{}] --{}%   '.format('#' * count ,' ' * (BAR_LENGTH - count),round(percentage*100,2)),end = '')
			return

		def show_status(self,percentage,monitor_circles,*args):
			if monitor_circles % 30 == 0:
				status = self.father.status
				used_time = time.time() - status['start_time']/1000
				if status['got_pages'] != 0:
					left_time = (status['all_pages']/status['got_pages'] - 1) * used_time
				else:
					left_time = 0
				msg = "{}/{} ({} %) - {}left ".format(
						status['got_pages'], status['all_pages'], int(percentage*100), 
						self.time_format(int(left_time)))
				self._logger.info(msg)
				return
			else :
				return

		def http_post_state(self):
			try:
				requests.post('http://localhost:{}/post'.format(self.http_port),json=self.father.status)
				self.father.status.update({"post_state":True})
			except:
				self.father.status.update({"post_state":False})
		
		#用于将秒数转化为小时分钟格式
		@staticmethod
		def time_format(second):
			second = int(second)
			if second <= 0:
				return '0s'
			else :
				time_lis = [0,0,0]
				if second >= 3600 :
					time_lis[0] = second // 3600
					second %= 3600
				if second >= 60 :
					time_lis[1] = second // 60
					second %= 60
				time_lis[2] = second
				for i in range(len(time_lis)):
					if time_lis[i]:
						top_level = i
						break
				out = ""
				level_name = ("h","min","s")
				for i in range(top_level,len(time_lis)):
					out += "{}{} ".format(time_lis[i],level_name[i])
				return out
