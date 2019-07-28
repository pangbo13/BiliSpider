# coding=utf-8 #
import argparse

def start():
    #av号解析函数
    def aid_decode(url):
        class URL_ERROR(Exception):
            def __init__(self):
                super().__init__()
                self.args = ('无法识别av号',)
                self.code = '101'
    
        url = url.lower()
        if url.isdigit():
            url = r'https://www.bilibili.com/video/av' + url
        elif url[:2] == 'av':
            if not url[2:].isdigit():
                raise URL_ERROR()
            url = r'https://www.bilibili.com/video/' + url
        elif 'av' in url :
            url = filter(lambda x : 'av' in x ,url.split(r'/'))
            url = tuple(url)[0]
            print(url)
            if url[:2] != 'av' :
                raise URL_ERROR()
            if url[2:].isdigit():
                raise URL_ERROR()
            url = r'https://www.bilibili.com/video/' + url
        else:
            raise URL_ERROR()
        return url

    def get_tid_by_url(url):
        def str_clip(content,start_str,end_str):
            start = content.find(start_str) + len(start_str)
            end = content.find(end_str,start)
            if start == -1 or end == -1:
                return None
            return content[start:end]
        import requests
        from headers import Page_headers as headers
        content = requests.get(url,headers=headers).content.decode('utf-8')
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
        gui_config()
    else :
        del config['gui']

    if not args.tid and not args.url:
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
        config['tid'] = tuple(set(map(int,args.tid.split(','))))

    if args.url and not args.tid : 
        tid_info = get_tid_by_url(aid_decode(args.url))
        config['tid'] = int(tid_info[0])
        print('已获取 {} 分区tid: {}'.format(tid_info[1],tid_info[0]))
    del config['url']


    print(config)
    from .bilispider import spider
    for tid in config['tid']:
        spider = spider(tid,config)
        spider.auto_run()
