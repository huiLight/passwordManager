from tkinter import *
import tkinter.font
import sqlite3
import random
#别忘了加上过滤语句，防止sql注入

class Encrypt:
	import random

	@staticmethod
	def rand(times=0):
		s = ""
		list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '%', '=']
		for i in range(0, times):
			rnum = random.randint(0,3)
			if rnum == 0:
				s += list[random.randint(0, 11)]
			elif rnum == 1 or rnum == 2:
				s += chr(random.randint(65, 90))
			else:
				s += chr(random.randint(97, 122))

		return s

	@staticmethod
	def c(ch, i, mod, j):
		ch = ord(ch)
		ch = (ch + i) % (ord(mod)+1)
		if ch < ord(j):
			ch += ord(j)
		return chr(ch)


	def en(self, str):

		for i in range(0, len(str)):
			ch = str[i]
			if ch >= 'a' and ch <= 'z':
				str = str[0:i] + Encrypt.c(ch, 5, 'z', 'a') + str[i+1:]
			elif ch >='A' and ch <= 'Z':
				str = str[0:i] + Encrypt.c(ch, 2, 'Z', 'A')  + str[i+1:]
			elif ch >='0' and ch <= '9':
				str = str[0:i] + Encrypt.c(ch, len(str)%10, '9', '0')  + str[i+1:]
			# else:
			# 	if ch != '/' and ch != '@' and ch != '`':
			# 		str = str[0:i] + c(ch, 1, '~', '!')  + str[i+1:]
		str = Encrypt.rand(5) + str[0:1] + Encrypt.rand(2) + str[1:4] + Encrypt.rand(1) + str[4:5] \
			+ Encrypt.rand(2) + str[5:-1] + Encrypt.rand(1) + str[-1:] + Encrypt.rand(1)
		return str

	def un(self, str):
		str = str[5:-1]
		str = str[0:1] + str[3:6] + str[7:8] + str[10:-2] + str[-1:]
		for i in range(0, len(str)):
			ch = str[i]
			if ch >= 'a' and ch <= 'z':
				str = str[0:i] + Encrypt.c(ch, 26-5, 'z', 'a') + str[i+1:]
			elif ch >='A' and ch <= 'Z':
				str = str[0:i] + Encrypt.c(ch, 26-2, 'Z', 'A') + str[i+1:]
			elif ch >='0' and ch <= '9':
				str = str[0:i] + Encrypt.c(ch, 10-len(str)%10, '9', '0') + str[i+1:]
			# else:
			# 	if ch != '/' and ch != '@' and ch != '`':
			# 		str = str[0:i] + c(ch, 94-1, '~', '!') + str[i+1:]

		return str

class StatuBar(Frame):
	"""docstring for StatuBar"""
	def __init__(self, master):
		super().__init__(master)
		self.label = Label(self, bd=1, relief=SUNKEN, padx=8, anchor=W)
		self.label.pack(fill=X)

	def set(self, format, *arg):
		self.label.config(text=format%arg)
		self.label.update_idletasks()

	def clear(self):
		self.label.config(text="")
		self.label.update_idletasks()

class SearchBar(Frame):
		
		def __init__(self, master):
			super().__init__(master)
			
			ft = tkinter.font.Font(self, family="Times", size=15, weight=tkinter.font.BOLD)
			
			self.all = Button(self, text="All", bg="#ff8832", fg="green", bd=0, font=ft, cursor="hand2", command=self.lookAll)
			self.all.pack(side=LEFT, padx=2)

			self.add = Button(self, text="Add", bg="#ff8832", fg="green", bd=0, font=ft, cursor="hand2", command=self.addNew)
			self.add.pack(side=LEFT, padx=2)

			self.delete = Button(self, text="Del", bg="#ff8832", fg="green", bd=0, font=ft, cursor="hand2", command=self.delOne)
			self.delete.pack(side=LEFT, padx=2)

			self.chg = Button(self, text="Chg", bg="#ff8832", fg="green", bd=0, font=ft, cursor="hand2", command=self.chgpw)
			self.chg.pack(side=LEFT, padx=2)
			
			self.go = Button(self, text="Go", bg="#ff8832", fg="green", bd=0, font=ft, cursor="hand2", command=self.sear)
			self.go.pack(side=RIGHT, padx=2)
			
			self.entry = Entry(self)
			self.entry.bind("<Return>", self.sear)
			self.entry.pack(side=RIGHT)

		def sear(self, event=None):
			content.clean()
			s = self.entry.get()
			statubar.set("正在搜索: %s",s)

			if s=="":
				statubar.set("输入不能为空")
				return
			con.select(s)
			statubar.set("就绪")
			
			self.entry.delete(0, END)
			self.entry.update_idletasks()

		def lookAll(self):
			content.clean()
			con.select('')

		def addNew(self):
			self.top = Toplevel()

			f1 = Frame(self.top)
			pfl = Label(f1, text="平台:")
			pfl.grid(row=1,column=1)
			self.pf = Entry(f1)
			self.pf.grid(row=1,column=2, padx=2)
			f1.grid(row=1,column=1,columnspan=2, pady = 4)

			f2 = Frame(self.top)
			unl = Label(f2, text="账号:")
			unl.grid(row=2,column=1)
			self.un = Entry(f2)
			self.un.grid(row=2,column=2, padx=2)
			f2.grid(row=2,column=1,columnspan=2)

			f3 = Frame(self.top)
			pwl = Label(f3, text="密码:")
			pwl.grid(row=3,column=1)
			self.pw = Entry(f3)
			self.pw.bind("<Return>", self.do)
			self.pw.grid(row=3,column=2, padx=2)
			f3.grid(row=3,column=1,columnspan=2)

			f4 = Frame(self.top)
			bt = Button(f4, text="Add", command=self.do)
			bt.grid(row=4,column=2)
			f4.grid(row=4,column=1,columnspan=2)

			# statubar = StatuBar(self.top)
			# statubar.grid(row=5, column=1)
		def do(self, event=None):
			pf = self.pf.get()
			un = self.un.get()
			pw = self.pw.get()

			if pf=="" or un=="" or pw=="":
				statubar.set("错误！输入不能为空！")
				return

			con.insert(pf, un, pw)
			statubar.set("Success")
			self.top.destroy()

		def delOne(self):
			self.top = Toplevel()
			f1 = Frame(self.top)
			pfl = Label(f1, text="平台:")
			pfl.grid(row=0,column=0)
			pf = Entry(f1)
			pf.grid(row=0,column=1, padx=1)
			f1.grid(row=0,column=0,columnspan=1, pady = 4)

			f2 = Frame(self.top)
			unl = Label(f2, text="账号:")
			unl.grid(row=1,column=0)
			un = Entry(f2)
			un.bind("<Return>", lambda e :  con.delete(pf.get(), un.get()))
			un.grid(row=1,column=1, padx=1)
			f2.grid(row=1,column=0,columnspan=2)

		def chgpw(self):
			self.top = Toplevel()

			f1 = Frame(self.top)
			pfl = Label(f1, text="平台:")
			pfl.grid(row=1,column=1)
			pf = Entry(f1)
			pf.grid(row=1,column=2, padx=2)
			f1.grid(row=1,column=1,columnspan=2, pady = 4)

			f2 = Frame(self.top)
			unl = Label(f2, text="账号:")
			unl.grid(row=2,column=1)
			un = Entry(f2)
			un.grid(row=2,column=2, padx=2)
			f2.grid(row=2,column=1,columnspan=2)

			f3 = Frame(self.top)
			pwl = Label(f3, text="密码:")
			pwl.grid(row=3,column=1)
			pw = Entry(f3)
			pw.bind("<Return>", lambda e : con.update(pf.get(), un.get(), pw.get()))
			pw.grid(row=3,column=2, padx=2)
			f3.grid(row=3,column=1,columnspan=2)



class Line(Frame):

	def __init__(self, master, **args):
		super().__init__(master)
		self.l1 = Label(self, text=args["l1"], width=10, bd=1)
		self.l1.bind("<Button-3>", self.rightKey)
		self.l1.pack(side=LEFT)
		self.l2 = Label(self, text=args["l2"], width=20, bd=1)
		self.l2.pack(side=LEFT)
		self.l3 = Label(self, text=args["l3"], width=20, bd=1)
		self.l3.pack(side=LEFT)
		self.l4 = Label(self, text=args["l4"], width=20, bd=1)
		self.l4.pack(side=LEFT)

	def set(self, **args):
		self.l1.config(text=args["l1"])
		self.l2.config(text=args["l2"])
		self.l3.config(text=args["l3"])
		self.l4.config(text=args["l4"])

	def setBG(self, color):
		self.l1.config(bg=color)
		self.l2.config(bg=color)
		self.l3.config(bg=color)
		self.l4.config(bg=color)

	def rmenu(self):
		menu = Menu(self, tearoff=False)
		menu.add_command(label="修改")
		menu.add_command(label="删除")
		return menu
	def rightKey(self, event):
		self.rmenu().post(event.x_root, event.y_root)

class Content(Frame):
	count = 0
	def __init__(self, master):
		self.master = master
		super().__init__(master)
		self.l1 = Line(self, l1="序号", l2="平台", l3="账号", l4="密码")
		self.l1.pack()
		self.lines = []

	def add(self, **args):
		self.lines.append(Line(self, l1=str(Content.count+1), **args))
		if Content.count % 2 == 0:
			self.lines[Content.count].setBG("#FFFFFF")
		self.lines[Content.count].update_idletasks()
		self.lines[Content.count].pack()
		Content.count += 1

	def clean(self):
		for r in self.lines:
			r.pack_forget()
		self.lines = [] #清空
		Content.count = 0




class Database:
	""" pf -> platform
		un -> uname
		pw -> password
	"""
	count = 0
	def __init__(self):
		self.con = Database.openDatabase()
		c = self.con.execute("SELECT count(*) from user;")
		for r in c:
			Database.count = r[0]

	def select(self, pf):
		cursor = self.con.execute("select * from user where platform LIKE('%%%s%%');"%pf)
		data = []
		for row in cursor:
			for c in row:
				data.append(c)
			content.add(l2=data[1], l3=data[2], l4=encrypt.un(data[3]))
			data=[] #要清空，否则还会输出第一条信息

	def insert(self, pf, un, pw):
		Database.count += 1
		self.con.execute("INSERT INTO user VALUES(%d, '%s', '%s', '%s')"%(Database.count, pf, un, encrypt.en(pw)))
		self.con.commit()

	def delete(self, pf, un):
		self.con.execute("DELETE FROM user WHERE platform='%s' AND uname='%s'"%(pf, un))
		self.con.commit()

	def update(self, pf, un, pw):
		self.con.execute("UPDATE user SET password='%s' WHERE platform='%s' AND uname='%s'"%(encrypt.en(pw), pf, un))
		self.con.commit()

	@staticmethod
	def openDatabase():
		import os
		if os.path.exists("data.db"):
			return sqlite3.connect("data.db")
		else:
			con = sqlite3.connect("data.db")
			con.execute("""CREATE TABLE user(
							id int primary key,
							platform char(30) not null,
							uname char(30) not null,
							password char(70) not null);""")
			return con


def jm(str):
	#字母位移， 数字更改， 标点更改
	for i in range(0,len(str)):
		if str[i] >= 'a' and str[i] <= 'z':
			str[i] = str[i] + 2 % 122 +97


def main():
	global root
	root = Tk()
	root.config(bg="#ffffff")
	root.wm_minsize(450, 400)
	root.wm_title("PasswordManger")

	global encrypt
	encrypt = Encrypt()

	global search
	search = SearchBar(root)
	search.config(bg="#ff8832")
	search.pack(fill=X)

	global content
	content = Content(root)
	content.pack(fill=X)

	global con
	con = Database()

	global statubar
	statubar = StatuBar(root)
	statubar.pack(side=BOTTOM, fill=X)

	root.mainloop()

def check(event=None):
	if mm.get() == "123":
		bstatu.set("Success")
		login.destroy()
		main()
	else:
		bstatu.set("密码错误")


login = Tk()
#login.wm_minsize(220,150)
login.wm_title("Login")
ft = tkinter.font.Font(login, family="Times", size=15, weight=tkinter.font.BOLD)

lb = Label(login, bg="#ff3355",text="Welcome",font=ft, height=2, bd=0)
lb.pack(fill=X)


mf = Frame(login, height=2, bg="#ff5544", bd=0)
lb = Label(mf, text="Password:", bg="#ff5533", font="Times", height=2, bd=0)
lb.pack(side=LEFT)
mm = Entry(mf, show="*")
mm.bind("<Return>", check)
mm.pack(pady=10, padx=4)
mf.pack(fill=X)

bf = Frame(login)
blogin = Button(bf, text="GO", width=15, bd=0, font=ft, fg="green", command=check)
blogin.pack()
bf.pack(fill=X)

bstatu = StatuBar(login)
bstatu.pack(side=BOTTOM, fill=X)
login.mainloop()