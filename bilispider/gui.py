import tkinter as tk
from tkinter import ttk

class gui_config():
	def __init__(self,config={}):
		def set_config():
			config['tid'] = int(tid_entry.get().split(" - ")[0])
			config['output'] = int(output_choice.get())
			config['logmode'] = int(logmode_choice.get())
			config['thread_num'] = int(thread_num.get())
			config['http'] = int(http_port.get())
			config['debug'] = bool(debug_switch.get())
			root.quit()
	
		def get_tid(event):
			tid_info_label.config(text = '正在获取')
			try:
				from .tools import get_tid_by_url,aid_decode
				info = get_tid_by_url(aid_decode(url_entry.get()))
				assert len(info[0])<40
				tid_entry.delete(0,tk.END)
				tid_entry.insert(0," - ".join(info))
				tid_info_label.config(text = "获取成功")
			except:
				tid_info_label.config(text = '获取失败')

		def show_more_or_less():
			if show_more_choice.get():
				ad_frame.pack(after=es_frame)
			else:
				ad_frame.forget()

		def show_thread_num(pos):
			thread_num_label.config(text=str(thread_num.get()))

		def set_port(pos):
			http_port.set(int(http_port.get()))

		def tid_entry_focusout(*args,**kwargs):
			if tid_entry.get().split("-")[0].strip().isdigit():
				tid = tid_entry.get().split("-")[0].strip()
				info = list(filter(lambda line:line[0]==tid,tid_inf))
				if len(info) == 0:
					return
				elif info[0][1]:
					tid_entry.delete(0,tk.END)
					tid_entry.insert(0," - ".join(info[0]))

		def tid_entry_focusin(event):
			tid_info_label.config(text="")

		def url_entry_focusin(event):
			url_entry.select_range(0,tk.END)
			tid_info_label.config(text="按下回车以获取tid")

		root = tk.Tk()
		self.root = root
		root.title('设置')

		show_more_choice = tk.IntVar(root,value=0)

		#显示基本选项
		es_frame = tk.Frame(root)
		ttk.Label(es_frame,text="分区id").grid(row=0,sticky=tk.E,padx=0)
		ttk.Label(es_frame,text="从url识别").grid(row=1,sticky=tk.E,padx=0)

		#加载tid输入框
		tid_entry = ttk.Combobox(es_frame,width =18)
		tid_entry.grid(row=0,column=1,sticky=tk.W)
		from .tools import load_tid_info
		tid_inf = load_tid_info()
		tid_option = tuple(" - ".join(line) for line in filter(lambda line:line[1],tid_inf))
		tid_entry.config(value=tid_option)
		tid_entry.insert(0,config.get('tid',None) if bool(config.get('tid',None)) else '')
		tid_entry_focusout()
		tid_entry.bind("<FocusOut>",tid_entry_focusout)
		tid_entry.bind("<FocusIn>",tid_entry_focusin)

		url_entry = ttk.Entry(es_frame,width=40)
		url_entry.grid(row=1,column=1,columnspan=3,sticky=tk.W)
		url_entry.bind("<Return>",get_tid)
		url_entry.bind("<FocusIn>",url_entry_focusin)

		tid_info_label = ttk.Label(es_frame)
		tid_info_label.grid(row=0,column=2,columnspan=2,padx=10,sticky=tk.W)
		es_frame.columnconfigure(0,minsize=80)
		es_frame.columnconfigure(1,minsize=100)
		es_frame.columnconfigure(2,minsize=120)
		es_frame.pack()

		#高级选项
		ad_frame = tk.Frame(root)
		logmode_choice = tk.IntVar(root,value=config.get('logmode',1))
		output_choice = tk.IntVar(root,value=config.get('output',1))
		thread_num = tk.IntVar(root,value=config.get('thread_num',2))
		http_port = tk.IntVar(root,value=config.get('http',1214))
		debug_switch = tk.BooleanVar(root,value=config.get('debug',False))
		#添加分割线
		ttk.Separator(ad_frame,orient=tk.HORIZONTAL).grid(row=0,column=0,columnspan=4,sticky="we",pady=8,padx=0)
		#添加标签控件
		ttk.Label(ad_frame,text='输出模式').grid(row=1,column=0,padx=(0,10))
		ttk.Label(ad_frame,text='日志模式').grid(row=2,column=0,padx=(0,10))
		ttk.Label(ad_frame,text='线程数').grid(row=3,column=0)
		ttk.Label(ad_frame,text='http服务器端口').grid(row=4,column=0,padx=(0,10))
		#日志模式单选按钮
		logmode_description = ('无输出','进度条模式','输出日志')
		for i in range(3):
			ttk.Radiobutton(ad_frame,text=logmode_description[i],variable=output_choice,value=i).grid(row=1,column=i+1,stick=tk.W)
		#输出模式单选按钮
		output_description = ('不保存','仅保存错误','保存所有输出')
		for i in range(3):
			ttk.Radiobutton(ad_frame,text=output_description[i],variable=logmode_choice,value=i).grid(row=2,column=i+1,stick=tk.W)
		#添加线程数滑动条
		ttk.Scale(ad_frame, from_=1, to=10,length=150,variable=thread_num,command=show_thread_num).grid(row=3,column=1,columnspan=2)
		thread_num_label = tk.Label(ad_frame,text='2')
		thread_num_label.grid(row=3,column=3)
		#添加端口输入框
		ttk.Scale(ad_frame, from_=0, to=2000,length=150,variable=http_port,command=set_port).grid(row=4,column=1,columnspan=2)
		ttk.Entry(ad_frame,textvariable=http_port,width=6).grid(row=4,column=3)
		#启用DEBUG
		ttk.Checkbutton(ad_frame,variable=debug_switch,text="启用DEBUG").grid(row=5,column=1,columnspan=2,stick='W')
		#高级选项结束

		buttom_frame = tk.Frame(root)
		ttk.Checkbutton(buttom_frame,text='展开高级选项',width=12,command=show_more_or_less,variable=show_more_choice).pack(side=tk.RIGHT,fill=tk.X,padx=(10,20))
		ttk.Button(buttom_frame,text='退出',width=8,command=exit).pack(side=tk.RIGHT,fill=tk.X,padx=(10,20))
		ttk.Button(buttom_frame,text='开始',width=8,command=set_config).pack(side=tk.RIGHT,fill=tk.X,padx=(60,20))
		buttom_frame.pack(pady=(7,5))
		root.mainloop()

		self.config = config

	def get(self):
		return self.config

if __name__ == '__main__':
	print(gui_config().get())