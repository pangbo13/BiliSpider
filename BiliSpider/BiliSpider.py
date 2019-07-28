#coding=utf-8
import requests
import time
import threading
import sys

<<<<<<< Updated upstream
=======
class spider():
	
	#构造函数
	def __init__(self,rid,config={}):
		
		self.set_logger(config)
>>>>>>> Stashed changes

class Spider():
	def __init__(self,rid,thread_num=2):
		self.url = 'https://api.bilibili.com/x/web-interface/newlist?rid={}&pn={}'.format(rid,'{}')
		self.rid = rid
<<<<<<< Updated upstream
		self.thread_num = thread_num
=======
		if rid not in config['tid']:
			self.logger.warning('分区id不一致，请检查设置')
		self.thread_num = config.get('thread_num',2)

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
	
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
=======
		#导入请求头
		from .headers import Api_headers as headers
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
			print('获取总页数失败')
			print('服务器返回内容：')
			print(res.text)
=======
			self.logger.error("获取总页数失败",exc_info = True)
			self.logger.error("服务器返回内容：\n" + res.content.decode('utf-8'))
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
		
	#消息处理函数
	def Info(self,threadname,type,content):
		INFO_time = time.strftime('%H:%M:%S',time.localtime())
		if type == 'INFO':
			print('[{}][ INFO][{}]{}'.format(INFO_time,threadname,content))
		if type == 'ERROR':
			print('[{}][ERROR][{}]{}'.format(INFO_time,threadname,content))
		if type == 'DEBUG':
			print('[{}][DEBUG][{}]{}'.format(INFO_time,threadname,content))	
			
=======

	def close(self):
		self.global_var['file'].close()
	
	def auto_run(self):
		self.prepare()
		self.start()
		self.wait()
		self.close()
	

>>>>>>> Stashed changes
	class SpiderThread (threading.Thread):
		def __init__(self, threadID, name, father):
			threading.Thread.__init__(self)
			self.threadID = threadID
			self.name = name
			self.pagesget = 0
			self.father = father
<<<<<<< Updated upstream
			self.father.Info(self.name,'DEBUG','线程已创建！')
		def run(self): 
			Info = self.father.Info			#转存Info函数
=======
			self.logger = father.logger

			self.logger.info(self.logformat("线程已创建！"))
		def logformat(self,msg):
			return self.name + ' - ' + msg

		def run(self): 
>>>>>>> Stashed changes
			#转存全局参数
			var = self.father.global_var
			all_pages = var['all_pages']
			url = var['url']
			f = var['file']
			threadLock = var['threadLock']
<<<<<<< Updated upstream
			Info(self.name,'DEBUG','线程已开始运行！')
=======
			logger = self.logger
			logformat = self.logformat
			logger.debug(logformat('线程已开始运行！'))
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
				Info(self.name,'INFO','正在处理第{}页'.format(pages))
=======
				logger.debug("正在处理第{}页".format(pages))
>>>>>>> Stashed changes
				#连接服务器
				s_time = time.time()*1000
				try:
					res = requests.get(url.format(pages),timeout = 2)
				except:
<<<<<<< Updated upstream
					Info(self.name,'ERROR','第{}页连接超时'.format(pages))
=======
					logger.error(logformat('第{}页连接超时'.format(pages)))
>>>>>>> Stashed changes
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
				items = ('aid','view','danmaku','reply','favorite','coin','share','like','dislike',)
				out = ''
				#解析数据
				for vinfo in res.json()['data']['archives']:
					out += ','.join(map(str,[vinfo['stat'][item] for item in items ])) + '\n'
					# out += 	repr(vinfo['stat']['aid']) + ','
					# out +=  repr(vinfo['stat']['view']) +  ','
					# out +=  repr(vinfo['stat']['danmaku']) +  ','
					# out +=  repr(vinfo['stat']['reply']) +  ','
					# out +=  repr(vinfo['stat']['favorite']) +  ','
					# out +=  repr(vinfo['stat']['coin']) +  ','
					# out +=  repr(vinfo['stat']['share']) +  ','
					# out +=  repr(vinfo['stat']['like']) +  ','
					# out +=  repr(vinfo['stat']['dislike']) +  '\n'
				#写入数据
<<<<<<< Updated upstream
				threadLock.acquire()
				f.write(out)
				threadLock.release()
				e_time = time.time()*1000
				write_time =int( e_time - s_time )
				
				Info(self.name,'DEBUG','第{}页-{}ms,{}ms'.format(pages,request_time,write_time))
=======
				queue.put(out,block=False)
				e_time = time.time()*1000
				write_time =int( e_time - s_time )
				logger.debug(logformat('第{}页-{}ms,{}ms'.format(pages,request_time,write_time)))
>>>>>>> Stashed changes
				time.sleep(0.2)
				self.pagesget += 1

	class MonitorThread (threading.Thread):
		def __init__(self, threadID, name, father):
			threading.Thread.__init__(self)
			self.threadID = threadID
			self.name = name
			self.father = father
			self.logger = father.logger
			self.logger.debug(self.logformat('线程已创建！'))
		def run(self):
			var = self.father.global_var
<<<<<<< Updated upstream
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
=======
			queue = var['queue']
			f = var['file']
			threads = var['threads'][1:]
			monitor_output = self.show_bar
			time.sleep(1)
			while bool(sum(t.isAlive() for t in threads)):
				if self.father.SHOW_BAR :
					percentage = (var['now_pages']-1)/var['all_pages']
					monitor_output(percentage,BAR_LENGTH)
				time.sleep(0.5)
				while not queue.empty():
					f.write(queue.get(block=False))
			monitor_output(1,BAR_LENGTH)

		def logformat(self,msg):
			return self.name + ' - ' + msg

		def show_bar(self,percentage,BAR_LENGTH):
			count = int(percentage*BAR_LENGTH)
			print('\r[{}{}] --{}%   '.format('#' * count ,' ' * (BAR_LENGTH - count),round(percentage*100,2)),end = '')
>>>>>>> Stashed changes
