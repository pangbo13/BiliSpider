import platform
print("="*19,"系统信息","="*19)
print(platform.platform())        #获取操作系统名称及版本号，'Linux-3.13.0-46-generic-i686-with-Deepin-2014.2-trusty'  
print(platform.architecture())    #获取操作系统的位数，('32bit', 'ELF')
print(platform.machine())         #计算机类型，'i686'
print(platform.processor())       #计算机处理器信息，''i686'
print("="*15,"python解释器信息","="*15)
print(platform.python_build())
print(platform.python_compiler())
print(platform.python_implementation())
print("="*19,"网络信息","="*19)
print("="*19,"模块信息","="*19)