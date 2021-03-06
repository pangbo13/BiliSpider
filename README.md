
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
+ 在终端使用`bilispider --gui`或`python -m bilispider --gui`(Linux下为`python3 -m bilispider --gui` )
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
+ `--thread_num`,`-n`：指定线程数，默认为2 
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
16|<unnamed>|1565
17|单机游戏|6221824
19|Mugen|89044
20|宅舞|184628
21|日常|7980247
22|鬼畜调教|145640
24|MAD·AMV|469464
25|MMD·3D|447616
26|音MAD|57434
27|综合|1187167
28|原创音乐|78235
29|音乐现场|864911
30|VOCALOID·UTAU|223511
31|翻唱|943664
32|完结动画|15471
33|连载动画|26777
37|人文·历史|114960
39|演讲• 公开课|1177670
41|<unnamed>|2
43|<unnamed>|1
46|<unnamed>|24
47|短片·手书·配音|340001
50|<unnamed>|1
51|资讯|30902
53|<unnamed>|156
54|OP/ED/OST|335
56|<unnamed>|4
59|演奏|859353
60|<unnamed>|1
63|<unnamed>|2
65|网络游戏|4390798
67|<unnamed>|124
71|综艺|1018459
74|<unnamed>|528
75|动物圈|1494771
76|美食圈|1335408
77|<unnamed>|7
79|<unnamed>|3
80|<unnamed>|14
82|<unnamed>|674
83|其他国家|127
85|短片|497145
86|特摄|188464
94|<unnamed>|3
95|手机平板|363292
96|星海|149167
98|机械|300963
114|<unnamed>|1
116|<unnamed>|1
118|<unnamed>|1
120|<unnamed>|2
121|GMV|187912
122|野生技术协会|676548
124|趣味科普人文|620610
125|<unnamed>|7
126|人力VOCALOID|37279
127|教程演示|1477
128|<unnamed>|2252
130|音乐综合|1265022
131|Korea相关|1708645
132|<unnamed>|2
134|<unnamed>|2
135|<unnamed>|14
136|音游|531930
137|明星|2666391
138|搞笑|1724096
139|<unnamed>|10
140|<unnamed>|1
141|<unnamed>|3
142|<unnamed>|1
143|<unnamed>|2
145|欧美电影|1161
146|日本电影|134
147|国产电影|3721
152|官方延伸|172077
153|国产动画|15262
154|舞蹈综合|189141
156|舞蹈教程|40732
157|美妆|642008
158|服饰|264172
159|T台|37156
161|手工|770090
162|绘画|721280
163|运动|1166346
164|健身|173115
166|广告|233056
168|国产原创相关|130812
169|布袋戏|31019
170|资讯|9240
171|电子竞技|3073928
172|手机游戏|6414333
173|桌游棋牌|554316
174|其他|2023313
175|ASMR|72
176|汽车|446090
178|科学·探索·自然|50397
179|军事|19674
180|社会·美食·旅行|175793
182|影视杂谈|462499
183|影视剪辑|3042705
184|预告 资讯|386427
185|国产剧|4826
186|港台剧|3
187|海外剧|1641
189|电脑装机|145668
190|摄影摄像|134530
191|影音智能|68526
192|风尚标|60105
193|MV|512412
194|电音|159584
195|动态漫·广播剧|19640
197|综合|988
198|街舞|167559
199|明星舞蹈|156726
