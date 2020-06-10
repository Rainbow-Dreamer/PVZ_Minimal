os.chdir('传送带测试')
with open('config.py', encoding='utf-8') as f:
    exec(f.read())
try:
    with open('../memory.txt') as f:
        last_place = f.read()
except:
    last_place = '.'


def go_back():
    pygame.mixer.quit()
    root.destroy()    
    os.chdir('..')
    os.startfile('pvz极简版.exe')

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.wm_iconbitmap(icon_name)
        self.title('传送带测试')
        self.minsize(*screen_size)
        self.last_place = last_place
        self.paused_time = 0
        self.sound_volume = 1
        self.music_flag = 1
        self.bullets_ls = []
        self.back_button = ttk.Button(self, text='返回', command=go_back)
        self.back_button.place(x=screen_size[0]-100, y=0)
        self.make_label = ttk.Label
        self.make_button = ttk.Button
        self.NULL, self.PLACE, self.REMOVE, self.PAUSE = 0, 1, 2, 3
        self.lawn_photo = Image.open(lawn_img)

        lawn_size = 250 // map_size[0]
        self.lawn_photo = self.lawn_photo.resize((lawn_size, lawn_size),
                                                 Image.ANTIALIAS)
        self.background_img = self.lawn_photo.copy()
        self.lawn_photo = ImageTk.PhotoImage(self.lawn_photo)
        self.lawn_width, self.lawn_height = self.lawn_photo.width(
        ), self.lawn_photo.height()
        
        self.target_plant = None
        
        self.current_belt = current_belt
        self.current_belt.imgs = []
        for each in self.current_belt.plants_base:
            current_img = Image.open(each.img)
            resize_num = self.current_belt.resize_num
            current_img = current_img.resize(
                (int(self.lawn_width/resize_num),
                 int(self.lawn_height/resize_num)), Image.ANTIALIAS)
            self.current_belt.imgs.append(ImageTk.PhotoImage(current_img))   
        for j in range(len(self.current_belt.plants_base)):
            self.current_belt.plants_base[j].number = j
        self.belt_img = Image.open(self.current_belt.img)
        self.belt_img = self.belt_img.resize((int(self.lawn_width/resize_num),
                 int(self.lawn_height/resize_num)), Image.ANTIALIAS)
        self.belt_width, self.belt_height = self.belt_img.width, self.belt_img.height
        self.belt_img = ImageTk.PhotoImage(self.belt_img)
        self.current_belt.belts = [ttk.Button(self, image=self.belt_img, command=lambda i=i:self.belt_plant(i)) for i in range(self.current_belt.show_length)]
        belt_x, belt_y = self.current_belt.belt_x, self.current_belt.belt_y
        offset = self.current_belt.offset
        for k in range(self.current_belt.show_length):
            current = self.current_belt.belts[k]
            current.plants = None
            current.place(x=belt_x + k*(self.belt_width+offset), y=belt_y)
        
        self.configs = ttk.Button(self,
                                  text='设置',
                                  command=self.make_config_window)
        
        self.configs.place(x=screen_size[0] - 100, y=screen_size[1] - 60)
        
            
        self.belt_counter = time.time()        
        self.action_text = StringVar()
        self.action_text_show = ttk.Label(self, textvariable=self.action_text)
        self.action_text_place_y = map_size[0] * (self.lawn_height + 10) + 150
        self.action_text_show.place(x=action_text_place_x,
                                    y=self.action_text_place_y,
                                    anchor='center')

        bg_music = pygame.mixer.music.load(background_music)
        pygame.mixer.music.set_volume(background_volume)
        pygame.mixer.music.play(loops=-1)
        game_start_time = time.time()
        self.game_start_time = game_start_time
        self.mode = NULL
        self.blocks = []
        self.moving_bullets = []
        self.sunshine_time = game_start_time

        self.choose = ttk.LabelFrame(self)
        self.maps = ttk.LabelFrame(self)
        self.init_shovel()
        self.choose.grid(row=0, column=0, sticky='W')
        self.lawnmowers = [0 for j in range(map_size[0])]
        self.lawnmower_img = Image.open(lawnmower_img)
        self.lawnmower_img = self.lawnmower_img.resize(
            (self.lawn_width, self.lawn_height), Image.ANTIALIAS)
        self.lawnmower_img = ImageTk.PhotoImage(self.lawnmower_img)
        self.no_lawnmower_img = Image.open(no_lawnmower_img)
        self.no_lawnmower_img = self.no_lawnmower_img.resize(
            (self.lawn_width, self.lawn_height), Image.ANTIALIAS)
        self.no_lawnmower_img = ImageTk.PhotoImage(self.no_lawnmower_img)
        if lawnmower_rows:
            self.mower_part = ttk.LabelFrame(self)
            self.mower_part.place(x=0, y=100)
            for k in lawnmower_rows:
                current_mower = lawnmower(k, 0, lawnmower_mode,
                                          lawnmower_speed, lawnmower_atack)
                current_mower.show = ttk.Button(
                    self.mower_part,
                    image=self.lawnmower_img,
                    command=lambda: self.action_text.set('我是一辆小推车'))
                current_mower.show.grid(row=k, column=0, sticky='W')
                self.lawnmowers[k] = current_mower

        self.init_map(*map_size)
        self.maps.place(x=65, y=100)
        
        self.choosed_plant = None
        self.sunshine_ls = []
        self.map_rows, self.map_columns = map_size

        self.bind("<Button-3>", lambda e: self.reset())
        self.zombie_explode_img = Image.open(zombie_explode)
        self.zombie_explode_img = self.zombie_explode_img.resize(
            (self.lawn_width, self.lawn_height), Image.ANTIALIAS)
        self.zombie_explode_img = ImageTk.PhotoImage(self.zombie_explode_img)
        self.normal_zombies_num = 0
        self.big_waves_zombies_num = 0
        self.normal_or_wave = 0
        self.whole_zombies = current_stage.get(0)
        self.killed_zombies = 0
        self.zombie_time = game_start_time + start_time
        self.killed_zombies_text = StringVar()
        self.killed_zombies_text.set(f'杀死僵尸数: {self.killed_zombies}')
        self.killed_zombies_show = ttk.Label(
            textvariable=self.killed_zombies_text)
        self.killed_zombies_show.place(x=action_text_place_x + 200,
                                       y=self.action_text_place_y,
                                       anchor='center')
        self.flag_img = Image.open(flag_img)
        self.flag_img = self.flag_img.resize(
            (self.lawn_width // 2, self.lawn_height // 2), Image.ANTIALIAS)
        self.flag_img = ImageTk.PhotoImage(self.flag_img)
        self.damaged_flag_img = Image.open(damaged_flag_img)
        self.damaged_flag_img = self.damaged_flag_img.resize(
            (self.lawn_width // 2, self.lawn_height // 2), Image.ANTIALIAS)
        self.damaged_flag_img = ImageTk.PhotoImage(self.damaged_flag_img)
        self.head_img = Image.open(zombie_head_img)
        self.head_img = self.head_img.resize(
            (self.lawn_width // 2, self.lawn_height // 2), Image.ANTIALIAS)
        self.head_img = ImageTk.PhotoImage(self.head_img)
        self.zombie_bar = ttk.LabelFrame(self)
        self.zombie_bar_normal_labels = []
        self.zombie_bar_wave_labels = []
        unit_width = int(50 / (current_stage.num_of_waves +
                               (current_stage.num_of_waves + 1) * 5))
        long_width = unit_width * 5
        short_width = unit_width
        counter = 6 * current_stage.num_of_waves + 4
        for k in range(current_stage.num_of_waves * 2 + 1):
            if k % 2 == 0:
                normal_labels = []
                for j in range(5):
                    current_bar = ttk.Label(self.zombie_bar, width=short_width)
                    current_bar.grid(row=0, column=counter - j)
                    normal_labels.append(current_bar)
                self.zombie_bar_normal_labels.append(normal_labels)
                counter -= 5
            else:
                current_bar = ttk.Label(self.zombie_bar,
                                        image=self.flag_img,
                                        width=long_width)
                current_bar.grid(row=0, column=counter)
                self.zombie_bar_wave_labels.append(current_bar)
                counter -= 1
        self.zombie_bar.place(x=action_text_place_x,
                              y=self.action_text_place_y + 50,
                              anchor='center')
        self.current_ind = -1
        self.current_zombies_num = len(self.whole_zombies)
        self.current_killed_zombies = 0
        self.current_time = time.time()
        self.check_plants()
        self.after(int(start_time * 1000), zombies_coming_sound.play)
        self.after(int(start_time * 1000), self.check_zombies)
    
    
    def reset(self):
        self.action_text.set('')
        self.target_plant = None
        self.mode = NULL
    
    
    def change_mode(self, num, plant=None):
        if self.mode != PAUSE:
            self.mode = num
            if num == PLACE:
                current_plant = choosed_plants[plant]
                if current_plant.enable == 0:
                    sunshine_not_enough.play()
                    self.action_text.set(f'{current_plant.name}正在冷却中')
                    self.mode = NULL
                elif self.sunshine < current_plant.price:
                    sunshine_not_enough.play()
                    self.action_text.set('阳光不够哦')
                    self.mode = NULL
                else:
                    choose_plants_sound.play()
                    self.action_text.set(f'你选择了{current_plant.name}')
                    self.choosed_plant = plant

            elif num == REMOVE:
                pick_shovel_sound.play()
                self.action_text.set('请选择一个草地上的植物铲除')
            elif     num == NULL:
                self.action_text.set('')
    
    
    def init_shovel(self):
        shovel_photo = ImageTk.PhotoImage(
            Image.open(shovel_img).resize((self.lawn_width, self.lawn_height),
                                          Image.ANTIALIAS))
        self.shovel_button = ttk.Button(
            self,
            image=shovel_photo,
            command=lambda: self.change_mode(REMOVE))
        self.shovel_button.image = shovel_photo
        self.shovel_button.place(x=screen_size[0]-170, y=0)   
    
    def belt_plant(self, i):
        current = self.current_belt.belts[i]
        if current.plants:
            self.mode = PLACE
            self.target_plant = current.plants
            
    
    
    def make_config_window(self):
        config_window = Toplevel(self)
        config_window.title('设置')
        config_window.minsize(500, 300)
        config_window.bg_volume_text = ttk.Label(config_window, text='背景音乐音量')
        config_window.bg_volume = Scale(
            config_window,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            resolution=5,
            length=200,
            command=lambda e: self.change_bg_volume(config_window))
        config_window.bg_volume.set(int(pygame.mixer.music.get_volume() * 100))
        config_window.bg_volume_text.place(x=0, y=20)
        config_window.bg_volume.place(x=100, y=0)
        config_window.bg_text = ttk.Label(config_window, text='背景音乐')
        config_window.bg = Text(config_window, width=55, height=5)
        config_window.bg_button = ttk.Button(
            config_window,
            text='更改',
            command=lambda: self.change_bg(config_window))
        if self.music_flag == 1:
            config_window.bg.insert(END, background_music)
        elif self.music_flag == 0:
            config_window.bg.insert(END, choose_plants_music)
        config_window.bg_text.place(x=0, y=60)
        config_window.bg.place(x=0, y=80)
        config_window.bg_button.place(x=400, y=80)
        config_window.sound_volume_text = ttk.Label(config_window, text='音效音量')
        config_window.sound_volume = Scale(
            config_window,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            resolution=5,
            length=200,
            command=lambda e: self.change_sound_volume(config_window))
        config_window.sound_volume.set(int(self.sound_volume * 100))
        config_window.sound_volume_text.place(x=0, y=180)
        config_window.sound_volume.place(x=100, y=160)
        if self.music_flag == 1:
            config_window.go_back_button = ttk.Button(config_window, text='返回主界面', command=lambda: self.go_back(config_window))
            config_window.go_back_button.place(x=400, y=20)

    def change_bg(self, config_window):
        filename = filedialog.askopenfilename(initialdir=self.last_place,
                                              title="选择你想播放的背景音乐",
                                              filetype=(("音乐文件",
                                                         "*.mp3;*.ogg;*.wav"),
                                                        ("所有文件", "*.*")))
        if filename:
            self.last_place = os.path.dirname(filename)
            with open('../memory.txt', 'w') as f:
                f.write(self.last_place)

            if self.music_flag == 1:
                global background_music
                background_music = filename
                pygame.mixer.music.stop()
                pygame.mixer.music.load(background_music)
                pygame.mixer.music.play(loops=-1)
                config_window.bg.delete('1.0', END)
                config_window.bg.insert(END, background_music)
            elif self.music_flag == 0:
                global choose_plants_music
                choose_plants_music = filename
                pygame.mixer.music.stop()
                pygame.mixer.music.load(choose_plants_music)
                pygame.mixer.music.play(loops=-1)
                config_window.bg.delete('1.0', END)
                config_window.bg.insert(END, choose_plants_music)

    def change_bg_volume(self, config_window):
        new_volume = config_window.bg_volume.get()
        if new_volume != int(pygame.mixer.music.get_volume() * 100):
            pygame.mixer.music.set_volume(new_volume / 100)
            if self.music_flag == 1:
                global background_volume
                background_volume = new_volume / 100
            elif self.music_flag == 0:
                global choose_seed_volume
                choose_seed_volume = new_volume / 100                

    def change_sound_volume(self, config_window):
        new_volume = config_window.sound_volume.get()
        if new_volume != int(self.sound_volume * 100):
            new_set_volume = new_volume / 100
            for each in whole_sounds:
                if type(each) == list:
                    for i in each:
                        i.set_volume(new_set_volume)
                else:
                        each.set_volume(new_set_volume)
            self.sound_volume = new_set_volume
    
    
    def block_action(self, j, k=None, mode=0):
        if self.mode != PAUSE:
            if mode == 1:
                dim = j.rows, j.columns
                j, k = dim
            if self.mode == PLACE:
                current = self.blocks[j][k]
                choose_plant = self.target_plant
                if current.plants is None or (not choose_plant.plant_normal):
                    current_time = self.current_time
                    current.plants = get_plant(choose_plant, j, k)
                    if current.plants.bullet_sound:
                        for each in current.plants.bullet_sound:
                            if type(each) == list:
                                for each_sound in each:
                                    each_sound.set_volume(self.sound_volume)
                            else:
                                each.set_volume(self.sound_volume)                    
                    self.make_img(current.plants)
                    if current.plants.use_bullet_img_first:
                        current.configure(image=current.plants.bullet_img)
                    else:
                        current.configure(image=current.plants.img)

                    current.plants.time = current_time
                    current_plant_name = current.plants.name
                    set_plants_sound.play()
                    self.action_text.set(
                        f'你成功放置了{current_plant_name}在第{j+1}行，第{k+1}列')
                    current.plants.counter = current_time
                    current.plants.enable = 0
                    self.choosed_plant = None
                    current_unit = self.current_belt.belts[choose_plant.belt_col]
                    current_unit.configure(image=self.belt_img)
                    current_unit.plants = None
                    self.target_plant = None
                    self.mode = NULL
                else:
                    self.action_text.set('这里已经有植物了，要种的话请先铲掉')

            elif self.mode == REMOVE:
                block = self.blocks[j][k]
                if block.plants is not None:
                    block.configure(image=self.lawn_photo)
                    unset_plants_sound.play()
                    self.action_text.set(
                        f'你铲除了第{j+1}行，第{k+1}列的植物{block.plants.name}')
                    if block.plants.away_func:
                        block.plants.away_func(block.plants, self)
                    block.plants.status = 0
                    block.plants = None
                else:
                    self.action_text.set('这里并没有植物，请问您要铲什么？')
                self.mode = NULL
            else:
                if mode == 1 and show_zombies:
                    current_block_zombies = [
                        x.name for x in self.whole_zombies
                        if x.status == 1 and x.rows == j and x.columns == k
                    ]
                    current_block_zombies_types = set(current_block_zombies)
                    zombies_message = f'第{j+1}行第{k+1}列的格子上有' + ', '.join([
                        f'{current_block_zombies.count(t)}个{t}'
                        for t in current_block_zombies_types
                    ])
                    plants_on_block = self.blocks[j][k].plants
                    if plants_on_block:
                        zombies_message += '\n'
                        zombies_message += f'这上面有个{plants_on_block.name}, 当前生命值{plants_on_block.hp}'
                    self.action_text.set(zombies_message)
                else:
                    plants_on_block = self.blocks[j][k].plants
                    if plants_on_block is None:
                        self.action_text.set('这是一块空荡荡的草坪')
                    else:
                        self.action_text.set(
                            f'这上面有个{plants_on_block.name}, 当前生命值{plants_on_block.hp}'
                        )

    
    
    
    def make_img(self, each, resize_num=1):
        current_img = Image.open(each.img)
        if each.img_transparent:
            ratio = min(self.lawn_height / current_img.height, self.lawn_width / current_img.width)
            current_img = current_img.resize(
                (int(current_img.width * ratio / resize_num),
                 int(current_img.height * ratio / resize_num)),
                Image.ANTIALIAS)
            center_width = int(self.lawn_width / 2 - current_img.width / 2)
            temp = self.background_img.copy()
            temp.paste(current_img, (center_width, 0), current_img)
            each.img = ImageTk.PhotoImage(temp)

        else:
            current_img = current_img.resize(
                (int(self.lawn_width / resize_num),
                 int(self.lawn_height / resize_num)), Image.ANTIALIAS)
            each.img = ImageTk.PhotoImage(current_img)
        try:
            if each.bullet_img:
                if not each.is_bullet:
                    current_img = Image.open(each.bullet_img)
                    current_img = current_img.resize(
                        (self.lawn_width, self.lawn_height), Image.ANTIALIAS)
                    each.bullet_img = ImageTk.PhotoImage(current_img)
                else:
                    each.bullet_img = Image.open(each.bullet_img)
                    ratio = min((self.lawn_height/3) / each.bullet_img.height, (self.lawn_width/3) / each.bullet_img.width)
                    each.bullet_img = ImageTk.PhotoImage(
                        each.bullet_img.resize(
                            (int(each.bullet_img.width*ratio), int(each.bullet_img.height*ratio)),
                            Image.ANTIALIAS))
            if each.other_img:
                for j in range(len(each.other_img)):
                    current_other_img_ls = each.other_img[j]
                    current_len = len(current_other_img_ls)
                    if current_len == 2:
                        img_name, resize_num = current_other_img_ls
                        as_bullet = False
                    elif current_len == 3:
                        img_name, resize_num, as_bullet = current_other_img_ls
                    current_other_img = Image.open(img_name)
                    ratio = min((self.lawn_height/resize_num) / current_other_img.height, (self.lawn_width/resize_num) / current_other_img.width)
                    current_other_img = current_other_img.resize(
                        (int(current_other_img.width*ratio),
                         int(current_other_img.height*ratio)), Image.ANTIALIAS)
                    current_other_img_ls[1] = img_name
                    current_other_img_ls[0] = ImageTk.PhotoImage(
                        current_other_img)
                    if as_bullet:
                        self.bullets_ls.append(img_name)
        except:
            pass    
    
    
    
    
    def pause(self):
        if self.mode != PAUSE:
            self.mode = PAUSE
            self.action_text.set("游戏暂停,按P继续")
            pygame.mixer.music.pause()
            pause_sound.play()
            self.paused_start = time.time()



    def init_map(self, rows, columns):
        lawn_photo = self.lawn_photo
        for j in range(rows):
            block_row = []
            for k in range(columns):
                current_block = ttk.Button(self.maps,
                                           image=lawn_photo,command=lambda j=j, k=k: self.block_action(j, k))
                current_block.plants = None
                current_block.image = lawn_photo
                current_block.grid(row=j, column=k)
                block_row.append(current_block)
            self.blocks.append(block_row)
        self.lawn_photo = lawn_photo


    def flower_get_sunshine(self, sun, obj):
        if self.mode != PAUSE:
            self.sunshine += obj.bullet_attack
            self.sunshine_text.set(self.sunshine)
            get_sunshine_sound.play()
            self.action_text.set(f'成功拿到了{obj.bullet_attack}点阳光')
            sun.destroy()

    def set_zombies(self, current_zombies):
        current_zombies.attack_sound = [
            pygame.mixer.Sound(j) for j in current_zombies.attack_sound
        ]
        for each in current_zombies.attack_sound:
            each.set_volume(self.sound_volume)
        whole_sounds.extend(current_zombies.attack_sound)
        current_zombies.dead_sound = [
            pygame.mixer.Sound(j)
            if type(j) != list else [pygame.mixer.Sound(k) for k in j]
            for j in current_zombies.dead_sound
        ]
        for each in current_zombies.dead_sound:
            if type(each) != list:
                each.set_volume(self.sound_volume)
            else:
                for i in each:
                    i.set_volume(self.sound_volume)
        whole_sounds.extend(current_zombies.dead_sound)
        current_zombies.hit_sound = [
            pygame.mixer.Sound(j) for j in current_zombies.hit_sound
        ]
        for each in current_zombies.hit_sound:
            each.set_volume(self.sound_volume)
        whole_sounds.extend(current_zombies.hit_sound)
        if current_zombies.hit_sound_ls:
            for k in range(len(current_zombies.hit_sound_ls)):
                current = current_zombies.hit_sound_ls[k][1]
                current_zombies.hit_sound_ls[k][1] = pygame.mixer.Sound(
                    current) if type(current) != list else [
                        pygame.mixer.Sound(y) for y in current
                    ]
            for each in current_zombies.hit_sound_ls:
                if type(each[1]) != list:
                    each[1].set_volume(self.sound_volume)
                else:
                    for i in each[1]:
                        i.set_volume(self.sound_volume)
            whole_sounds.extend([i[1] for i in current_zombies.hit_sound_ls])
        if current_zombies.other_sound:
            current_zombies.other_sound = [
                pygame.mixer.Sound(k) for k in current_zombies.other_sound
            ]
            for each in current_zombies.other_sound:
                each.set_volume(self.sound_volume)
            whole_sounds.extend(current_zombies.other_sound)
        self.make_img(current_zombies)
        current_zombies_button = ttk.Button(
            self.maps,
            image=current_zombies.img,
            command=lambda current_zombies=current_zombies: self.block_action(
                current_zombies, mode=1))
        current_zombies_button.image = current_zombies.img
        current_zombies.button = current_zombies_button
        current_zombies.next_to_plants = False
        current_zombies.eating = False
        current_zombies.time = self.current_time

    def lawnmower_move(self, obj):
        if obj.columns == 0:
            lawnmower_sound.play()
        if obj.columns >= self.map_columns:
            obj.destroy()
            return
        attack_size = [obj.columns, obj.columns + 1]
        current_zombies = [
            each for each in self.whole_zombies if each.status == 1
            and each.rows == obj.rows and each.columns in attack_size
        ]

        if current_zombies:
            if obj.mode == 0:
                for each in current_zombies:
                    each.hp = 0
                    each.status = 0
                    self.killed_zombies += 1
                    self.current_killed_zombies += 1
                    self.killed_zombies_text.set(
                        f'杀死僵尸数: {self.killed_zombies}')
                    self.zombie_dead_normal(each)
            elif obj.mode == 1:
                for each in current_zombies:
                    each.hp -= obj.attack
        obj.grid(row=obj.rows, column=obj.columns)
        obj.columns += 1
        self.after(obj.move_speed, lambda: self.lawnmower_move(obj))

    def zombie_dead_normal(self, obj):
        obj.button.destroy()
        obj.dead_sound[0].play()
        self.after(2000, lambda: random.choice(obj.dead_sound[1]).play())


    def check_plants(self):
        self.current_time = time.time()
        if self.current_time - self.belt_counter >= self.current_belt.new_plant_speed:
            self.belt_counter = self.current_time
            belt_col = self.current_belt.show_length - 1
            last_unit = self.current_belt.belts[belt_col]
            if last_unit.plants is None:
                new_plant = deepcopy(self.current_belt.choose())
                new_plant.belt_col = belt_col
                new_plant.belt_counter = self.current_time
                last_unit.configure(image=self.current_belt.imgs[new_plant.number])
                last_unit.plants = new_plant
        for k in range(1, self.current_belt.show_length):
            each_unit = self.current_belt.belts[k]
            if each_unit.plants:
                each = each_unit.plants
                if self.current_time - each.belt_counter >= self.current_belt.move_speed:
                    each.belt_counter = self.current_time
                    after_belt = self.current_belt.belts[k-1]
                    if after_belt.plants is None:                    
                        each_unit.configure(image=self.belt_img)
                        each_unit.plants = None
                        each.belt_col = k-1
                        after_belt.configure(image=self.current_belt.imgs[each.number])
                        after_belt.plants = each
        if self.mode == 'stop':
            return
        if self.mode == PAUSE:
            if keyboard.is_pressed('p'):
                self.mode = NULL
                self.action_text.set('游戏继续')
                pygame.mixer.music.unpause()
                repause_current_time = time.time()
                self.paused_time = repause_current_time - self.paused_start
                self.sunshine_time += self.paused_time
                self.paused_start = None
                for i in range(map_size[0]):
                    for j in range(map_size[1]):
                        block_here = self.blocks[i][j]
                        if block_here.plants != None:
                            block_here.plants.time += self.paused_time
                for each in choosed_plants:
                    each.counter += self.paused_time
                for k in self.whole_zombies:
                    if k.status == 0 and k.hp > 0:
                        k.appear_time += self.paused_time
                    elif k.status == 1:
                        k.time += self.paused_time
                self.zombies_move_call()
                for each_bullet in self.moving_bullets:
                    if each_bullet.func:
                        each_bullet.func(self, each_bullet)
                self.moving_bullets = []
                self.paused_time = 0
        else:
            nrow, ncol = map_size
            for i in range(nrow):
                j = 0
                while j < ncol:
                    current = self.blocks[i][j]
                    if current.plants is not None:
                        if current.plants.hp <= 0:
                            if current.plants.dead_normal:
                                plant_bite_sound.play()
                                self.action_text.set(
                                    f'第{i+1}行，第{j+1}列的植物{current.plants.name}被吃掉了'
                                )
                                current.plants = None
                                current.configure(image=self.lawn_photo)
                                j += 1
                                continue
                        if current.plants.hp_img:
                            plants_hp_tol = current.plants.hp_img[0][0]
                            if (current.plants.change_mode == 0 and
                                    current.plants.hp / current.plants.full_hp
                                    <= plants_hp_tol) or (
                                        current.plants.change_mode == 1
                                        and current.plants.hp <= plants_hp_tol
                                    ) or (current.plants.change_mode == 2
                                          and current.plants.full_hp -
                                          current.plants.hp >= plants_hp_tol):
                                new_hp_img = Image.open(
                                    current.plants.hp_img[0][1])
                                new_hp_img = new_hp_img.resize(
                                    (self.lawn_width, self.lawn_height),
                                    Image.ANTIALIAS)
                                new_hp_img = ImageTk.PhotoImage(new_hp_img)
                                current.configure(image=new_hp_img)
                                current.plants.img = new_hp_img
                                current.plants.hp_img = current.plants.hp_img[
                                    1:]
                        if current.plants.status == 1:
                            if current.plants.func:
                                current.plants.runs(self)
                    j += 1

        self.after(1, self.check_plants) 
     
    
    def check_zombies(self):
        
                

        if self.mode != PAUSE:
            current_time = self.current_time
            if self.normal_or_wave == 0:
                new_ind = int(self.current_killed_zombies /
                              (self.current_zombies_num * 0.2))
                if new_ind == 5:
                    new_ind = 4
                if new_ind != self.current_ind:
                    self.zombie_bar_normal_labels[self.normal_zombies_num][
                        self.current_ind].configure(image='')
                    self.zombie_bar_normal_labels[
                        self.normal_zombies_num][new_ind].configure(
                            image=self.head_img)
                    self.current_ind = new_ind
            if self.current_killed_zombies == self.current_zombies_num:
                self.current_ind = -1
                self.current_killed_zombies = 0
                self.zombie_time = current_time
                if self.normal_or_wave == 0:
                    self.normal_or_wave = 1
                    if self.normal_zombies_num == current_stage.num_of_waves:
                        self.action_text.set('你赢了！')
                        self.mode = PAUSE
                        self.win()
                        return
                    self.normal_zombies_num += 1
                    self.whole_zombies = current_stage.get(
                        self.big_waves_zombies_num, 1)
                    self.current_zombies_num = len(self.whole_zombies)
                    self.after(2000, huge_wave_sound.play)
                    self.after(2000,
                               lambda: self.action_text.set('一大波僵尸要来袭了！'))
                    self.after(5000, zombies_coming_sound.play)
                    self.after(
                        5000, lambda: self.zombie_bar_wave_labels[
                            self.big_waves_zombies_num].configure(
                                image=self.damaged_flag_img))
                    self.after(
                        5000, lambda: self.zombie_bar_normal_labels[
                            self.normal_zombies_num - 1][-1].configure(image=''
                                                                       ))
                    self.after(
                        5000, lambda: self.zombie_bar_normal_labels[
                            self.normal_zombies_num][0].configure(image=self.
                                                                  head_img))
                    self.zombie_time += 5
                    self.after(5000, self.check_zombies)
                    return
                elif self.normal_or_wave == 1:
                    self.normal_or_wave = 0
                    self.big_waves_zombies_num += 1
                    self.whole_zombies = current_stage.get(
                        self.normal_zombies_num)
                    self.current_zombies_num = len(self.whole_zombies)

            passed_time = current_time - self.zombie_time
            for each in self.whole_zombies:
                if each.status == 1:
                    if each.hp <= 0:
                        each.status = 0
                        self.killed_zombies += 1
                        self.current_killed_zombies += 1
                        self.killed_zombies_text.set(
                            f'杀死僵尸数: {self.killed_zombies}')
                        self.zombie_dead_normal(each)
                    else:

                        if each.hp_img:
                            hp_tol = each.hp_img[0][0]
                            if (each.change_mode == 0
                                    and each.hp / each.full_hp <= hp_tol) or (
                                        each.change_mode == 1
                                        and each.hp <= hp_tol) or (
                                            each.change_mode == 2 and
                                            each.full_hp - each.hp >= hp_tol):
                                new_hp_img = Image.open(each.hp_img[0][1])
                                new_hp_img = new_hp_img.resize(
                                    (self.lawn_width, self.lawn_height),
                                    Image.ANTIALIAS)
                                new_hp_img = ImageTk.PhotoImage(new_hp_img)
                                each.button.configure(image=new_hp_img)
                                each.button.image = new_hp_img
                                each.hp_img = each.hp_img[1:]
                        if each.hit_sound_ls:
                            hit_tol = each.hit_sound_ls[0][0]
                            if (each.change_mode == 0
                                    and each.hp / each.full_hp <= hit_tol) or (
                                        each.change_mode == 1
                                        and each.hp <= hit_tol) or (
                                            each.change_mode == 2 and
                                            each.full_hp - each.hp >= hit_tol):
                                each.hit_sound = each.hit_sound_ls[0][1]
                                each.hit_sound_ls = each.hit_sound_ls[1:]
                        if each.eachtime_func:
                            each.runs(self, num=1)
                else:
                    if each.hp > 0 and passed_time >= each.appear_time:
                        self.set_zombies(each)
                        each.alive()
                        if each.start_func:
                            each.runs(self, num=0)
        self.after(1, self.check_zombies)

    def zombies_move_call(self):
        for each in self.whole_zombies:
            if each.status == 1 and each.hp > 0:
                if each.repause_func:
                    each.runs(self, num=2)

    def lose(self):
        self.action_text.set('僵尸进了你的家里！')
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        lose_sound.play()
        self.after(7000, quit)

    def win(self):
        self.after(7000, quit)


root = Root()


def quit():
    pygame.mixer.quit()
    root.destroy()


root.protocol('WM_DELETE_WINDOW', quit)
root.mainloop()
