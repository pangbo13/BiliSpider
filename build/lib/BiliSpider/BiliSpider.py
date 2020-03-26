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
		self.status = {'progress' : '__init__'}
		from .version import version
		self.status['version'] = version

		#创建数据文件夹
		if not os.path.exists(r'./data'):
			os.makedirs(r'./data')

		self.set_logger(config)

		self.url = 'https://api.bilibili.com/x/web-interface/newlist?rid={}&pn={}'.format(rid,'{}')
		self.rid = rid
		if rid not in config['tid']:
			self.__logger.warning('分区id不一致，请检查设置')
		self.thread_num = config.get('thread_num',2)
		self.http_port = config.get('http',1214)
		self.save_full = config.get('save_full',False)

		# 配置高级设置
		advanced_setting = dict(config.get('advanced_setting',{}))
		self.RUN_CUSTOM_FUNC = advanced_setting.get("RUN_CUSTOM_FUNC",False)
		self.COLLECT_ITEMS = advanced_setting.get('COLLECT_ITEMS',('aid','view','danmaku','reply','favorite','coin','share','like','dislike',))
		self.CIRCLE_INTERVAL = advanced_setting.get('CIRCLE_INTERVAL',0.1)
		self.BAR_LENGTH = advanced_setting.get('BAR_LENGTH',50)

		self.__logger.debug("构造完成")

	def reload(self,rid,config={}):
		self.status = {'progress' : '__init__'}
		self.url = 'https://api.bilibili.com/x/web-interface/newlist?rid={}&pn={}'.format(rid,'{}')
		self.rid = rid
		if rid not in config['tid']:
			self.__logger.warning('分区id不一致，请检查设置')
		self.__logger.debug("重置完成")

	def set_logger(self,config):
		#创建日志文件夹
		if not os.path.exists(r'./log'):
			os.makedirs(r'./log')

		#配置日志记录
		FORMAT = '[%(asctime)s][%(levelname)s] - %(message)s'
		FILENAME = r'./log/'+'-'.join(map(str,tuple(time.localtime())[:5])) + '.log'
		root_logger = logging.getLogger(__package__)
		if config.get('debug',False):
			root_logger.setLevel(level = logging.DEBUG)
		elif config.get('logmode',1) ==0 and config.get('output',1) == 0:
			root_logger.setLevel(level = logging.FATAL)
		else:
			root_logger.setLevel(level = logging.INFO)

		#配置输出日志文件
		file_log_level = (0,logging.ERROR,logging.DEBUG)[config.get('logmode',1)]
		if file_log_level != 0 :
			handler = logging.FileHandler(FILENAME,encoding='utf-8')
			handler.setLevel(file_log_level)
			handler.setFormatter(logging.Formatter(fmt = FORMAT,datefmt='%H:%M:%S'))
			root_logger.addHandler(handler)

		#配置控制台日志输出
		console = logging.StreamHandler()
		if config.get('output',1) != 1 :
			console.setLevel(logging.DEBUG)
		else:
			console.setLevel(logging.FATAL)
		console.setFormatter(logging.Formatter(fmt = FORMAT,datefmt='%H:%M:%S'))
		root_logger.addHandler(console)

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
		root_logger.info("日志配置完毕")

		self.__root_logger = root_logger
		self.__logger = logging.getLogger(__name__)
	
	#初始化函数
	def ready(self):
		#更新状态
		self.status['progress'] =  'prepare'
		
		threadLock = threading.Lock()
		q = queue.Queue()
		#生成文件名
		FILENAME = 'unfinished-' + '-'.join(map(str,tuple(time.localtime())[:5])) + '({})'.format(self.rid) + '.txt'
		#打开文件
		try:
			file = open(r'./data/'+FILENAME, 'a+',encoding='utf-8')
		except IOError as e:
			self.__logger.fatal("文件操作错误："+str(e))
			return -1
		except Exception as e:
			import traceback
			self.__logger.error(traceback.format_exc())
			self.__logger.fatal("意外终止："+str(e))
			return -2
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
			'file' : [file,],
			'url' : self.url,
			'headers' : headers,
			}

		if self.save_full:
			self._global_var['file'].append(open(r'./data/INFO - '+FILENAME,'w',encoding='utf-8'))

		return 0


	#获取总页数函数
	def get_all_pages(self):
		'''
		获取总页数函数
		'''
		self.__logger.debug("开始获取总页数")
		try:
			res = requests.get(self.url.format(r'1&ps=1'))
			all_pages = int(res.json()['data']['page']['count']/50) + 1
			self.__logger.info("分区下总页数：{}".format(all_pages))
			return all_pages
		except Exception as e:
			self.__logger.fatal("获取总页数失败："+str(e))
			self.__logger.debug("服务器返回内容：\n" + res.content.decode('utf-8'))
			return -1

	@staticmethod
	def get_pages_generator(all_panges):
		page = 0
		error_list = []
		while page<all_panges or len(error_list)>0:
			if page < all_panges:
				page += 1
				e = (yield page)
				if e != None:
					error_list.append(e)
			else:
				yield error_list.pop()



	def start_spider(self):
		#更新状态
		self.status['progress'] = 'start'
		self.status['spider_thread_num'] = self.thread_num
		self.status['http_mode'] = 0
		# 创建新线程
		spider_threads = self._global_var['spider_threads']
		func_threads = self._global_var['func_threads']

		for i in range(1,self.thread_num+1):
			spider_threads.append(self.SpiderThread(i, "SThread-{}".format(i), self))
		
		func_threads.append(self.MonitorThread(0, 'Monitor', self))
		if self.http_port != 0:
			try:
				res = requests.get('http://localhost:{}/data'.format(self.http_port),timeout=0.2)
				if res.json().get('spider').get('http_mode') == 0:
					self.status['http_mode'] = 1
				else :
					self.status['http_mode'] = 2
					from .tcppost import BilispiderSocket
					spidersocket = BilispiderSocket("localhost",1214,self)
					func_threads.append(spidersocket)
			except:
				from .httpserver import start_server
				http_thread = threading.Thread(target=start_server,daemon=True,name='HTTPserver',args=(self,self.http_port))
				func_threads.append(http_thread)
				self.status['http_mode'] = 1
		#http_mode 0-内置初始化 1-内置 2-外部
		#获取总页数
		all_pages = self.get_all_pages()
		if all_pages == -1:
			self.__logger.fatal("获取总页数失败，爬虫意外终止")
			self.set_fatal()
			return -1
		self._global_var['all_pages'] = all_pages
		self._global_var['pages_generator'] = self.get_pages_generator(all_pages)
		self.status['all_pages'] = all_pages
		self.status['got_pages'] = 0
		# 开启新线程
		for t in spider_threads:
			t.start()
		for t in func_threads:
			t.start()
		return 0
	#等待函数

	def wait(self):
		'''
		等待函数，阻塞当前进程至所有爬虫线程结束
		'''
		#更新状态
		self.status['progress'] = 'wait'
		# 等待所有线程完成
		while self._global_var['func_threads'][0].is_alive():
			try:
				time.sleep(1)
			except KeyboardInterrupt:
				self.set_pause(1)
				self.show_pause_menu()

	def close(self):
		'''
		进行后续操作
		'''
		if self.status['progress'] not in ('exit','fatal'):
			self.status['progress'] = 'close'
			for f in self._global_var['file']:
				f.close()
				os.rename(f.name,f.name.replace('unfinished-',''))
		else:
			for f in self._global_var['file']:
				f.close()
				os.rename(f.name,f.name.replace('unfinished-',self.status['progress'] + '-'))
	
	def auto_run(self):
		'''
		自动开始执行
		'''
		status_code = self.ready()
		if status_code != 0:
			return -1
		status_code = self.start_spider()
		if status_code != 0:
			return -2
		self.wait()
		self.close()
		return 0

	def set_custom_function(self,target):
		self.SpiderThread.CUSTOM_FUNC = target
		
	#运行时控制函数
	def set_pause(self,if_pause,thread_ids=()):
		'''
		此函数用于暂停爬虫线程
		if_pause用于标识是否暂停目标线程
		thread_ids为操作的目标线程id，留空则操作所有线程
		'''
		if not thread_ids:
			thread_ids = range(self.thread_num)
		else:
			if max(map(int,thread_ids)) > self.thread_num:
				raise RuntimeError()
			thread_ids = map(lambda x:int(x)-1,thread_ids)
		
		if if_pause:
			for id in thread_ids:
				if not self._global_var['spider_threads'][id].PAUSE:
					self._global_var['spider_threads'][id].PAUSE = True
			#等待所有线程暂停
			while not all(self._global_var['spider_threads'][id].PAUSE == 2 for id in thread_ids):
				time.sleep(0.2)
			self.__logger.info('程序暂停')
		else:
			for id in thread_ids:
				self._global_var['spider_threads'][id].PAUSE = False
	
	def get_pause(self):
		return tuple(t.PAUSE for t in self._global_var['spider_threads'])

	def set_fatal(self):
		'''
		此函数用于将爬虫状态设置为fatal，主要针对爬虫内部使用，不建议用户通过此函数退出爬虫
		若需要人为退出爬虫，建议使用 set_exit 函数
		'''
		self.status['progress'] = 'fatal'
		for t in self._global_var['spider_threads']:
			t.EXIT = True

	def set_exit(self):
		'''
		此函数用于用户控制中途退出爬虫
		'''
		self.status['progress'] = 'exit'
		for t in self._global_var['spider_threads']:
			t.EXIT = True

	def get_http_thread(self):
		'''
		返回服务器线程对象
		'''
		if len(self._global_var['func_threads']) != 1:
			return self._global_var['func_threads'][1]
		else:
			return None
		
	def debug_shell(self):
		try:
			while True:
				cmd = input('>>>')
				if cmd.rstrip().endswith(':'):
					cmd_list = []
					while cmd.strip():
						cmd_list.append(cmd)
						cmd = input()
					cmd = '\n'.join(cmd_list)
				try:
					exec(cmd.expandtabs(4))
				except :
					import traceback
					print('\n'.join(traceback.format_exc().splitlines()[3:]))
		except KeyboardInterrupt:
			print('\n退出')

	def show_pause_menu(self):
		if self.SHOW_BAR:
			print()#换行
		print('='*45)
		while True:
			print('请选择操作：')
			print('1.继续')
			print('2.退出')
			print('3.进入调试模式')
			choice = input('输入选择：')
			if choice == '1':
				self.set_pause(0)
				break
			elif choice == '2':
				if input('确认退出吗？(y/n)').lower() == 'y':
					self.set_exit()
					self.set_pause(0)
					break
				else:
					print('操作已取消')
			elif choice == '3':
				print('按下ctrl+C可退出')
				self.debug_shell()
			else:
				print('输入选项无效，',end='')
			print('='*45)

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
			self.EXIT = False
			self.father = father
			self.save_full = father.save_full
			self.__logger = logging.getLogger(__name__)
			self.session = requests.Session()

			#转存高级设置
			self.RUN_CUSTOM_FUNC = father.RUN_CUSTOM_FUNC
			self.COLLECT_ITEMS = father.COLLECT_ITEMS

			self.__logger.info(self.logformat("线程已创建！"))
		def __del__(self):
			self.session.close()
		def logformat(self,msg):
			return '线程' + str(self.threadID) + ' - ' + msg

		def CUSTOM_FUNC(self,res,father,logger):
			logger.warning("用户选择运行自定义函数，但未指定自定义函数")

		def run(self): 
			#转存全局参数
			var = self.father._global_var
			url = var['url']
			queue = var['queue']
			pages_generator = var['pages_generator']
			logger = self.__logger
			logformat = self.logformat
			error_page = None
			logger.debug(logformat('线程已开始运行！'))
			time.sleep(0.1)
			while True :
				if self.PAUSE:
					logger.info(logformat("线程已暂停"))
					self.PAUSE = 2
					while self.PAUSE:
						time.sleep(0.2) 
					logger.info(logformat("线程重新开始运行"))
				if self.EXIT:
					logger.warning(logformat("接受到退出指令"))
					self.EXIT = 2
					return
				#从列表获取页数
				try:
					page_id = pages_generator.send(error_page)
				except StopIteration:
					return
				logger.debug(logformat("正在处理第{}页".format(page_id)))
				s_time = time.time()*1000
				try:
					res = self.session.get(url.format(page_id),timeout = 2,headers = var['headers'])
				except requests.Timeout:
					logger.error(logformat('第{}页连接超时'.format(page_id)))
					try:
						time.sleep(2)
						res = self.session.get(url.format(page_id),timeout = 10,headers = var['headers'])
					except requests.Timeout:
						logger.error(logformat('第{}页连接第二次超时'.format(page_id)))
						error_page = page_id
						continue
				except Exception as e:
					logger.error(logformat("出现错误:"+str(e)))
					error_page = page_id
					continue
				e_time = time.time()*1000
				request_time =int( e_time - s_time )
				
				s_time = time.time()*1000

				out = ''
				#解析数据
				try:
					for vinfo in res.json()['data']['archives']:
						out += ','.join(map(str,[vinfo['stat'][item] for item in self.COLLECT_ITEMS ])) + '\n'
				except:
					logger.error(logformat("第{}页数据解析失败".format(page_id)))
					if res.status_code == 412:
						logger.fatal("服务器返回412")
						self.father.set_fatal()
						return
					else:
						continue

				if self.save_full:
					info_out = ''
					for vinfo in res.json()['data']['archives']:
						info_out += '\t'.join(map(str,[vinfo[item] for item in ('aid','bvid','title','videos','pubdate','duration')]))
						info_out += '\t' + str(vinfo['owner']['mid']) + '\t' + vinfo['owner']['name']
						info_out += '\t' + vinfo['pic'].rsplit(r'/',1)[-1][:-4]
						info_out += '\t' + repr(vinfo['desc'])[1:-1] + '\n'
					var['file'][1].write(info_out)

				if self.RUN_CUSTOM_FUNC:
					try:
						s_time = time.time() * 1000
						self.CUSTOM_FUNC(res,father,logger)
						e_time = time.time() * 1000
					except:
						logger.warning(logformat("第{}页自定义函数调用出错".format(page_id)))
					else:
						logger.debug(logformat("第{}页自定义函数调用结束，用时:{}ms".format(page_id,int(e_time-s_time))))
				#写入数据
				queue.put(out,block=False)
				e_time = time.time()*1000
				write_time =int( e_time - s_time )
				logger.debug(logformat('第{}页-{}ms,{}ms'.format(page_id,request_time,write_time)))
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
			self.__logger = logging.getLogger(__name__)

			# 转存高级设置
			self.BAR_LENGTH = father.BAR_LENGTH
			self.CIRCLE_INTERVAL = father.CIRCLE_INTERVAL

			self.__logger.debug(self.logformat('线程已创建！'))
		def run(self):
			#全局变量
			father = self.father
			status = father.status
			var = father._global_var
			queue = var['queue']
			f = var['file'][0]
			spider_threads = var['spider_threads']
			#启动时间
			status['start_time'] = time.time()*1000
			status['pause_time'] = 0

			
			if self.SHOW_BAR:
				monitor_output = self.show_bar
			else:
				monitor_output = self.show_status

			#等待爬虫线程启动
			while not any(t.is_alive() for t in spider_threads):
				time.sleep(0.02)

			monitor_circles = -1
			while any(t.is_alive() for t in spider_threads):
				if all(father.get_pause()):
					pause_start = time.time()*1000
					while all(father.get_pause()):
						time.sleep(self.CIRCLE_INTERVAL)
					status['pause_time'] += time.time()*1000 - pause_start
					if status['progress'] == 'exit':
						break
				monitor_circles += 1
				if monitor_circles % 2 == 0:
					#更新状态
					status['queue_len'] = queue.qsize()
					status['now_time'] = time.time()*1000
					status['pages_get_by_threads'] = [t.pagesget for t in spider_threads]
					status['got_pages'] = var['got_pages']
					status['percentage'] = (var['got_pages'])/var['all_pages']
					status['monitor_circles'] = monitor_circles
				if monitor_circles % 5 == 0:
					#显示进度条或输出状态
					if not self.QUITE_MODE :
						percentage = (var['got_pages'])/var['all_pages']
						monitor_output(percentage,monitor_circles)
				if monitor_circles % 20 == 0:
					if status['http_mode'] == 2 and self.http_port != 0:
						#发送当前状态
						threading.Thread(target=self.http_post_status,name='http_post',daemon=True).start()
				if monitor_circles % 50 == 0:
					#写入文件
					while not queue.empty():
						f.write(queue.get(block=False))
				time.sleep(self.CIRCLE_INTERVAL)
			
			#完成后再次执行一次循环
			#显示进度条或输出状态
			if not self.QUITE_MODE and not status['progress'] == 'exit':
				percentage = (var['got_pages'])/var['all_pages']
				monitor_output(percentage,0)
			#更新状态
			status['queue_len'] = queue.qsize()
			status['now_time'] = time.time()*1000
			status['pages_get_by_threads'] = [t.pagesget for t in spider_threads]
			status['got_pages'] = var['got_pages']
			status['percentage'] = (var['got_pages'])/var['all_pages']
			status['monitor_circles'] = monitor_circles
			if status['http_mode'] == 2 and self.http_port != 0:
				#发送当前状态
				threading.Thread(target=self.http_post_status,name='http_post',daemon=True).start()
			#写入文件
			while not queue.empty():
				f.write(queue.get(block=False))
			#最后一次循环完毕
			if status['progress'] == 'fatal' :
				self.__logger.fatal('爬虫意外退出')
			else:
				self.__logger.info('运行结束')
			if self.SHOW_BAR:
				print()

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
				used_time = self.CIRCLE_INTERVAL * status['monitor_circles']
				if status['got_pages'] != 0:
					left_time = (status['all_pages']/status['got_pages'] - 1) * used_time
				else:
					left_time = 0
				msg = "{}/{} ({} %) - {}left ".format(
						status['got_pages'], status['all_pages'], int(percentage*100), 
						self.time_format(int(left_time)))
				self.__logger.info(msg)
				return
			else :
				return

		def http_post_status(self):
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
				return '0s '
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
