#coding=utf-8
import requests
import time
def safemode(rid):
	start_time = time.time()

	print('正在获取总页数')
	res = requests.get('https://api.bilibili.com/x/web-interface/newlist?rid={}&ps=1'.format(rid))
	all_pages = int(res.json()['data']['page']['count']/50) + 1
	print(all_pages)

	f = open('data.txt', 'a+',encoding='utf-8')
	pages = 1
	while pages <= all_pages:
		print(str(pages)+'\t--'+str(int((pages*10000)/all_pages)/100)+'%')
		s_time = time.time()*1000
		try:
			res = requests.get('https://api.bilibili.com/x/web-interface/newlist?rid={}&pn={}'.format(rid,pages))
		except:
			print('连接超时')
			time.sleep(5)
			continue
		e_time =time.time()*1000
		request_time =int( e_time - s_time )
		s_time = int(time.time()*1000)
		for vinfo in res.json()['data']['archives']:
			out = repr(vinfo['stat']['aid']) + ','
			out +=  repr(vinfo['stat']['view']) +  ','
			out +=  repr(vinfo['stat']['danmaku']) +  ','
			out +=  repr(vinfo['stat']['reply']) +  ','
			out +=  repr(vinfo['stat']['favorite']) +  ','
			out +=  repr(vinfo['stat']['coin']) +  ','
			out +=  repr(vinfo['stat']['share']) +  ','
			out +=  repr(vinfo['stat']['like']) +  ','
			out +=  repr(vinfo['stat']['dislike']) +  '\n'
			f.write(out)
		e_time = time.time()*1000
		write_time =int( e_time - s_time )
		left_time = int((all_pages-pages)*(e_time/1000-start_time)/pages)
		print('request:'+str(request_time)+'ms\twrite:'+str(write_time)+'ms\tleft:'+str(left_time)+'s')
		pages += 1
	f.close()
	print('done')
	end_time = time.time()
	print(str(int(end_time - start_time))+'s')

