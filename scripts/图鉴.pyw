class Root2(Toplevel):

    def __init__(self):
        super(Root2, self).__init__()
        self.protocol('WM_DELETE_WINDOW', self.close_wiki_window)
        self.minsize(*screen_size)
        self.title('图鉴')
        self.plants_frame = ttk.LabelFrame(self)
        self.plants_frame.place(x=0, y=0)
        max_num = num_each_row * max_rows
        self.max_num = max_num
        self.ls = plants_ls
        N = len(self.ls)
        self.num_of_pages = N // max_num
        self.pages = [[k * max_num, (k + 1) * max_num]
                      for k in range(self.num_of_pages)]
        if self.pages:
            self.pages += [[self.pages[-1][1], N]]
        else:
            max_num = N
        self.current_page = 0
        for i in range(N):
            current = plants_ls[i]
            current_img = Image.open(current.img)
            ratio = current_img.height / height
            current_img = current_img.resize(
                (int(current_img.width / ratio), height),
                Image.Resampling.LANCZOS)
            current.img = ImageTk.PhotoImage(current_img)
            current.button = ttk.Button(self.plants_frame,
                                        image=current.img,
                                        command=lambda i=i: self.show_info(i))
        for j in range(len(zombies_ls)):
            current = zombies_ls[j]
            current_img = Image.open(current.img)
            ratio = current_img.height / height
            current_img = current_img.resize(
                (int(current_img.width / ratio), height),
                Image.Resampling.LANCZOS)
            current.img = ImageTk.PhotoImage(current_img)
            current.button = ttk.Button(self.plants_frame,
                                        image=current.img,
                                        command=lambda j=j: self.show_info(j))
        for i in range(max_num):
            current = self.ls[i]
            current.button.grid(row=i // num_each_row, column=i % num_each_row)
        self.update()
        plants_sizes = self.plants_frame.winfo_width(
        ), self.plants_frame.winfo_height()
        self.info_frame = ttk.LabelFrame(self)
        self.info_frame.place(x=plants_sizes[0] + 50, y=0)
        self.info_text = StringVar()
        self.info_label = ttk.Label(self.info_frame,
                                    textvariable=self.info_text,
                                    image='',
                                    compound=TOP)
        self.info_label.grid(row=0, column=0)
        self.page_frame = ttk.LabelFrame(self)
        self.page_frame.place(x=0, y=plants_sizes[1] + 20)
        self.pre_page = ttk.Button(self.page_frame,
                                   text='上一页',
                                   command=lambda: self.switch_page(-1))
        self.pre_page.grid(row=0, column=0)
        self.next_page = ttk.Button(self.page_frame,
                                    text='下一页',
                                    command=lambda: self.switch_page(1))
        self.next_page.grid(row=0, column=1)
        self.mode = 0
        self.change_mode_plants = ttk.Button(
            self, text='植物', command=lambda: self.switch_mode(0))
        self.change_mode_zombies = ttk.Button(
            self, text='僵尸', command=lambda: self.switch_mode(1))
        self.change_mode_plants.place(x=0, y=plants_sizes[1] + 100)
        self.change_mode_zombies.place(x=100, y=plants_sizes[1] + 100)

    def switch_mode(self, mode):
        if mode != self.mode:
            random.choice(paper_sound).play()
            self.info_text.set('')
            self.info_label.configure(image='')
            if self.pages:
                m, n = self.pages[self.current_page]
            else:
                m, n = 0, len(self.ls)
            for each in range(m, n):
                self.ls[each].button.grid_forget()
            self.ls = zombies_ls if mode == 1 else plants_ls
            self.mode = mode
            N = len(self.ls)
            max_num = self.max_num
            self.num_of_pages = N // max_num
            self.pages = [[k * max_num, (k + 1) * max_num]
                          for k in range(self.num_of_pages)]
            if self.pages:
                self.pages += [[self.pages[-1][1], N]]
            else:
                max_num = N
            self.current_page = 0
            for i in range(max_num):
                current = self.ls[i]
                current.button.grid(row=i // num_each_row,
                                    column=i % num_each_row)
            self.update()
            plants_sizes = self.plants_frame.winfo_width(
            ), self.plants_frame.winfo_height()
            self.info_frame.place(x=plants_sizes[0] + 50, y=0)
            self.info_label.grid(row=0, column=0)
            self.page_frame.place(x=0, y=plants_sizes[1] + 20)
            self.pre_page.grid(row=0, column=0)
            self.next_page.grid(row=0, column=1)
            self.change_mode_plants.place(x=0, y=plants_sizes[1] + 100)
            self.change_mode_zombies.place(x=100, y=plants_sizes[1] + 100)

    def show_info(self, i):
        random.choice(paper_sound).play()
        choose_obj = self.ls[i]
        self.info_label.configure(image=choose_obj.img)
        if self.mode == 0:
            current_info = [
                choose_obj.name, f'所需阳光：{choose_obj.price}',
                f'生命值：{choose_obj.hp}', f'冷却时间：{choose_obj.cooling_time}',
                f'攻击力：{choose_obj.bullet_attack if choose_obj.bullet_attack else 0}',
                choose_obj.information if choose_obj.information else ''
            ]
        elif self.mode == 1:
            current_info = [
                choose_obj.name, f'生命值：{choose_obj.hp}',
                f'移动速度：每{choose_obj.move_speed}秒一格',
                f'攻击力：{choose_obj.attack}',
                choose_obj.information if choose_obj.information else ''
            ]
        self.info_text.set('\n'.join(current_info))

    def switch_page(self, num):
        page_num = self.current_page + num
        if 0 <= page_num <= self.num_of_pages:
            random.choice(paper_sound).play()
            m, n = self.pages[self.current_page]
            for each in range(m, n):
                self.ls[each].button.grid_forget()
            j, k = self.pages[page_num]
            for i in range(j, k):
                current = self.ls[i]
                current.button.grid(row=(i - j) // num_each_row,
                                    column=(i - j) % num_each_row)
            self.current_page = page_num

    def close_wiki_window(self):
        root.open_wiki_window = False
        self.destroy()


if __name__ == '__main__':
    json_config_path = os.path.join(abs_path, "scripts/game_config.json")
    with open(json_config_path, encoding='utf-8') as f:
        current_config = json.load(f)
    height = current_config['wiki']['height']
    num_each_row = current_config['wiki']['num_each_row']
    screen_size = current_config['wiki']['screen_size']
    max_rows = current_config['wiki']['max_rows']
    sound_volume = current_config['wiki']['sound_volume']
    pygame.mixer.init()
    paper_sound = [
        pygame.mixer.Sound('resources/sounds/paper.ogg'),
        pygame.mixer.Sound('resources/sounds/seedlift.ogg')
    ]
    for each in paper_sound:
        each.set_volume(sound_volume)
    os.chdir('scripts/plant_scripts')
    sys.path.append(os.getcwd())
    filename = os.listdir()
    remove_ls = ['__pycache__', '__init__.py', 'plant.py', 'bullets.py']
    for each in remove_ls:
        if each in filename:
            filename.remove(each)
    plants_name = [x[:-3] for x in filename]
    for k in filename:
        with open(k, encoding='utf-8') as f:
            exec(f.read(), globals())
    plants_ls = [eval(i) for i in plants_name]
    os.chdir('../zombie_scripts')
    sys.path.append(os.getcwd())
    filename = os.listdir()
    remove_ls = ['__pycache__', '__init__.py', 'regular.py', 'zombies.py']
    for each in remove_ls:
        if each in filename:
            filename.remove(each)
    zombies_name = [x[:-3] for x in filename]
    for k in filename:
        with open(k, encoding='utf-8') as f:
            exec(f.read(), globals())
    zombies_ls = [eval(i) for i in zombies_name]
    os.chdir('../../resources')
    root.wiki_window = Root2()
