import platform
print("系统信息".center(50,"="))
print(platform.platform())        #获取操作系统名称及版本号，'Linux-3.13.0-46-generic-i686-with-Deepin-2014.2-trusty'  
print(platform.architecture())    #获取操作系统的位数，('32bit', 'ELF')
print(platform.machine())         #计算机类型，'i686'
print(platform.processor())       #计算机处理器信息，''i686'
print("Python解释器信息".center(50,"="))
print(platform.python_build())
print(platform.python_compiler())
print(platform.python_implementation())
print("模块信息".center(50,"="))
modules = ("requests","psutil","tkinter","time","os","logging","queue","argparse")
for m in modules:
	try:
		__import__(m)
	except ModuleNotFoundError:
		print("{}模块未安装".format(m))
	except Exception as e:
		print("载入模块{}出错:".format(m),e)
	else:
		print("已载入模块{}".format(m))
print("网络信息".center(50,"="))
