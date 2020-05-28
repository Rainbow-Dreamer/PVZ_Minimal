import os, sys
from tkinter import *
from tkinter import ttk
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.minsize(700, 500)
        self.title('关卡制作器')
        self.top_label = ttk.Label(self, text='在这里制作属于你自己的关卡')
        self.top_label.place(x=250, y=0)
        self.choose_num_text = ttk.Label(self, text='请先在这里输入你的关卡的旗帜数（有几个大波）')
        self.choose_num_text.place(x=0, y=60)
        self.choose_num_label = ttk.Entry(self)
        self.choose_num_label.place(x=270, y=60)
        self.choose_num_confirm = ttk.Button(self, text='确定', command=self.read_num)
        self.choose_num_confirm.place(x=450, y=58)
        self.choose_num_error = ttk.Label(self, text='请输入一个正整数')
        self.stage_num_text = StringVar()
        self.show_stage_num = ttk.Label(self, textvariable=self.stage_num_text)
        self.generate_stages = ttk.Button(self, text='产生关卡列表', command=self.generate)
    def read_num(self):
        self.stage_num = self.choose_num_label.get()
        try:
            self.stage_num = int(self.stage_num)
            if self.choose_num_error.place_info():
                self.choose_num_error.place_forget()
            self.stage_num_text.set(f'当前关卡的旗帜数: {self.stage_num}')
            self.show_stage_num.place(x=0, y=92)
            self.generate_stages.place(x=150, y=90)
        except:
            if self.show_stage_num.place_info():
                self.show_stage_num.place_forget()
            if self.generate_stages.place_info():
                self.generate_stages.place_forget()
            self.choose_num_label.delete(0, END)
            self.choose_num_error.place(x=0, y=92)
    def generate(self):
        self.choose_num_confirm.destroy()
        self.choose_num_text.destroy()
        self.choose_num_label.destroy()
        self.generate_stages.destroy()
        self.choose_stages_bar = Scrollbar(self)
        self.choose_stages_bar.place(x=170, y=210, height=180, anchor=CENTER)
        self.choose_stages_list = Listbox(self,
                                     yscrollcommand=self.choose_stages_bar.set)
        for k in range(self.stage_num*2 + 1):
            if k % 2 == 0:
                self.choose_stages_list.insert(END, f'第{k%2 + 1}波旗帜之前')
            else:
                self.choose_stages_list.insert(END, f'第{k%2 + 1}波旗帜')
        self.choose_stages_list.place(x=0, y=120)
        self.choose_stages_bar.config(command=self.choose_stages_list.yview)
        self.modify_button = ttk.Button(self, text='编辑此部分', command=self.modify)
        self.modify_button.place(x=230, y=260)
    def modify(self):
        pass
        

root = Root()

root.mainloop()
