import os, sys
from tkinter import *
from tkinter import ttk

class stage_part:
    def __init__(self, types=None, num=None, row=None, column=None, appear_time=None, zombie_ls=None):
        self.types = types
        self.num = num
        self.row = row
        self.column = column
        self.appear_time = appear_time
        self.zombie_ls = zombie_ls


def zombie_get(name, row, column, appear_time):
    return f'get_zombies("{name}", {row}, {column}, {appear_time})'

def random_from(ls_text):
    return f'random.choice([{ls_text}])'

def get_whole_types(obj):
    whole = obj.normals + obj.waves
    whole_zombie_text = [x.zombie_ls.replace(' ','').split(',') if x.types == 1 else [y.name for y in x] for x in whole]
    whole_types = list(set([i for j in whole_zombie_text for i in j]))
    return whole_types

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.minsize(700, 600)
        self.title('关卡制作器')
        self.top_label = ttk.Label(self, text='在这里制作属于你自己的关卡')
        self.stage_name_text = ttk.Label(self, text='关卡名称：')
        self.stage_name = ttk.Entry(self, width=15)
        self.stage_name_text.place(x=500, y=0)
        self.stage_name.place(x=570, y=0)
        self.start_time_text = ttk.Label(self, text='僵尸出现时间：')
        self.start_time = ttk.Entry(self, width=8)
        self.start_time_text.place(x=500, y=30)
        self.start_time.place(x=600, y=30)
        self.saved_button = ttk.Button(self, text='生成关卡脚本', command=self.convert)
        self.saved_button.place(x=0, y=10)
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
        self.normals = [stage_part() for i in range(self.stage_num+1)]
        self.waves = [stage_part() for j in range(self.stage_num)]
        self.choose_stages_bar = Scrollbar(self)
        self.choose_stages_bar.place(x=170, y=210, height=180, anchor=CENTER)
        self.choose_stages_list = Listbox(self,
                                     yscrollcommand=self.choose_stages_bar.set)
        for k in range(self.stage_num*2):
            if k % 2 == 0:
                self.choose_stages_list.insert(END, f'第{k//2+1}波旗帜之前')
            else:
                self.choose_stages_list.insert(END, f'第{k//2+1}波旗帜')
        self.choose_stages_list.insert(END, f'第{self.stage_num}波旗帜之后')
        self.choose_stages_list.place(x=0, y=120)
        self.choose_stages_bar.config(command=self.choose_stages_list.yview)
        self.modify_button = ttk.Button(self, text='编辑此部分', command=self.modify)
        self.modify_button.place(x=200, y=140)
        self.num_of_zombies_text = ttk.Label(self, text='请输入这部分的僵尸数量')
        self.current_part = StringVar()
        self.show_current = ttk.Label(self, textvariable=self.current_part)
        self.num_of_zombies = ttk.Entry(self, width=8)
        self.num_of_zombies_confirm = ttk.Button(self, text='确定', command=self.num_of_zombies_set)
        self.num_of_zombies_save = ttk.Label(self, text='设置成功')
        self.show_current.place(x=0, y=320)
        self.ask_choose_mode_text = ttk.Label(self, text='僵尸种类随机从某几种里挑选还是一个一个写？')
        self.ask_choose_which = IntVar()
        self.ask_choose_mode_random = ttk.Radiobutton(self, text='随机', value=1, variable=self.ask_choose_which)
        self.ask_choose_mode_each = ttk.Radiobutton(self, text='一个一个写', value=2, variable=self.ask_choose_which)
        self.ask_choose_mode_confirm = ttk.Button(self, text='确定', command=self.zombie_choose_mode)
        self.random_choose_types_text = ttk.Label(self, text='请输入可选择的僵尸种类，用英文逗号隔开，比如： 普通僵尸, 路障僵尸')
        self.random_choose_types = ttk.Entry(self, width=50)
        self.random_choose_rows_text = ttk.Label(self, text='请输入僵尸会出现的所有行数，用英文逗号隔开，如果全部行数都出现请留空')        
        self.random_choose_rows = ttk.Entry(self, width=20)
        self.random_choose_types_confirm = ttk.Button(self, text='确定', command=self.random_choose_types_set)
        self.appear_times_text = ttk.Label(self, text='请输入僵尸出现的时间范围，格式：开始的秒数, 结束的秒数')        
        self.appear_times = ttk.Entry(self, width=20)
        self.config_text = ttk.Label(self, text='需要修改僵尸的参数请写在这里，多个参数请用英文逗号隔开')        
        self.config_options =  ttk.Entry(self, width=30)
        self.each_bar = Scrollbar(self)
        self.each_list = Listbox(self, yscrollcommand=self.each_bar.set)
        self.each_list.bind("<<ListboxSelect>>", lambda e: self.show_zombies())
        self.msg_var = StringVar()
        self.show_zombie_msg = ttk.Label(self, textvariable=self.msg_var)
        self.show_zombie_name = ttk.Label(self, text='当前僵尸的种类：')
    def refresh(self, obj):
        if obj.place_info():
            obj.place_forget()        
    def refresh_modify(self):
        self.refresh(self.random_choose_types_text)
        self.refresh(self.random_choose_types)
        self.refresh(self.random_choose_types_confirm)
        self.refresh(self.random_choose_rows_text)
        self.refresh(self.random_choose_rows)
        self.refresh(self.random_choose_types_confirm)
        self.refresh(self.appear_times_text)
        self.refresh(self.appear_times)
        self.refresh(self.config_text)
        self.refresh(self.config_options)
        self.refresh(self.each_bar)
        self.refresh(self.each_list)
        self.refresh(self.show_zombie_msg)
    def modify(self):
        self.refresh_modify()
        self.current_part.set(self.choose_stages_list.get(ACTIVE))        
        self.current_ind = self.choose_stages_list.index(ACTIVE)
        self.num_of_zombies_text.place(x=0, y=340)
        self.num_of_zombies.place(x=150, y=340)
        self.num_of_zombies_confirm.place(x=300, y=340)
        self.ask_choose_mode_text.place(x=0, y=370)
        self.ask_choose_mode_random.place(x=270, y=370)
        self.ask_choose_mode_each.place(x=330, y=370)
        self.ask_choose_mode_confirm.place(x=450, y=370)         
        self.current_obj = self.normals[self.current_ind // 2] if self.current_ind % 2 == 0 else self.waves[self.current_ind // 2]
        if not self.current_obj.types:
            self.ask_choose_which.set(0)         
        else:
            self.ask_choose_which.set(self.current_obj.types)  
        saved_num = self.current_obj.num
        self.num_of_zombies.delete(0, END)
        if saved_num:
            self.num_of_zombies.insert(END, saved_num) 
        self.random_choose_rows.delete(0, END)
        if self.current_obj.row:
            self.random_choose_rows.insert(END, self.current_obj.row)
        self.appear_times.delete(0, END)
        if self.current_obj.appear_time:
            self.appear_times.insert(END, self.current_obj.appear_time)        
        self.random_choose_types.delete(0, END)
        if self.current_obj.zombie_ls:
            self.random_choose_types.insert(END, self.current_obj.zombie_ls)                
    
    def num_of_zombies_set(self):
        try:
            current_num = int(self.num_of_zombies.get())
            self.current_obj.num = current_num
            self.num_of_zombies_save.place(x=400, y=340)
            self.after(1000, self.num_of_zombies_save.place_forget)
        except:
            pass
    def zombie_choose_mode(self):
        self.choose_mode = self.ask_choose_which.get()
        if self.choose_mode == 1:
            self.refresh(self.each_bar)
            self.refresh(self.each_list) 
            self.show_zombie_msg.place_forget()
            self.current_obj.types = 1
            self.random_choose_types.delete(0, END)
            if self.current_obj.zombie_ls:
                self.random_choose_types.insert(END, self.current_obj.zombie_ls)                
            self.random_choose_types_text.place(x=0, y=400)
            self.random_choose_types.place(x=0, y=420)
            self.random_choose_types_confirm.place(x=400, y=420)
            self.random_choose_rows_text.place(x=0, y=450)
            self.random_choose_rows.place(x=0, y=470)
            self.appear_times_text.place(x=0, y=490)
            self.appear_times.place(x=0, y=510)
            self.config_text.place(x=0, y=530)
            self.config_options.place(x=0, y=550)
        elif self.choose_mode == 2:
            self.refresh(self.random_choose_types_text)
            self.refresh(self.random_choose_types)
            self.refresh(self.random_choose_types_confirm)
            self.refresh(self.random_choose_rows_text)
            self.refresh(self.random_choose_rows)
            self.refresh(self.random_choose_types_confirm)
            self.refresh(self.appear_times_text)
            self.refresh(self.appear_times)     
            self.refresh(self.config_text)
            self.refresh(self.config_options)            
            self.current_obj.types = 2
            if self.current_obj.num:
                self.each_bar.place(x=170, y=450, height=70, anchor=CENTER)
                for k in range(self.current_obj.num):
                    self.each_list.insert(END, f'第{k+1}只僵尸')
                self.each_list.place(x=0, y=400)
                self.each_bar.config(command=self.each_list.yview)
            else:
                current_msg = ttk.Label(self, text='您还没有设置僵尸数量')
                current_msg.place(x=450, y=300)
                self.after(1000, current_msg.place_forget)
            
    def random_choose_types_set(self):
        current_ls = self.random_choose_types.get()
        appear_rows = self.random_choose_rows.get()
        appear_times = self.appear_times.get()
        self.current_obj.zombie_ls =  current_ls
        self.current_obj.row = appear_rows
        self.current_obj.column = 'map_size[1]-1'
        self.current_obj.appear_time = appear_times
        self.num_of_zombies_save.place(x=500, y=420)
        self.after(1000, self.num_of_zombies_save.place_forget)
    
    def show_zombies(self):
        self.msg_var.set(self.each_list.get(ANCHOR))
        self.show_zombie_msg.place(x=400,y=420)
    
    def convert(self):
        pass

def get_rows(appear_rows):
    if not appear_rows:
        appear_rows = 'random.randint(0, map_size[0]-1)'
    else:
        try:
            appear_rows = appear_rows.replace(' ', '').split(',')
            if len(appear_rows) == 1:
                appear_rows = str(appear_rows[0])
            else:
                appear_rows = f'random.choice({[int(i) for i in appear_rows]})'
        except:
            appear_rows = 'random.randint(0, map_size[0]-1)'    
    return appear_rows
def get_appear_times(appear_time):
    return f'random.randint({appeat_times})'
root = Root()

root.mainloop()
