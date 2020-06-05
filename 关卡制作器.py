os.chdir('stages')


class stage_part:
    def __init__(self,
                 types=None,
                 names=None,
                 num=None,
                 row=None,
                 column=None,
                 appear_time=None,
                 zombie_ls=None,
                 config=None,
                 probs=None):
        self.types = types
        self.names = names
        self.num = num
        self.row = row
        self.column = column
        self.appear_time = appear_time
        self.zombie_ls = zombie_ls
        self.config = config
        self.probs = probs


def zombie_get(name, row, column, appear_time, config):
    if column == '':
        column = 'map_size[1]-1'
    print(repr(column))
    result = f'get_zombies({name}, {row}, {column}, {appear_time})'
    if config:
        result += f'.configure({config})'
    return result


def get_whole_types(obj):
    whole = obj.normals + obj.waves
    whole_zombie_text = [
        x.names.replace(' ', '').split(',')
        for x in whole if x.types == 1 and x.names
    ] + [[y[0] for y in x.zombie_ls if y]
         for x in whole if x.types == 2 and x.zombie_ls]
    whole_types = list(set([i for j in whole_zombie_text for i in j]))
    return whole_types


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.minsize(700, 800)
        self.title('关卡制作器')
        self.normals = None
        self.waves = None
        self.top_label = ttk.Label(self, text='在这里制作属于你自己的关卡')
        self.stage_name_text = ttk.Label(self, text='关卡名称：')
        self.stage_name = ttk.Entry(self, width=15)
        self.stage_name_text.place(x=500, y=0)
        self.stage_name.place(x=570, y=0)
        self.start_time_text = ttk.Label(self, text='僵尸出现时间：')
        self.start_time = ttk.Entry(self, width=8)
        self.start_time_text.place(x=500, y=30)
        self.start_time.place(x=600, y=30)
        self.stage_info_text = ttk.Label(self, text='关卡说明：(不想写的话可以留空)')
        self.stage_info = ScrolledText(self, width=40, height=10)
        self.stage_info_text.place(x=300, y=100)
        self.stage_info.place(x=300, y=120)
        self.saved_button = ttk.Button(self,
                                       text='生成关卡脚本',
                                       command=self.convert)
        self.saved_button.place(x=0, y=10)
        self.top_label.place(x=250, y=0)
        self.choose_num_text = ttk.Label(self, text='请先在这里输入你的关卡的旗帜数（有几个大波）')
        self.choose_num_text.place(x=0, y=60)
        self.choose_num_label = ttk.Entry(self)
        self.choose_num_label.place(x=270, y=60)
        self.choose_num_confirm = ttk.Button(self,
                                             text='确定',
                                             command=self.read_num)
        self.choose_num_confirm.place(x=450, y=58)
        self.choose_num_error = ttk.Label(self, text='请输入一个正整数')
        self.stage_num_text = StringVar()
        self.show_stage_num = ttk.Label(self, textvariable=self.stage_num_text)
        self.generate_stages = ttk.Button(self,
                                          text='产生关卡列表',
                                          command=self.generate)
        self.make_maps_button = ttk.Button(self, text='定制地图', command=self.make_maps)
        self.make_maps_button.place(x=120, y=10)
        self.new_map_size = None
        self.read_new_map_size = None
        self.new_map = None
        self.new_map_show = None
    
    
    def make_maps(self):
        make_map_window = Toplevel(self)
        make_map_window.title('定制地图')
        make_map_window.minsize(600, 400)
        make_map_window.ask_map_size_text = ttk.Label(make_map_window, text='地图尺寸(格式：行数, 列数)')
        make_map_window.ask_map_size = ttk.Entry(make_map_window)
        if self.new_map_size:
            make_map_window.ask_map_size.insert(END, self.new_map_size)
        make_map_window.ask_map_size_text.place(x=0, y=0)
        make_map_window.ask_map_size.place(x=160, y=0)
        make_map_window.confirm = ttk.Button(make_map_window, text='保存', command=lambda: self.make_maps_confirm(make_map_window))
        make_map_window.confirm.place(x=0, y=250) 
        make_map_window.change_all_button = ttk.Button(make_map_window, text='全部变成', command=lambda: self.change_all(make_map_window))
        make_map_window.change_all_content = ttk.Entry(make_map_window, width=15)
        make_map_window.change_all_button.place(x=100, y=250) 
        make_map_window.change_all_content.place(x=200, y=250)
        make_map_window.change_button = ttk.Button(make_map_window, text='改变', command=lambda: self.changes(make_map_window))
        make_map_window.change_content = ttk.Entry(make_map_window, width=20)
        make_map_window.change_button.place(x=320, y=250) 
        make_map_window.change_content.place(x=420, y=250)
        make_map_window.change_format = ttk.Label(make_map_window, text='改变的格式为: r行数, 类型 (改变一整行), c列数, 类型 (改变一整列), \nr行数c列数, 类型 (改变第r行第c列), 以1作为起始。')
        make_map_window.change_format.place(x=0, y=300)
        make_map_window.new_map_content = Text(make_map_window, width=80, height=15)
        if self.new_map_show:
            make_map_window.new_map_content.insert(END, self.new_map_show)            
        make_map_window.new_map_content.place(x=0, y=30)
    
    def change_all(self, obj):
        content = obj.change_all_content.get()
        if content and self.read_new_map_size:
            rows, columns = self.read_new_map_size
            self.new_map = [[content for i in range(columns)] for j in range(rows)]
            obj.new_map_content.delete('1.0', END)
            enter_char = ',\n'
            self.new_map_show = f"[{enter_char.join([str(x) for x in self.new_map])}]"
            obj.new_map_content.insert(END, self.new_map_show)            
        
    
    def changes(self, obj):
        content = obj.change_content.get()
        if content and self.read_new_map_size and self.new_map:
            test = content.replace(' ', '').split(',')
            if len(test) == 2:
                correct = False
                read_type = 0
                places, types = test
                if places[0] == 'r':
                    if 'r' in places and 'c' in places:
                        rows, columns = places[1:].split('c')
                        if rows.isdigit() and columns.isdigit():
                            correct = True
                            read_type = 3
                            rows, columns = int(rows)-1, int(columns)-1
                            
                    else:
                        if places[1:].isdigit():
                            correct = True
                            read_type = 1
                            rows =  int(places[1:])-1
                elif places[0] == 'c':
                    if places[1:].isdigit():
                            correct = True
                            read_type = 2
                            columns =  int(places[1:])-1
                if correct:
                    if read_type == 1:
                        if 0 <= rows < self.read_new_map_size[0]:
                            self.new_map[rows] = [types for k in range(self.read_new_map_size[1])]
                            self.map_reinsert(obj)
                    elif read_type == 2:
                        if 0 <= columns < self.read_new_map_size[1]:
                            for each_row in self.new_map:
                                each_row[columns] = types
                            self.map_reinsert(obj)   
                    elif read_type == 3:
                        if 0 <= rows < self.read_new_map_size[0] and 0 <= columns < self.read_new_map_size[1]:
                            self.new_map[rows][columns] = types
                            self.map_reinsert(obj)   
                            
                            
                        
    def map_reinsert(self, obj):
        obj.new_map_content.delete('1.0', END)
        enter_char = ',\n'
        self.new_map_show = f"[{enter_char.join([str(x) for x in self.new_map])}]"
        obj.new_map_content.insert(END, self.new_map_show)                    
    
    def make_maps_confirm(self, obj):
        self.new_map_size = obj.ask_map_size.get()
        if self.new_map_size:
            new_map_size = self.new_map_size.replace(' ', '').split(',')
            if len(new_map_size) == 2:
                if new_map_size[0].isdigit() and new_map_size[1].isdigit():
                    rows, columns = int(new_map_size[0]), int(new_map_size[1])
                    if (not self.read_new_map_size) or (self.read_new_map_size and (rows, columns) != self.read_new_map_size):
                        self.read_new_map_size = rows, columns
                        self.new_map = [['day' for i in range(columns)] for j in range(rows)]
                        obj.new_map_content.delete('1.0', END)
                        enter_char = ',\n'
                        self.new_map_show = f"[{enter_char.join([str(x) for x in self.new_map])}]"
                        obj.new_map_content.insert(END, self.new_map_show)
        new_map_show = obj.new_map_content.get('1.0', END)
        if self.new_map_show != new_map_show:
            self.new_map_show = new_map_show
        
    
    def edit_map(self, obj):
        pass
        

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
        self.normals = [stage_part() for i in range(self.stage_num + 1)]
        self.waves = [stage_part() for j in range(self.stage_num)]
        self.choose_stages_bar = Scrollbar(self)
        self.choose_stages_bar.place(x=170, y=210, height=180, anchor=CENTER)
        self.choose_stages_list = Listbox(
            self, yscrollcommand=self.choose_stages_bar.set, exportselection=0)
        for k in range(self.stage_num * 2):
            if k % 2 == 0:
                self.choose_stages_list.insert(END, f'第{k//2+1}波旗帜之前')
            else:
                self.choose_stages_list.insert(END, f'第{k//2+1}波旗帜')
        self.choose_stages_list.insert(END, f'第{self.stage_num}波旗帜之后')
        self.choose_stages_list.place(x=0, y=120)
        self.choose_stages_bar.config(command=self.choose_stages_list.yview)
        self.choose_stages_list.bind("<<ListboxSelect>>",
                                     lambda e: self.modify())
        self.num_of_zombies_text = ttk.Label(self, text='请输入这部分的僵尸数量')
        self.current_part = StringVar()
        self.show_current = ttk.Label(self, textvariable=self.current_part)
        self.num_of_zombies = ttk.Entry(self, width=8)
        self.num_of_zombies_confirm = ttk.Button(
            self, text='确定', command=self.num_of_zombies_set)
        self.num_of_zombies_save = ttk.Label(self, text='设置成功')
        self.show_current.place(x=0, y=320)
        self.ask_choose_mode_text = ttk.Label(self,
                                              text='僵尸种类随机从某几种里挑选还是一个一个写？')
        self.ask_choose_which = IntVar()
        self.ask_choose_mode_random = ttk.Radiobutton(
            self, text='随机', value=1, variable=self.ask_choose_which)
        self.ask_choose_mode_each = ttk.Radiobutton(
            self, text='一个一个写', value=2, variable=self.ask_choose_which)
        self.ask_choose_mode_confirm = ttk.Button(
            self, text='确定', command=self.zombie_choose_mode)
        self.random_choose_types_text = ttk.Label(
            self, text='请输入可选择的僵尸种类，用英文逗号隔开，比如： 普通僵尸, 路障僵尸')
        self.random_choose_types = ttk.Entry(self, width=50)
        self.random_choose_rows_text = ttk.Label(
            self, text='请输入僵尸会出现的所有行数，用英文逗号隔开，如果全部行数都出现请留空')
        self.random_choose_rows = ttk.Entry(self, width=20)
        self.random_choose_types_confirm = ttk.Button(
            self, text='确定', command=self.random_choose_types_set)
        self.appear_times_text = ttk.Label(self,
                                           text='请输入僵尸出现的时间范围，格式：开始的秒数, 结束的秒数')
        self.appear_times = ttk.Entry(self, width=20)
        self.config_text = ttk.Label(
            self, text='需要修改僵尸的参数请写在这里，多个参数请用英文逗号隔开，格式：参数1=值1, 参数2=值2')
        self.config_options = ttk.Entry(self, width=30)
        self.prob_text = ttk.Label(self, text='如果需要设置每种僵尸出现的概率请写在这里，用英文逗号隔开')
        self.prob = ttk.Entry(self, width=30)
        self.each_bar = Scrollbar(self)
        self.each_list = Listbox(self,
                                 yscrollcommand=self.each_bar.set,
                                 exportselection=0)
        self.each_list.bind("<<ListboxSelect>>", lambda e: self.show_zombies())
        self.msg_var = StringVar()
        self.show_zombie_msg = ttk.Label(self, textvariable=self.msg_var)
        self.make_zombie_message()

    def make_zombie_message(self):
        self.show_zombie_name_text = ttk.Label(self, text='当前僵尸的种类：')
        self.show_zombie_name = ttk.Entry(self, width=10)
        self.show_zombie_row_text = ttk.Label(self, text='当前僵尸的出现行数：')
        self.show_zombie_row = ttk.Entry(self, width=10)
        self.show_zombie_column_text = ttk.Label(self, text='当前僵尸的出现列数：')
        self.show_zombie_column = ttk.Entry(self, width=10)
        self.show_zombie_appear_time_text = ttk.Label(self, text='当前僵尸的出现时间：')
        self.show_zombie_appear_time = ttk.Entry(self, width=10)
        self.show_zombie_config_text = ttk.Label(self, text='当前僵尸的参数配置：')
        self.show_zombie_config = ttk.Entry(self, width=30)
        self.show_zombie_save = ttk.Button(self,
                                           text='保存',
                                           command=self.save_current_zombies)

    def save_current_zombies(self):
        current_name = self.show_zombie_name.get()
        if not current_name:
            return
        current_row = self.show_zombie_row.get()
        current_column = self.show_zombie_column.get()
        current_appear_time = self.show_zombie_appear_time.get()
        if not current_row:
            current_row = 0
        if not current_appear_time:
            current_appear_time = 0
        current_config = self.show_zombie_config.get()
        current_ind = self.inds
        self.current_obj.zombie_ls[current_ind] = [
            current_name, current_row, current_column, current_appear_time,
            current_config
        ]
        self.num_of_zombies_save.place(x=600, y=500)
        self.after(1000, self.num_of_zombies_save.place_forget)

    def show_zombie_messages(self, ind):

        zombie_msg = self.current_obj.zombie_ls[ind]
        self.show_zombie_name.delete(0, END)
        self.show_zombie_row.delete(0, END)
        self.show_zombie_column.delete(0, END)
        self.show_zombie_appear_time.delete(0, END)
        self.show_zombie_config.delete(0, END)
        if zombie_msg:
            self.show_zombie_name.insert(END, zombie_msg[0])
            self.show_zombie_row.insert(END, zombie_msg[1])
            self.show_zombie_column.insert(END, zombie_msg[2])
            self.show_zombie_appear_time.insert(END, zombie_msg[3])
            self.show_zombie_config.insert(END, zombie_msg[4])

        self.show_zombie_msg.place(x=400, y=410)
        self.show_zombie_name_text.place(x=200, y=440)
        self.show_zombie_name.place(x=350, y=440)
        self.show_zombie_row_text.place(x=200, y=470)
        self.show_zombie_row.place(x=350, y=470)
        self.show_zombie_column_text.place(x=200, y=500)
        self.show_zombie_column.place(x=350, y=500)
        self.show_zombie_appear_time_text.place(x=200, y=530)
        self.show_zombie_appear_time.place(x=350, y=530)
        self.show_zombie_config_text.place(x=200, y=560)
        self.show_zombie_config.place(x=350, y=560)
        self.show_zombie_save.place(x=500, y=500)

    def refresh_current_zombie_msg(self):
        self.refresh(self.show_zombie_msg)
        self.refresh(self.show_zombie_name_text)
        self.refresh(self.show_zombie_name)
        self.refresh(self.show_zombie_row_text)
        self.refresh(self.show_zombie_row)
        self.refresh(self.show_zombie_column_text)
        self.refresh(self.show_zombie_column)
        self.refresh(self.show_zombie_appear_time_text)
        self.refresh(self.show_zombie_appear_time)
        self.refresh(self.show_zombie_config_text)
        self.refresh(self.show_zombie_config)
        self.refresh(self.show_zombie_save)

    def refresh(self, obj):
        if obj.place_info():
            obj.place_forget()

    def refresh_random_mode(self):
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
        self.refresh(self.prob_text)
        self.refresh(self.prob)

    def refresh_each_mode(self):
        self.refresh(self.each_bar)
        self.refresh(self.each_list)
        self.refresh(self.show_zombie_msg)
        self.refresh_current_zombie_msg()

    def refresh_modify(self):
        self.refresh_random_mode()
        self.refresh_each_mode()

    def random_mode_place(self):
        self.random_choose_types_text.place(x=0, y=400)
        self.random_choose_types.place(x=0, y=420)
        self.random_choose_types_confirm.place(x=400, y=420)
        self.random_choose_rows_text.place(x=0, y=450)
        self.random_choose_rows.place(x=0, y=470)
        self.appear_times_text.place(x=0, y=490)
        self.appear_times.place(x=0, y=510)
        self.config_text.place(x=0, y=530)
        self.config_options.place(x=0, y=550)
        self.prob_text.place(x=0, y=570)
        self.prob.place(x=0, y=590)

    def modify(self):
        self.refresh_modify()
        self.current_part.set(self.choose_stages_list.get(ANCHOR))
        self.current_ind = self.choose_stages_list.index(ANCHOR)
        self.num_of_zombies_text.place(x=0, y=340)
        self.num_of_zombies.place(x=150, y=340)
        self.num_of_zombies_confirm.place(x=300, y=340)
        self.ask_choose_mode_text.place(x=0, y=370)
        self.ask_choose_mode_random.place(x=270, y=370)
        self.ask_choose_mode_each.place(x=330, y=370)
        self.ask_choose_mode_confirm.place(x=450, y=370)
        self.current_obj = self.normals[
            self.current_ind //
            2] if self.current_ind % 2 == 0 else self.waves[self.current_ind //
                                                            2]
        if not self.current_obj.types:
            self.ask_choose_which.set(0)
        else:
            self.ask_choose_which.set(self.current_obj.types)
        saved_num = self.current_obj.num
        self.num_of_zombies.delete(0, END)
        if saved_num:
            self.num_of_zombies.insert(END, saved_num)

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
            self.refresh_each_mode()
            self.current_obj.types = 1
            if self.current_obj.num:
                self.random_choose_types.delete(0, END)
                if self.current_obj.names:
                    self.random_choose_types.insert(END,
                                                    self.current_obj.names)
                self.random_choose_rows.delete(0, END)
                if self.current_obj.row:
                    self.random_choose_rows.insert(END, self.current_obj.row)
                self.appear_times.delete(0, END)
                if self.current_obj.appear_time:
                    self.appear_times.insert(END, self.current_obj.appear_time)
                self.config_options.delete(0, END)
                if self.current_obj.config:
                    self.config_options.insert(END, self.current_obj.config)
                if self.current_obj.probs:
                    self.prob.insert(END, self.current_obj.probs)
                self.random_mode_place()
            else:
                current_msg = ttk.Label(self, text='您还没有设置僵尸数量')
                current_msg.place(x=450, y=300)
                self.after(1000, current_msg.place_forget)
        elif self.choose_mode == 2:
            self.refresh_random_mode()
            self.current_obj.types = 2
            if self.current_obj.num:
                if (not self.current_obj.zombie_ls) or (len(
                        self.current_obj.zombie_ls) != self.current_obj.num):
                    self.current_obj.zombie_ls = [
                        [] for k in range(self.current_obj.num)
                    ]
                self.each_bar.place(x=170, y=500, height=160, anchor=CENTER)
                self.each_list.delete(0, END)
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
        config_options = self.config_options.get()
        probs = self.prob.get()
        self.current_obj.names = current_ls
        self.current_obj.row = appear_rows
        self.current_obj.column = 'map_size[1]-1'
        self.current_obj.appear_time = appear_times
        self.current_obj.config = config_options
        self.current_obj.probs = probs
        self.num_of_zombies_save.place(x=500, y=420)
        self.after(1000, self.num_of_zombies_save.place_forget)

    def show_zombies(self):
        self.inds = self.each_list.index(ANCHOR)
        self.msg_var.set(self.each_list.get(ANCHOR))
        self.show_zombie_messages(self.inds)

    def convert_stages(self, output_text, stage_num, obj, ls, prefix):
        for i in range(stage_num):
            current = obj[i]
            if current.types == 1:
                probs_text = current.probs
                names_text = random_from(current.names, probs_text)
                rows_text = get_rows(current.row)
                column_text = current.column
                appear_time_text = get_appear_times(current.appear_time)
                config_text = current.config

                if config_text:
                    config_text = f'.configure({config_text})'
                if names_text and rows_text != None and column_text != None and appear_time_text != None:
                    output_text += f"{prefix}{i+1} = [get_zombies({names_text}, {rows_text}, {column_text}, {appear_time_text})"
                    if config_text:
                        output_text += config_text
                    output_text += f' for i in range({current.num})]\n'
                    ls.append(f'{prefix}{i+1}')
            elif current.types == 2:
                msg = ', '.join(
                    [zombie_get(*each) for each in current.zombie_ls if each])
                output_text += f'{prefix}{i+1} = [{msg}]\n'
                ls.append(f'{prefix}{i+1}')
        return output_text

    def convert(self):
        output_text = ''
        stage_name = self.stage_name.get()
        if not stage_name:
            current_msg = ttk.Label(self, text='请输入关卡名')
            current_msg.place(x=570, y=90)
            self.after(1000, current_msg.destroy)
            return
        start_time = self.start_time.get()
        if not start_time and start_time != 0:
            current_msg = ttk.Label(self, text='请输入僵尸的出现时间')
            current_msg.place(x=570, y=90)
            self.after(1000, current_msg.destroy)
            return
        if not self.normals or not self.waves:
            current_msg = ttk.Label(self, text='请先输入旗帜数并产生关卡列表')
            current_msg.place(x=500, y=90)
            self.after(1000, current_msg.destroy)
            return
        information = self.stage_info.get('1.0', END)
        if information.replace('\n', ''):
            output_text += f"'''\n{information}'''\n"
        normals = self.normals
        waves = self.waves
        whole_types = get_whole_types(self)
        output_text += f'zombies_names = {whole_types}\n'
        output_text += '''with open('common.py', encoding='utf-8') as f:
    exec(f.read(), globals())
'''
        output_text += f'start_time = {start_time}\n'
        if self.new_map_size:
            output_text += f'map_size = {self.new_map_size}\n'
            output_text += 'lawnmower_rows = [i for i in range(map_size[0])]\n'
        if self.new_map_show:
            output_text += f'map_content = {self.new_map_show}\n'
        stage_num = self.stage_num
        available_normals = []
        available_waves = []
        output_text = self.convert_stages(output_text, stage_num + 1, normals,
                                          available_normals, 'part')
        output_text = self.convert_stages(output_text, stage_num, waves,
                                          available_waves, 'big_wave')

        output_text += f'current_stage = Stage({stage_num})\n'
        if available_normals:
            output_text += f"current_stage.set_normal_all({','.join(available_normals)})\n"
        if available_waves:
            output_text += f"current_stage.set_waves_all({','.join(available_waves)})"
        with open(f'{stage_name}.py', 'w', encoding='utf-8') as f:
            f.write(output_text)
        success = ttk.Label(self, text='成功生成脚本文件,请到stages文件夹里查看')
        success.place(x=0, y=50)
        self.after(1000, success.place_forget)


def random_from(ls_text, probs):
    if ls_text:
        if probs:
            return f'random.choices([{ls_text}], weights=[{probs}], k=1)[0]'
        return f'random.choice([{ls_text}])'


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
    if appear_time:
        if ',' in appear_time:
            return f'random.randint({appear_time})'
        else:
            return appear_time
    else:
        return '0'


root = Root()

root.mainloop()
