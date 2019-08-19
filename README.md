
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
+ `--safemode`：安全模式
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
## 基本设置
![GUI窗口](img/gui_2.png "GUI主窗口")
+ 在 从url识别中 输入av号或视频地址，点击确认获取分区信息
+ 点击确认以提交参数
## 高级设置
![GUI窗口高级选项](img/gui_3.png "GUI主窗口高级选项")

# HTTP服务器
+ 运行内置httpsever模块或使用[BiliSpider_HTTPserver](https://github.com/pangbo13/BiliSpider_HTTPserver "在github中打开BiliSpider_HTTPserver")启动服务器
+ 服务器将运行于1214端口
+ 通过访问data路径可获取爬虫状态和系统资源信息，例如： 
	> http://localhost:1214/data
+ 返回值为json格式
# 高级用法
## ~~咕咕咕~~
# 参考数据
## 分区id
分区id|分区名|参考视频数
---|:--:|---:
12|<unnamed>|1
16|<unnamed>|1674
17|单机游戏|4619262
19|Mugen|72150
20|宅舞|169883
21|日常|4561408
22|鬼畜调教|118462
24|MAD·AMV|348606
25|MMD·3D|385817
26|音MAD|51707
27|综合|823079
28|原创音乐|45282
29|音乐现场|507884
30|VOCALOID·UTAU|197616
31|翻唱|678780
32|完结动画|15889
33|连载动画|25896
37|人文·历史|90880
39|演讲• 公开课|662700
41|<unnamed>|2
43|<unnamed>|1
46|<unnamed>|25
47|短片·手书·配音|242761
50|<unnamed>|1
51|资讯|22952
53|<unnamed>|161
54|OP/ED/OST|320
56|<unnamed>|4
59|演奏|559064
60|<unnamed>|1
63|<unnamed>|2
65|网络游戏|3120252
67|<unnamed>|127
71|综艺|781218
74|<unnamed>|541
75|动物圈|895904
76|美食圈|843589
77|<unnamed>|7
79|<unnamed>|3
80|<unnamed>|14
82|<unnamed>|696
83|其他国家|132
85|短片|310021
86|特摄|128915
94|<unnamed>|3
95|手机平板|273307
96|星海|115603
98|机械|197551
114|<unnamed>|1
116|<unnamed>|1
118|<unnamed>|1
120|<unnamed>|2
121|GMV|136090
122|野生技术协会|450310
124|趣味科普人文|431702
125|<unnamed>|10
126|人力VOCALOID|30570
127|教程演示|1239
128|<unnamed>|2340
130|音乐综合|997474
131|Korea相关|1319188
132|<unnamed>|2
134|<unnamed>|2
135|<unnamed>|15
136|音游|382552
137|明星|1891614
138|搞笑|966316
139|<unnamed>|10
140|<unnamed>|1
141|<unnamed>|3
142|<unnamed>|1
143|<unnamed>|2
145|欧美电影|891
146|日本电影|95
147|国产电影|3884
152|官方延伸|129248
153|国产动画|13416
154|三次元舞蹈|296980
156|舞蹈教程|27794
157|美妆|466928
158|服饰|175771
159|T台|21836
161|手工|498822
162|绘画|414602
163|运动|713928
164|健身|109358
166|广告|177150
168|国产原创相关|95777
169|布袋戏|26372
170|资讯|6646
171|电子竞技|2238886
172|手机游戏|3821050
173|桌游棋牌|337709
174|其他|1154288
175|ASMR|68
176|汽车|279524
178|科学·探索·自然|38250
179|军事|14365
180|社会·美食·旅行|102552
182|影视杂谈|332506
183|影视剪辑|2050261
184|预告 资讯|291825
185|国产剧|4826
186|港台剧|1
187|海外剧|1392
189|电脑装机|100080
190|摄影摄像|68519
191|影音智能|37262
192|风尚标|52235
193|MV|296537
194|电音|134399
195|动态漫·广播剧|22596
