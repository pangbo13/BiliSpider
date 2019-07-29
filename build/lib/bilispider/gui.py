import tkinter as tk

class gui_config():
	def __init__(self,config={}):
		def set_tid():
			config['tid'] = tid_entry.get()
			root.quit()
	
		def get_tid():
			tid_info_label['text']='正在获取'
			from .tools import get_tid_by_url,aid_decode
			tid_entry.delete(0,tk.END)
			info = get_tid_by_url(aid_decode(url_entry.get()))
			tid_entry.insert(0,int(info[0]))
			tid_info_label['text']='分区名:' + info[1] + ',id:' + info[0]

		root = tk.Tk()
		self.root = root
		root.title('设置')

		es_frame = tk.Frame(root)
		tk.Label(es_frame,text="分区id").grid(row=0,sticky=tk.E,padx=0)
		tk.Label(es_frame,text="从url识别").grid(row=1,sticky=tk.E,padx=0)
		tid_entry = tk.Entry(es_frame)
		tid_entry.grid(row=0,column=1,sticky=tk.W)
		url_entry = tk.Entry(es_frame)
		url_entry.grid(row=1,column=1,columnspan=3,ipadx=100)
		tk.Button(es_frame,text='确认',command=get_tid).grid(row=0,column=1,sticky=tk.E)
		tid_info_label = tk.Label(es_frame)
		tid_info_label.grid(row=0,column=3,sticky=tk.W)
		# tid_info_label['text']='sd'
		# tid_entry.delete(0,tk.END)
		# tid_entry.insert(0,'sd')
		es_frame.pack()
		buttom_frame = tk.Frame(root)
		tk.Button(buttom_frame,text='开始',width=10,command=set_tid).pack(side=tk.RIGHT,fill=tk.X,padx=50)
		tk.Button(buttom_frame,text='退出',width=10,command=exit).pack(side=tk.RIGHT,fill=tk.X,padx=50)
		buttom_frame.pack()
		root.mainloop()

		self.config = config

	def get(self):
		return self.config

if __name__ == '__main__':
	print(gui_config().get())