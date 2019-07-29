# coding=utf-8 #
import argparse

def start():
    #av号解析函数
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
        #输出格式：tuple(分区id,分区名)
        return (str_clip(content,r'"tid":',r','),str_clip(content,r'"tname":"',r'",'))



    #开始解析参数
    parser = argparse.ArgumentParser(add_help=False)
    parser.description='输入参数或指定配置文件以配置BiliSpider'
    parser.add_argument("-h","--help",help="打印此信息并退出",action='store_true')
    parser.add_argument("-t","--tid", help="通过分组id进行爬取 可使用逗号连接多个tid，如：1,2,3",type=str)
    parser.add_argument("-u","--url", help="通过视频网址或av号自动识别分区并爬取 注意：仅在无(--tid,-t)时生效",type=str)
    parser.add_argument("-lc","--loadconfig",metavar="FILE_PATH",help="指定配置文件 注意：单独指定的参数将覆盖配置文件参数",type=str)
    parser.add_argument("--output",help="指定控制台输出模式：0-无输出；1-进度条模式；2-输出日志",type=int,choices=(0,1,2),default=1)
    parser.add_argument("--logmode",help="指定日志保存模式：0-不保存；1-仅保存错误；2-保存所有输出",type=int,choices=(0,1,2),default=1)
    parser.add_argument("--debug",help="启用调试",action='store_true')
    parser.add_argument("--saveconfig","-sc",metavar="FILE_PATH",help="根据参数保存配置文件并退出",type=str)
    parser.add_argument("--thread_num","-tn",help="指定线程数，默认为2",default=2,type=int)
    parser.add_argument("--gui","-g",help="打开可视化界面",action='store_true')
    parser.add_argument("--safemode",help="安全模式",action='store_true')
    args = parser.parse_args()
    config = dict(vars(args))

    if args.help:
        parser.print_help()
        exit()

    if args.safemode:
        print("进入安全模式后，仅使用单线程和必要模块，除tid外的参数将被忽略，可以减少资源消耗和被封禁IP的风险，但效率会变低")
        if input("输入Y以进入安全模式:").lower() != 'y':
            pass
        else :
            print('你已进入安全模式')
            #TODO
        exit()

    if args.loadconfig:
        import json
        with open(args.config,"r") as f:
            config.update(json.loads(f.read()))
    del config['loadconfig']

    if args.gui:
        from .gui import gui_config
        config = gui_config(config).get()
    else :
        del config['gui']

    if not config['tid'] and not args.url:
        parser.print_help()
        exit()


    if args.saveconfig:
        import json
        with open(args.saveconfig,'w') as f:
            del config['saveconfig']
            f.write(json.dumps(config))
    else :
        del config['saveconfig']

    if args.debug :
        config['output'] = 2

    if args.tid:
        #将获取的字符串以逗号拆分
        #再通过map函数迭代转化为int
        #转化为set以去除重复项
        config['tid'] = tuple(set(map(int,args.tid.split(','))))

    if args.url and not config['tid'] : 
        tid_info = get_tid_by_url(aid_decode(args.url))
        config['tid'] = int(tid_info[0])
        print('已获取 {} 分区tid: {}'.format(tid_info[1],tid_info[0]))
    del config['url']


    print(config)
    from .bilispider import spider
    for tid in config['tid']:
        #实例化
        spider = spider(tid,config)
        spider.auto_run()
