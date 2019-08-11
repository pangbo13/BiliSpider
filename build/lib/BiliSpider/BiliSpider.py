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

		#创建必要文件夹
		if not os.path.exists(r'./log'):
			os.makedirs(r'./log')
		if not os.path.exists(r'./data'):
			os.makedirs(r'./data')

		self.set_logger(config)

		self.url = 'https://api.bilibili.com/x/web-interface/newlist?rid={}&pn={}'.format(rid,'{}')
		self.rid = rid
		if rid not in config['tid']:
			self.logger.warning('分区id不一致，请检查设置')
		self.thread_num = config.get('thread_num',2)
		self.http_port = config.get('http',1214)

		self.logger.debug("构造完成")

	def set_logger(self,config):

		#配置日志记录
		FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s '
		FILENAME = r'./log/'+'-'.join(map(str,tuple(time.localtime())[:5])) + '.log'
		#logging.basicConfig(level = logging.DEBUG,format = FORMAT ,datefmt='%H:%M:%S')
		logger = logging.getLogger(__name__)
		if config.get('debug',False):
			logger.setLevel(level = logging.DEBUG)
		elif config.get('logmode',1) ==0 and config.get('output',1) == 0:
			logger.setLevel(level = logging.FATAL)
		else:
			logger.setLevel(level = logging.INFO)

		#配置输出日志文件
		file_log_level = (0,logging.ERROR,logging.DEBUG)[config.get('logmode',1)]
		if file_log_level != 0 and config.get('debug',False):
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

		#日志配置完成
		logger.info("日志配置完毕")

		self.logger = logger
	
	#初始化函数
	def prepare(self):
		#更新状态
		self.status = {'process' : 'prepare'}
		
		threadLock = threading.Lock()
		q = queue.Queue()
		errorlist = []
		now_pages = 0
		#生成文件名
		FILENAME = r'./data/'+'-'.join(map(str,tuple(time.localtime())[:5])) + '({})'.format(self.rid) + '.txt'
		#打开文件			
		file = open(FILENAME, 'a+',encoding='utf-8')
		#输出当前时间
		file.write(time.ctime(time.time()) + '\n')
		#导入请求头
		from .headers import Api_headers as headers
		#封装全局变量
		self.global_var ={
			'threadLock' : threadLock,
			'queue' : q,
			'spider_threads' : [],
			'func_threads' : [],
			'errorlist' : errorlist,
			'now_pages' : now_pages,
			'file' : file,
			'url' : self.url,
			'headers' : headers,
			}
	#获取总页数函数
	def get_all_pages(self):
		'''
		获取总页数函数
		'''
		self.logger.debug("开始获取总页数")
		#print('正在获取总页数:',end='')
		try:
			res = requests.get(self.url.format(r'1&ps=1'))
			all_pages = int(res.json()['data']['page']['count']/50) + 1
			self.logger.info("分区下总页数：{}".format(all_pages))
			#print(all_pages)
			self.global_var['all_pages'] = all_pages
			return all_pages
		except:
			self.logger.error("获取总页数失败",exc_info = True)
			self.logger.error("服务器返回内容：\n" + res.content.decode('utf-8'))
			return -1
	def start(self):
		#更新状态
		self.status = {'process' : 'start'}
		self.status['spider_thread_num'] = self.thread_num
		# 创建新线程
		spider_threads = self.global_var['spider_threads']
		func_threads = self.global_var['func_threads']

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
		self.status['all_pages'] = all_pages
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
		self.status = {'process' : 'wait'}
		# 等待所有线程完成
		# threads = self.global_var['spider_threads']
		# for t in threads:
		# 	t.join()
		self.global_var['func_threads'][0].join()

	def close(self):
		'''
		进行后续操作
		'''
		self.global_var['file'].close()
	
	def auto_run(self):
		'''
		自动开始执行
		'''
		self.prepare()
		self.start()
		self.wait()
		self.close()
	

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
			self.father = father
			self.logger = father.logger

			self.logger.info(self.logformat("线程已创建！"))
		def logformat(self,msg):
			return self.name + ' - ' + msg

		def run(self): 
			#转存全局参数
			var = self.father.global_var
			all_pages = var['all_pages']
			url = var['url']
			queue = var['queue']
			threadLock = var['threadLock']
			logger = self.logger
			logformat = self.logformat
			logger.debug(logformat('线程已开始运行！'))
			time.sleep(0.5)
			while True:
				#修改全局变量
				threadLock.acquire()
				var['now_pages'] += 1
				pages = var['now_pages']
				threadLock.release()
				#判断是否继续
				if (pages>all_pages):
					break
				logger.debug("正在处理第{}页".format(pages))
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
						var['errorlist'].append(pages)
						continue
				e_time = time.time()*1000
				request_time =int( e_time - s_time )
				
				s_time = time.time()*1000
				items = ('aid','view','danmaku','reply','favorite','coin','share','like','dislike',)
				out = ''
				#解析数据
				for vinfo in res.json()['data']['archives']:
					out += ','.join(map(str,[vinfo['stat'][item] for item in items ])) + '\n'
				#写入数据
				queue.put(out,block=False)
				e_time = time.time()*1000
				write_time =int( e_time - s_time )
				logger.debug(logformat('第{}页-{}ms,{}ms'.format(pages,request_time,write_time)))
				time.sleep(0.2)
				self.pagesget += 1

	class MonitorThread (threading.Thread):
		def __init__(self, threadID, name, father):
			threading.Thread.__init__(self)
			self.threadID = threadID
			self.name = name
			self.father = father
			self.http_port = father.http_port
			self.logger = father.logger
			self.logger.debug(self.logformat('线程已创建！'))
		def run(self):
			#设置进度条长度
			self.BAR_LENGTH = 50

			#全局变量
			status = {}
			var = self.father.global_var
			queue = var['queue']
			f = var['file']
			spider_threads = var['spider_threads']
			#启动时间
			status['start_time'] = time.time()*1000
			
			monitor_output = self.show_bar
			time.sleep(1)
			monitor_circles = -1
			while any(t.isAlive() for t in spider_threads):
				monitor_circles += 1
				if monitor_circles % 5 == 0:
					#显示进度条
					if self.father.SHOW_BAR :
						percentage = (var['now_pages']-1)/var['all_pages']
						monitor_output(percentage,monitor_circles)
				if monitor_circles % 2 == 0:
					#更新状态
					status['queue_len'] = queue.qsize()
					status['now_pages'] = var['now_pages']
					status['now_times'] = time.time()*1000
					status['pages_get_by_threads'] = [t.pagesget for t in spider_threads]
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
				time.sleep(0.1)
				
			#将队列中剩余数据写入文件
			while not queue.empty():
				f.write(queue.get(block=False))

			monitor_output(1,monitor_circles)
			print('\n')

		def logformat(self,msg):
			return self.name + ' - ' + msg

		def show_bar(self,percentage,BAR_LENGTH,*args):
			BAR_LENGTH = self.BAR_LENGTH
			count = int(percentage*BAR_LENGTH)
			print('\r[{}{}] --{}%   '.format('#' * count ,' ' * (BAR_LENGTH - count),round(percentage*100,2)),end = '')

		def show_status(self,percentage,*args):
			pass

		def http_post_state(self):
			try:
				requests.post('http://localhost:{}/post'.format(self.http_port),json=self.father.status)
			except:
				pass
