import tkinter as tk
from tkinter import ttk

class gui_config():
	def __init__(self,config={}):
		def set_config():
			config['tid'] = tid_entry.get()
			config['output'] = int(output_choice.get())
			config['logmode'] = int(logmode_choice.get())
			config['thread_num'] = int(thread_num.get())
			root.quit()
	
		def get_tid():
			tid_info_label.config(text = '正在获取')
			try:
				from .tools import get_tid_by_url,aid_decode
				tid_entry.delete(0,tk.END)
				info = get_tid_by_url(aid_decode(url_entry.get()))
				tid_entry.insert(0,int(info[0]))
				tid_info_label.config(text = '分区名:' + info[1] + ',id:' + info[0])
			except:
				tid_info_label.config(text = '获取失败')

		def show_more_or_less():
			if show_more_choice.get():
				ad_frame.pack(after=es_frame)
			else:
				ad_frame.forget()

		def show_thread_num(var):
			thread_num_label.config(text=str(thread_num.get()))

		root = tk.Tk()
		self.root = root
		root.title('设置')

		show_more_choice = tk.IntVar(root,value=0)

		#显示基本选项
		es_frame = tk.Frame(root)
		ttk.Label(es_frame,text="分区id").grid(row=0,sticky=tk.E,padx=0)
		ttk.Label(es_frame,text="从url识别").grid(row=1,sticky=tk.E,padx=0)
		tid_entry = ttk.Entry(es_frame)
		tid_entry.grid(row=0,column=1,sticky=tk.W)
		url_entry = ttk.Entry(es_frame,width=40)
		url_entry.grid(row=1,column=1,columnspan=3,sticky=tk.W)
		ttk.Button(es_frame,text='确认',width=5,command=get_tid).grid(row=0,column=1,sticky=tk.E)
		tid_info_label = ttk.Label(es_frame)
		tid_info_label.grid(row=0,column=2,padx=10,sticky=tk.W)
		es_frame.columnconfigure(0,minsize=80)
		es_frame.columnconfigure(1,minsize=200)
		es_frame.columnconfigure(2,minsize=120)
		es_frame.pack()

		#高级选项
		ad_frame = tk.Frame(root)
		logmode_choice = tk.IntVar(root,value=config.get('logmode',2)-1)
		output_choice = tk.IntVar(root,value=config.get('output',2)-1)
		thread_num = tk.IntVar(root,value=config.get('thread_num',2))

		ttk.Separator(ad_frame,orient=tk.HORIZONTAL).grid(row=0,column=0,columnspan=4,sticky="we",pady=8,padx=0)
		ttk.Label(ad_frame,text='日志模式').grid(row=1,column=0,padx=(0,10))
		ttk.Label(ad_frame,text='输出模式').grid(row=2,column=0,padx=(0,10))

		logmode_description = ('无输出','进度条模式','输出日志')
		for i in range(3):
			ttk.Radiobutton(ad_frame,text=logmode_description[i],variable=logmode_choice,value=i).grid(row=1,column=i+1,stick=tk.W)

		output_description = ('不保存','仅保存错误','保存所有输出')
		for i in range(3):
			ttk.Radiobutton(ad_frame,text=output_description[i],variable=output_choice,value=i).grid(row=2,column=i+1,stick=tk.W)
		ttk.Label(ad_frame,text='线程数').grid(row=3,column=0)
		ttk.Scale(ad_frame, from_=1, to=10,length=150,variable=thread_num,command=show_thread_num).grid(row=3,column=1,columnspan=2)
		thread_num_label = tk.Label(ad_frame,text='2')
		thread_num_label.grid(row=3,column=3)
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