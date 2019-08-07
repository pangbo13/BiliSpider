
A spider of BiliBili.

基于python3编写的一个bilibili多线程爬虫。

# 安装

## 安装python 3.7 
+ https://www.python.org/downloads/
## 安装bilispider
+ pip3 install bilispider
# 快速入门
### Windows
+ 在cmd中使用bilispider启动，输入`bilispider –help`以查看帮助
+ 在cmd中使用`python -m bilispider`
## Linux
+ 在终端中使用`python3 -m bilispider`启动
## 作为模块导入
+ `import bilispider`
+ 使用`help(bilispider.bilispider)`以查看用法
+ 实例化类：`s = bilispider.spider(tid,config={})`
	+ tid:分区的编号，查询方法见GUI和高级用法
	+ config：字典类型变量(可选)，用于指定设置参数，用法见[高级用法](#高级用法 "转到高级用法")
+ 开始爬取：`s.auto_run()`
	+ 若希望控制运行过程请见[高级用法](#高级用法 "转到高级用法")
## GUI控制模式(测试版本)
+ 在控制台使用`bilispider --gui`或`python -m bilispider --gui`(Linux下为`python3 -m bilispider --gui` )
	> 详见[GUI指南](#GUI指南 "GUI指南")

# 设置参数
+ `-h`，`--help`：打印帮助信息并退出
+ `-v`,`--version`：显示版本
+ **`-t`,`--tid`：通过分组id进行爬取 可使用逗号连接多个tid，如：`-t 1,2,3`**
+ **`-u`,`--url`: 通过视频网址或av号自动识别分区并爬取 *注意：仅在无(--tid,-t)时生效***
+  `-lc`,`--loadconfig`: 指定配置文件 *注意：单独指定的参数将覆盖配置文件参数*
+ `--output`: `指定控制台输出模式 *默认为1*
	+ 0-无输出
	+ **1-进度条模式**
	+ 2-输出日志
+ `--logmode`：指定日志保存模式 *默认为1*
	+ 0-不保存
	+ **1-仅保存错误**
	+ 2-保存所有输出
+ `--debug`：启用调试
+ `--saveconfig`,`-sc`：根据参数保存配置文件并退出 *注意：使用该参数不会爬取数据*
+ `--thread_num`,`-tn`：指定线程数，默认为2 
	+  ***注意：线程数过多可能导致IP封禁***
+ `--gui`,`-g`：打开可视化界面 *(测试)*
+ `--safemode`：安全模式 *(测试)*
## 参数实例
> bilispider --tid 30 \
 bilispider -t 30 

> bilispider -u https://www.bilibili.com/video/av61967870 \
bilispider -u av61967870 \
bilispider -u 61967870

> bilispider -t 30 --output 2 --logmode 2 --debug \
bilispider -t 30 --output 2 --logmode 2 -sc config.json \
bilispider -lc config.json


# GUI指南
![GUI窗口](img/gui_1.png "GUI主窗口")
+ 在 从url识别中 输入av号或视频地址，点击确认获取分区信息
+ 点击确认以提交参数

# HTTP服务器
+ 运行内置httpsever模块或使用[BiliSpider_HTTPserver](https://github.com/pangbo13/BiliSpider_HTTPserver "在github中打开BiliSpider_HTTPserver")启动服务器
+ 服务器将运行于1214端口
+ 通过访问data路径可获取爬虫状态和系统资源信息，例如： 
	> http://localhost:1214/data
+ 返回值为json格式
# 高级用法
## ~~咕咕咕~~