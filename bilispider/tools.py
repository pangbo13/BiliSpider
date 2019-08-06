def get_tid_by_url(url):
	#定义查找函数
	def str_clip(content,start_str,end_str):
		start = content.find(start_str) + len(start_str)
		end = content.find(end_str,start)
		if start == -1 or end == -1:
			return None
		return content[start:end]
	import requests
	#导入请求头
	from .headers import Page_headers as headers
	#获取网页内容
	#使用.content获取二进制内容再编码，避免使用.text出现中文编码错误
	content = requests.get(url,headers=headers).content.decode('utf-8')
	#裁剪网页，返回结果
	#返回结果：tuple(分区id,分区名)
	return (str_clip(content,r'"tid":',r','),str_clip(content,r'"tname":"',r'",'))

def aid_decode(url):
	#定义错误类
	class URL_ERROR(Exception):
		def __init__(self):
			super().__init__()
			self.args = ('无法识别av号',)
			self.code = '101'

	url = url.lower()
	if url.isdigit():
		#如果是纯数字
		url = r'https://www.bilibili.com/video/av' + url
	elif url[:2] == 'av':
		#如果是以av开头的av号
		if not url[2:].isdigit():
			raise URL_ERROR()
		url = r'https://www.bilibili.com/video/' + url
	elif 'av' in url :
		#检测地址中是否含av关键字
		#拆分地址，选取含有av的部分
		url = filter(lambda x : 'av' in x ,url.split(r'/'))
		#如果获取多个结果，只选择第一个，避免后面的额外信息包括关键词
		url = tuple(url)[0]
		#检测获取的片段是否是av+数字的形式，否则抛出错误
		if url[:2] != 'av' :
			raise URL_ERROR()
		if url[2:].isdigit():
			raise URL_ERROR()
		#格式化为完整视频地址
		url = r'https://www.bilibili.com/video/' + url
	else:
		raise URL_ERROR()
	return url

def check_update():
	from .version import version
	from requests import get
	from os import system
	print('正在检查更新')
	res = get(r'https://raw.githubusercontent.com/pangbo13/BiliSpider/master/version.txt')
	latest_version = res.text
	now_version = version
	if latest_version > now_version:
		print('发现更新：' + latest_version)
		system(r'pip install https://github.com/pangbo13/BiliSpider/blob/master/dist/bilispider-{}-py3-none-any.whl?raw=true'.format(latest_version))
	else:
		print('未发现更新')

