# coding=utf-8 #
import argparse

def start():
    '''
    命令行进入点，用于解析命令行参数
    '''
    
    #导入av号解析tid的函数
    from .tools import aid_decode,get_tid_by_url

    #开始解析参数
    parser = argparse.ArgumentParser(add_help=False)
    parser.description='输入参数或指定配置文件以配置BiliSpider'
    parser.add_argument("-h","--help",help="打印此信息并退出",action='store_true')
    parser.add_argument("-v","--version",help="显示版本",action='store_true')
    parser.add_argument("-t","--tid", help="通过分组id进行爬取 可使用逗号连接多个tid，如：1,2,3",type=str)
    parser.add_argument("-u","--url", help="通过视频网址或av号自动识别分区并爬取 注意：仅在无(--tid,-t)时生效",type=str)
    parser.add_argument("-lc","--loadconfig",metavar="FILE_PATH",help="指定配置文件 注意：单独指定的参数将覆盖配置文件参数",type=str)
    parser.add_argument("--output",help="指定控制台输出模式：0-无输出；1-进度条模式；2-输出日志",type=int,choices=(0,1,2),default=1)
    parser.add_argument("--logmode",help="指定日志保存模式：0-不保存；1-仅保存错误；2-保存所有输出",type=int,choices=(0,1,2),default=1)
    parser.add_argument("--debug",help="启用调试",action='store_true')
    parser.add_argument("--saveconfig","-sc",metavar="FILE_PATH",help="根据参数保存配置文件并退出",type=str)
    parser.add_argument("--thread_num","-tn",help="指定线程数，默认为2",default=2,type=int)
    parser.add_argument("--http", help="设置http状态数据发送端口，0为关闭，默认为1214，若检测到服务器未开启将启动内置服务器",type=int,default=1214)
    parser.add_argument("--gui","-g",help="打开可视化界面",action='store_true')
    parser.add_argument("--safemode",help="安全模式",action='store_true')
    args = parser.parse_args()
    config = dict(vars(args))

    if args.help:
        parser.print_help()
        return 1

    if args.version:
        from .version import version
        print(version)
        return 2

    if args.safemode:
        print("进入安全模式后，仅使用单线程和必要模块，除tid外的参数将被忽略，可以减少资源消耗和被封禁IP的风险，但效率会变低")
        from .safemode import safemode
        safemode(args.tid)
        return 3

    if args.loadconfig:
        import json
        with open(args.config,"r") as f:
            config.update(json.loads(f.read()))
    del config['loadconfig']

    if args.gui:
        from .gui import gui_config
        config.update(gui_config(config).get())
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

    if config.get('tid',False):
        #将获取的字符串以逗号拆分
        #再通过map函数迭代转化为int
        #转化为set以去除重复项
        config['tid'] = tuple(set(map(int,config['tid'].split(','))))

    if args.url and not config['tid'] : 
        tid_info = get_tid_by_url(aid_decode(args.url))
        config['tid'] = int(tid_info[0])
        print('已获取 {} 分区tid: {}'.format(tid_info[1],tid_info[0]))
    del config['url']


    print(config)
    from .bilispider import spider
    for tid in config['tid']:
        print('当前处理分区： ' + str(tid))
        #实例化
        s = spider(tid,config)
        s.auto_run()

    from .tools import check_update
    check_update()