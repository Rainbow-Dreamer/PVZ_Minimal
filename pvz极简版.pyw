import os, sys, importlib, pygame, time, random, keyboard
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from copy import deepcopy
pygame.mixer.init()
sys.path.append(os.path.dirname(__file__))
current_dir = os.getcwd()
config_path = os.path.join(current_dir, "pvz_config.py")
with open(config_path, encoding='utf-8') as f:
    datas = f.read()
    exec(datas, globals())
whole_plants_img = [x[1] for x in whole_plants]
whole_plants = [[x[0], 0] for x in whole_plants]

try:
    with open('../memory.txt') as f:
        last_place = f.read()
except:
    last_place = '.'


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.wm_iconbitmap(icon_name)
        self.title(title_name)
        self.minsize(*screen_size)
        self.sound_volume = 1
        self.last_place = last_place
        self.music_flag = 0
        self.is_stop = False
        self.wiki = ttk.Button(self, text='图鉴', command=self.open_wiki)
        self.wiki.place(x=screen_size[0] - 100, y=screen_size[1] - 180)

        self.make_stage = ttk.Button(self,
                                     text='制作关卡',
                                     command=self.open_make_stage)
        self.make_stage.place(x=screen_size[0] - 100, y=screen_size[1] - 140)

        self.configs = ttk.Button(self,
                                  text='设置',
                                  command=self.make_config_window)
        self.little_game = ttk.Button(self,
                                      text='小游戏',
                                      command=self.open_little_game)
        self.little_game.place(x=screen_size[0] - 100, y=screen_size[1] - 100)

        self.configs.place(x=screen_size[0] - 100, y=screen_size[1] - 60)
        self.make_label = ttk.Label
        self.make_button = ttk.Button
        self.get_zombies = get_zombies
        self.plant_bite_sound = plant_bite_sound
        self.unset_plants_sound = unset_plants_sound
        self.NULL, self.PLACE, self.REMOVE, self.PAUSE = 0, 1, 2, 3
        self.map_img_dict = map_img_dict
        global lawn_size
        if not lawn_size:
            lawn_size = 250 / map_size[0]
        lawn_size = int(lawn_size)
        global default_lawn_size
        if not default_lawn_size:
            default_lawn_size = deepcopy(lawn_size)
        self.lawn_photo = Image.open(lawn_photo)
        self.lawn_photo = self.lawn_photo.resize((lawn_size, lawn_size),
                                                 Image.ANTIALIAS)
        self.background_img = self.lawn_photo.copy()
        self.lawn_photo = ImageTk.PhotoImage(self.lawn_photo)
        self.action_text = StringVar()
        self.action_text_show = ttk.Label(self, textvariable=self.action_text)
        self.action_text_show.place(x=action_text_place_x,
                                    y=action_text_place_y,
                                    anchor='center')
        pygame.mixer.music.load(choose_plants_music)
        pygame.mixer.music.set_volume(choose_seed_volume)
        pygame.mixer.music.play(loops=-1)
        self.plants_already_choosed = ttk.LabelFrame(self, height=200)
        self.plants_already_choosed.grid(sticky='w')
        self.choose_plants_screen = ttk.LabelFrame(self)
        self.choose_buttons = []
        self.num_plants = len(whole_plants)
        average_height = 200 / (self.num_plants / 5)
        if lawn_size <= average_height:
            average_height = lawn_size
        self.choose_plant_bg = Image.open(choose_plant_bg)
        self.choose_plant_bg = self.choose_plant_bg.resize(
            (lawn_size, lawn_size), Image.ANTIALIAS)
        for i in range(self.num_plants):
            current_plant = whole_plants[i]
            current_img = whole_plants_img[i]
            current_plant[1] = i
            if current_img in pre_transparent:
                current_img = Image.open(current_img)
                ratio = min(lawn_size / current_img.height,
                            lawn_size / current_img.width)
                current_img = current_img.resize(
                    (int(current_img.width * ratio),
                     int(current_img.height * ratio)), Image.ANTIALIAS)
                center_width = int(lawn_size / 2 - current_img.width / 2)
                temp = self.choose_plant_bg.copy()
                temp.paste(current_img, (center_width, 0), current_img)
                current_img = ImageTk.PhotoImage(temp)

            else:
                current_img = Image.open(current_img)
                current_img = current_img.resize(
                    (int(lawn_size), int(lawn_size)), Image.ANTIALIAS)
                current_img = ImageTk.PhotoImage(current_img)
            current_button = ttk.Button(
                self.choose_plants_screen,
                image=current_img,
                command=lambda i=i: self.append_plants(i))
            current_button.image = current_img
            current_button.grid(row=i // 6, column=i % 6)
            self.choose_buttons.append(current_button)
        self.choose_plants_screen.place(x=0, y=200)
        self.start_game = ttk.Button(text='开始游戏', command=self.start_init)
        self.start_game.place(x=0, y=500)
        self.choose_stage_text = ttk.Label(self, text='请选择关卡')
        self.choose_stage_text.place(x=450, y=220)
        self.choose_stages_bar = Scrollbar(self)
        self.choose_stages_bar.place(x=610, y=340, height=170, anchor=CENTER)
        self.choose_stages = Listbox(self,
                                     yscrollcommand=self.choose_stages_bar.set)
        for k in stage_file:
            self.choose_stages.insert(END, k)
        self.choose_stages.place(x=450, y=250)
        self.choose_stages_bar.config(command=self.choose_stages.yview)

    def open_wiki(self):
        os.chdir('..')
        with open('图鉴.pyw', encoding='utf-8') as f:
            exec(f.read(), globals())

    def open_make_stage(self):
        with open('../关卡制作器.pyw', encoding='utf-8') as f:
            exec(f.read(), globals())

    def open_little_game(self):
        filename = filedialog.askopenfilename(initialdir='../小游戏',
                                              title="选择游戏脚本文件",
                                              filetype=(("游戏脚本文件", "*.pzg;"),
                                                        ("所有文件", "*.*")))
        if filename:
            quit()
            read_little_games(filename)

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
            config_window.go_back_button = ttk.Button(
                config_window,
                text='返回主界面',
                command=lambda: self.go_back(config_window))
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

    def make_img(self, each, resize_num=1, types=None):
        current_img = Image.open(each.img).convert('RGBA')
        if each.img_transparent:
            ratio = min(lawn_size / current_img.height,
                        lawn_size / current_img.width)
            current_img = current_img.resize(
                (int(current_img.width * ratio / resize_num),
                 int(current_img.height * ratio / resize_num)),
                Image.ANTIALIAS)
            center_width = int(lawn_size / 2 - current_img.width / 2)
            if types:
                temp = self.background_dict[types].copy()
            else:
                temp = self.background_img.copy()
            temp.paste(current_img, (center_width, 0), current_img)
            each.img = ImageTk.PhotoImage(temp)

        else:
            current_img = current_img.resize(
                (int(lawn_size / resize_num), int(lawn_size / resize_num)),
                Image.ANTIALIAS)
            each.img = ImageTk.PhotoImage(current_img)
        try:
            if each.bullet_img:
                if not each.is_bullet:
                    current_img = Image.open(each.bullet_img)
                    current_img = current_img.resize((lawn_size, lawn_size),
                                                     Image.ANTIALIAS)
                    each.bullet_img = ImageTk.PhotoImage(current_img)
                else:
                    each.bullet_img = Image.open(each.bullet_img)
                    ratio = min((lawn_size / 3) / each.bullet_img.height,
                                (lawn_size / 3) / each.bullet_img.width)
                    each.bullet_img = ImageTk.PhotoImage(
                        each.bullet_img.resize(
                            (int(each.bullet_img.width * ratio),
                             int(each.bullet_img.height * ratio)),
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
                    ratio = min(
                        (lawn_size / resize_num) / current_other_img.height,
                        (lawn_size / resize_num) / current_other_img.width)
                    current_other_img = current_other_img.resize(
                        (int(current_other_img.width * ratio),
                         int(current_other_img.height * ratio)),
                        Image.ANTIALIAS)
                    current_other_img_ls[1] = img_name
                    current_other_img_ls[0] = ImageTk.PhotoImage(
                        current_other_img)
                    if as_bullet:
                        self.bullets_ls.append(img_name)
        except:
            pass

    def draw_choosed_plants(self):
        for each in self.plants_already_choosed.grid_slaves():
            each.destroy()
        for q in range(len(choosed_plants)):
            the_append_plant, number = choosed_plants[q]
            append_button = ttk.Button(self.plants_already_choosed,
                                       image=self.choose_buttons[number].image)
            append_button.configure(
                command=lambda q=q, y=number: self.remove_plants(q, y))
            append_button.grid(row=0, column=q)

    def append_plants(self, i):
        the_append_plant = whole_plants[i]
        self.action_text.set(f'你选择了{the_append_plant[0]}')
        choose_plant_sound.play()
        choosed_plants.append(the_append_plant)
        self.choose_buttons[i].grid_forget()
        self.draw_choosed_plants()

    def remove_plants(self, q, x):
        self.action_text.set(f'你取消选择了{whole_plants[x][0]}')
        del choosed_plants[q]
        self.draw_choosed_plants()
        self.choose_buttons[x].grid(row=x // 6, column=x % 6)

    def start_init(self):
        self.is_stop = False
        self.msg_text = StringVar()
        self.msg_box_text = ttk.Label(self, textvariable=self.msg_text)
        self.msg_lines = 0
        if msg_box:
            self.msg_box_text.place(x=msg_box_x, y=msg_box_y)
        choosed_stage = self.choose_stages.get(ACTIVE)
        with open(f'../stages/{choosed_stage}.py', encoding='utf-8') as f:
            stage_file_contents = f.read()
        exec(stage_file_contents, globals())
        if lawn_size != default_lawn_size:
            self.background_img = self.background_img.resize(
                (int(lawn_size), int(lawn_size)), Image.ANTIALIAS)
        self.stage_name = ttk.Label(self, text=choosed_stage)
        self.stage_name.place(x=10, y=screen_size[1] - 50)
        global choosed_plants
        pygame.mixer.music.stop()
        bg_music = pygame.mixer.music.load(background_music)
        pygame.mixer.music.set_volume(background_volume)
        pygame.mixer.music.play(loops=-1)
        self.music_flag = 1
        self.plants_already_choosed.destroy()
        self.choose_plants_screen.destroy()
        self.start_game.destroy()
        self.choose_stage_text.destroy()
        self.choose_stages.destroy()
        self.choose_stages_bar.destroy()
        self.game_start_time = time.time()
        self.mode = NULL
        self.blocks = []
        self.moving_bullets = []
        self.sunshine_time = self.game_start_time
        choosed_plants = [x[0] for x in choosed_plants]
        os.chdir('..')
        choosed_plants = deepcopy([
            eval(f'importlib.import_module("plant_scripts.{x}").{x}')
            for x in choosed_plants
        ])
        os.chdir('resource')
        if modified_file:
            with open(modified_file, encoding='utf-8') as f:
                exec(f.read())

        self.plants_generate = deepcopy(choosed_plants)
        self.paused_time = 0
        self.get_plant = get_plant
        self.choose = ttk.LabelFrame(self)

        self.init_sunshine()
        self.init_plants()
        self.init_shovel()
        self.choosed_plants = choosed_plants
        self.choose.grid(row=0, sticky='W')
        self.whole_map = LabelFrame(self, borderwidth=0, highlightthickness=0)
        self.whole_map.grid(row=1, sticky='W')
        self.maps = ttk.LabelFrame(self.whole_map)
        self.lawnmower_frame = ttk.LabelFrame(self.whole_map)
        self.lawnmowers = [0 for j in range(map_size[0])]
        self.lawnmower_img = Image.open(lawnmower_img)
        self.lawnmower_img = self.lawnmower_img.resize((lawn_size, lawn_size),
                                                       Image.ANTIALIAS)
        self.lawnmower_img = ImageTk.PhotoImage(self.lawnmower_img)
        self.no_lawnmower_img = Image.open(no_lawnmower_img)
        self.no_lawnmower_img = self.no_lawnmower_img.resize(
            (lawn_size, lawn_size), Image.ANTIALIAS)
        self.no_lawnmower_img = ImageTk.PhotoImage(self.no_lawnmower_img)

        if lawnmower_rows:
            for k in lawnmower_rows:
                current_mower = lawnmower(k, 0, lawnmower_mode,
                                          lawnmower_speed, lawnmower_atack)
                current_mower.show = ttk.Button(
                    self.lawnmower_frame,
                    image=self.lawnmower_img,
                    command=lambda: self.action_text.set('我是一辆小推车'))
                current_mower.show.grid(row=k, column=0, sticky='W')
                self.lawnmowers[k] = current_mower

        self.init_map()
        self.lawnmower_frame.grid(row=0, column=0, sticky='W')
        self.maps.grid(row=0, column=1, sticky='W')
        self.choosed_plant = None
        self.sunshine_ls = []
        self.map_rows, self.map_columns = map_size

        self.bind("<Button-3>", lambda e: self.reset())
        self.bind("<space>", lambda e: self.pause())
        self.zombie_explode_img = Image.open(zombie_explode)
        self.zombie_explode_img = self.zombie_explode_img.resize(
            (lawn_size, lawn_size), Image.ANTIALIAS)
        self.zombie_explode_img = ImageTk.PhotoImage(self.zombie_explode_img)
        self.check_plants()
        self.normal_zombies_num = 0
        self.big_waves_zombies_num = 0
        self.normal_or_wave = 0
        self.whole_zombies = current_stage.get(0)
        self.killed_zombies = 0
        self.zombie_time = self.game_start_time + start_time
        self.killed_zombies_text = StringVar()
        self.killed_zombies_text.set(f'杀死僵尸数: {self.killed_zombies}')
        self.killed_zombies_show = ttk.Label(
            textvariable=self.killed_zombies_text)
        self.killed_zombies_show.place(x=action_text_place_x + 200,
                                       y=action_text_place_y,
                                       anchor='center')
        self.flag_img = Image.open(flag_img)
        self.flag_img = self.flag_img.resize((lawn_size // 2, lawn_size // 2),
                                             Image.ANTIALIAS)
        self.flag_img = ImageTk.PhotoImage(self.flag_img)
        self.damaged_flag_img = Image.open(damaged_flag_img)
        self.damaged_flag_img = self.damaged_flag_img.resize(
            (lawn_size // 2, lawn_size // 2), Image.ANTIALIAS)
        self.damaged_flag_img = ImageTk.PhotoImage(self.damaged_flag_img)
        self.head_img = Image.open(zombie_head_img)
        self.head_img = self.head_img.resize((lawn_size // 2, lawn_size // 2),
                                             Image.ANTIALIAS)
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
                              y=action_text_place_y + 50,
                              anchor='center')
        self.current_ind = -1
        self.current_zombies_num = len(self.whole_zombies)
        self.current_killed_zombies = 0
        self._zombie1 = self.after(int(start_time * 1000),
                                   zombies_coming_sound.play)
        self._zombie2 = self.after(int(start_time * 1000), self.check_zombies)
        global first_time
        first_time = False

    def pause(self):
        if self.mode != PAUSE:
            self.mode = PAUSE
            self.action_text.set("游戏暂停,按P继续")
            pygame.mixer.music.pause()
            pause_sound.play()
            self.paused_start = time.time()

    def reset(self):
        if self.mode == PLACE or self.mode == REMOVE:
            random.choice(reset_sound).play()
        self.change_mode(NULL)

    def msg_refresh(self):
        self.msg_text.set('')

    def msg_write(self, text, newline=True):
        if self.msg_lines >= msg_lines_limit:
            self.msg_refresh()
            self.msg_lines = 0
        content = self.msg_text.get()
        if newline:
            self.msg_lines += 1
            content += '\n'
        content += text
        self.msg_text.set(content)

    def init_sunshine(self):
        sun_photo = ImageTk.PhotoImage(
            Image.open(sunshine_img).resize((lawn_size, lawn_size),
                                            Image.ANTIALIAS))
        self.sunshine = init_sunshine
        self.sunshine_text = StringVar()
        self.sunshine_text.set(self.sunshine)
        self.sunshine_show = ttk.Label(self.choose,
                                       textvariable=self.sunshine_text,
                                       image=sun_photo,
                                       compound=TOP)
        self.sunshine_show.image = sun_photo
        self.sunshine_show.grid(row=0, column=0)
        self.fall_sunshine_img = ImageTk.PhotoImage(
            Image.open(fall_sunshine_img).resize((lawn_size, lawn_size),
                                                 Image.ANTIALIAS))
        self.flower_sunshine_img = ImageTk.PhotoImage(
            Image.open(fall_sunshine_img).resize((lawn_size, lawn_size),
                                                 Image.ANTIALIAS))

    def init_plants(self):
        self.bullets_ls = []
        self.plants_num = len(choosed_plants)
        for i in range(self.plants_num):
            plants_info = choosed_plants[i]
            self.make_img(plants_info)
            if plants_info.bullet_img and plants_info.is_bullet:
                self.bullets_ls.append(plants_info.bullet_img_name)
            current_text = StringVar()
            if not plants_info.no_cooling_start:
                current_text.set(f'${plants_info.price} 冷却中')
            else:
                current_text.set(f'${plants_info.price}')
            current_button = ttk.Button(
                self.choose,
                image=plants_info.img,
                textvariable=current_text,
                compound=TOP,
                command=lambda i=i: self.change_mode(PLACE, i))
            current_button.image = plants_info.img
            current_button.textvariable = current_text
            current_button.grid(row=0, column=i + 1)
            plants_info.button = current_button
            plants_info.counter = self.game_start_time
            plants_info.enable = 1 if plants_info.no_cooling_start else 0

    def init_shovel(self):
        shovel_photo = ImageTk.PhotoImage(
            Image.open(shovel_img).resize((lawn_size, lawn_size),
                                          Image.ANTIALIAS))
        self.shovel_button = ttk.Button(
            self.choose,
            image=shovel_photo,
            command=lambda: self.change_mode(REMOVE))
        self.shovel_button.image = shovel_photo
        self.shovel_button.grid(row=0, column=self.plants_num + 1)

    def init_map(self):
        self.background_dict = {}
        for each_type in self.map_img_dict:
            current_bg = Image.open(self.map_img_dict[each_type]).resize(
                (lawn_size, lawn_size), Image.ANTIALIAS)
            self.background_dict[each_type] = current_bg.copy()
            self.map_img_dict[each_type] = ImageTk.PhotoImage(current_bg)
        rows, columns = len(map_content), len(map_content[0])
        for j in range(rows):
            block_row = []
            for k in range(columns):
                current_type = map_content[j][k]
                lawn_photo = self.map_img_dict[current_type]
                current_block = ttk.Button(
                    self.maps,
                    image=lawn_photo,
                    command=lambda j=j, k=k: self.block_action(j, k))
                current_block.plants = None
                current_block.types = current_type
                current_block.image = lawn_photo
                current_block.grid(row=j, column=k)
                block_row.append(current_block)
            self.blocks.append(block_row)

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
            elif num == NULL:
                self.action_text.set('')

    def block_action(self, j, k=None, mode=0):
        if self.mode != PAUSE:
            if mode == 1:
                dim = j.rows, j.columns
                j, k = dim
            if self.mode == PLACE:
                current = self.blocks[j][k]
                choose_plant = self.plants_generate[self.choosed_plant]
                if any(
                        cond(self, current) if callable(cond) else current.
                        types == cond for cond in choose_plant.plant_range):
                    current_time = self.current_time
                    ready_plants = get_plant(choose_plant, j, k)
                    if ready_plants.bullet_sound:
                        for each in ready_plants.bullet_sound:
                            if type(each) == list:
                                for each_sound in each:
                                    each_sound.set_volume(self.sound_volume)
                            else:
                                each.set_volume(self.sound_volume)
                    self.make_img(ready_plants, types=current.types)
                    if ready_plants.use_bullet_img_first:
                        current.configure(image=ready_plants.bullet_img)
                    else:
                        current.configure(image=ready_plants.img)

                    ready_plants.time = current_time
                    current_plant_name = ready_plants.name
                    current_choosed_plants = choosed_plants[self.choosed_plant]
                    ready_plants.button = current_choosed_plants.button
                    set_plants_sound.play()
                    self.action_text.set(
                        f'你成功放置了{current_plant_name}在第{j+1}行，第{k+1}列')
                    ready_plants.button.textvariable.set(
                        f'${ready_plants.price} 冷却中')
                    current_choosed_plants.counter = current_time
                    current_choosed_plants.enable = 0
                    self.sunshine -= ready_plants.price
                    self.sunshine_text.set(self.sunshine)
                    if not ready_plants.plant_func:
                        current.plants = ready_plants
                    else:
                        ready_plants.plant_func(self, current, ready_plants)
                    self.choosed_plant = None
                    self.mode = NULL
                else:
                    if current.plants:
                        self.action_text.set('这里已经有植物了，要种的话请先铲掉')

            elif self.mode == REMOVE:
                block = self.blocks[j][k]
                if block.plants is not None:
                    if block.plants.away_func:
                        block.plants.away_func(block.plants, self)
                    if block.plants.away_self_func:
                        block.plants.away_self_func(block.plants, self, block)
                    else:
                        block.configure(image=self.map_img_dict[block.types])
                        unset_plants_sound.play()
                        self.action_text.set(
                            f'你铲除了第{j+1}行，第{k+1}列的植物{block.plants.name}')

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
                        if plants_on_block.name == '荷叶' and plants_on_block.contain_plants:
                            plants_on_block = plants_on_block.contain_plants
                        zombies_message += '\n'
                        zombies_message += f'这上面有个{plants_on_block.name}, 当前生命值{plants_on_block.hp}'
                    self.action_text.set(zombies_message)
                else:
                    plants_on_block = self.blocks[j][k].plants
                    if not plants_on_block:
                        self.action_text.set('这是一块空荡荡的草坪')
                    else:
                        if plants_on_block.name == '荷叶' and plants_on_block.contain_plants:
                            plants_on_block = plants_on_block.contain_plants
                        self.action_text.set(
                            f'这上面有个{plants_on_block.name}, 当前生命值{plants_on_block.hp}'
                        )

    def appear_sunshine(self):
        if self.mode != PAUSE:
            sunshine_appear = ttk.Button(self.choose,
                                         image=self.fall_sunshine_img,
                                         command=self.get_sunshine)
            sunshine_appear.image = self.fall_sunshine_img
            sunshine_appear.grid(row=0, column=self.plants_num + 2)
            self.sunshine_ls.append(sunshine_appear)

    def get_sunshine(self):
        if self.mode != PAUSE:
            self.sunshine += sky_sunshine
            self.sunshine_text.set(self.sunshine)
            get_sunshine_sound.play()
            self.action_text.set(f'成功拿到了{sky_sunshine}点阳光')
            if self.sunshine_ls:
                self.sunshine_ls.pop().destroy()

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
        self.make_img(current_zombies,
                      types=self.blocks[current_zombies.rows][
                          current_zombies.columns].types)
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

    def lawnmower_clear(self, obj):
        left_zombies = [
            each for each in self.whole_zombies
            if each.status == 1 and each.rows == obj.rows and each.columns <= 0
        ]
        if left_zombies:
            if obj.mode == 0:
                for each in left_zombies:
                    each.hp = 0
                    if each.eachtime_func:
                        each.runs(self, num=1)
                    each.status = 0
                    self.killed_zombies += 1
                    self.current_killed_zombies += 1
                    self.killed_zombies_text.set(
                        f'杀死僵尸数: {self.killed_zombies}')
                    self.zombie_dead_normal(each)
            elif obj.mode == 1:
                for each in left_zombies:
                    each.hp -= obj.attack

    def lawnmower_move(self, obj):
        if self.is_stop:
            return
        if obj.columns == 0:
            lawnmower_sound.play()
        if obj.columns >= self.map_columns:
            obj.destroy()
            return
        self.lawnmower_clear(obj)
        attack_size = [obj.columns, obj.columns + 1]
        current_zombies = [
            each for each in self.whole_zombies if each.status == 1
            and each.rows == obj.rows and each.columns in attack_size
        ]

        if current_zombies:
            if obj.mode == 0:
                for each in current_zombies:
                    each.hp = 0
                    if each.eachtime_func:
                        each.runs(self, num=1)
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
        if self.is_stop:
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
            self.current_time = time.time()
            if self.current_time - self.sunshine_time >= sunshine_cooling_time:
                self.appear_sunshine()
                self.sunshine_time = self.current_time
            for each_plant in choosed_plants:
                if self.current_time - each_plant.counter > each_plant.cooling_time:
                    each_plant.enable = 1
                    each_plant.button.textvariable.set(f'${each_plant.price}')
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
                                current.configure(
                                    image=self.map_img_dict[current.types])
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
                                    (lawn_size, lawn_size), Image.ANTIALIAS)
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
        if self.is_stop:
            return
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
                        #self.mode = PAUSE
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
                        if each.eachtime_func:
                            each.runs(self, num=1)
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
                                    (lawn_size, lawn_size), Image.ANTIALIAS)
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
        pygame.mixer.music.stop()
        win_sound.play()
        self.after(5000, self.ask_if_continue)

    def go_back(self, obj):
        self.is_stop = True
        self.mode = PAUSE
        if self._zombie1:
            self.after_cancel(self._zombie1)
        if self._zombie2:
            self.after_cancel(self._zombie2)
        if msg_box:
            self.msg_box_text.place_forget()
        global modified_file
        modified_file = None
        global map_size
        map_size = default_map_size
        global map_content
        map_content = deepcopy(default_map_content)
        global lawnmower_rows
        lawnmower_rows = deepcopy(default_lawnmower_rows)
        global choosed_plants
        choosed_plants = []
        global lawn_size
        if lawn_size != default_lawn_size:
            self.background_img = self.background_img.resize(
                (default_lawn_size, default_lawn_size), Image.ANTIALIAS)
        lawn_size = deepcopy(default_lawn_size)
        self.lawn_photo = self.background_img.copy()
        self.lawn_photo = self.lawn_photo.resize((lawn_size, lawn_size),
                                                 Image.ANTIALIAS)
        self.lawn_photo = ImageTk.PhotoImage(self.lawn_photo)
        self.map_img_dict = deepcopy(default_map_img_dict)
        obj.destroy()
        self.choose.destroy()
        self.whole_map.destroy()
        self.maps.destroy()
        self.zombie_bar.destroy()
        self.action_text.set('')
        self.killed_zombies_text.set('')
        self.stage_name.destroy()
        self.music_flag = 0
        pygame.mixer.music.load(choose_plants_music)
        pygame.mixer.music.set_volume(choose_seed_volume)
        pygame.mixer.music.play(loops=-1)
        self.plants_already_choosed = ttk.LabelFrame(self, height=200)
        self.plants_already_choosed.grid(sticky='w')
        self.choose_plants_screen = ttk.LabelFrame(self)
        self.choose_plants_screen.place(x=0, y=200)
        self.choose_buttons = []
        self.num_plants = len(whole_plants)
        average_height = 200 / (self.num_plants / 5)
        if lawn_size <= average_height:
            average_height = lawn_size
        for i in range(self.num_plants):
            current_plant = whole_plants[i]
            current_img = whole_plants_img[i]
            current_plant[1] = i
            if current_img in pre_transparent:
                current_img = Image.open(current_img)
                ratio = min(lawn_size / current_img.height,
                            lawn_size / current_img.width)
                current_img = current_img.resize(
                    (int(current_img.width * ratio),
                     int(current_img.height * ratio)), Image.ANTIALIAS)
                center_width = int(lawn_size / 2 - current_img.width / 2)
                temp = self.choose_plant_bg.copy()
                temp.paste(current_img, (center_width, 0), current_img)
                current_img = ImageTk.PhotoImage(temp)

            else:
                current_img = Image.open(current_img)
                current_img = current_img.resize(
                    (int(lawn_size), int(lawn_size)), Image.ANTIALIAS)
                current_img = ImageTk.PhotoImage(current_img)
            current_button = ttk.Button(
                self.choose_plants_screen,
                image=current_img,
                command=lambda i=i: self.append_plants(i))
            current_button.image = current_img
            current_button.grid(row=i // 6, column=i % 6)
            self.choose_buttons.append(current_button)
        self.start_game = ttk.Button(text='开始游戏', command=self.start_init)
        self.start_game.place(x=0, y=500)
        self.choose_stage_text = ttk.Label(self, text='请选择关卡')
        self.choose_stage_text.place(x=450, y=220)
        self.choose_stages_bar = Scrollbar(self)
        self.choose_stages_bar.place(x=610, y=340, height=170, anchor=CENTER)
        self.choose_stages = Listbox(self,
                                     yscrollcommand=self.choose_stages_bar.set)
        for k in stage_file:
            self.choose_stages.insert(END, k)
        self.choose_stages.place(x=450, y=250)
        self.choose_stages_bar.config(command=self.choose_stages.yview)

    def ask_if_continue(self):
        self.is_stop = True
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x, y = self.winfo_x(), self.winfo_y()
        ask_window = Toplevel(self)
        ask_window.title('继续游戏')
        ask_window.minsize(300, 200)
        ask_window.update()
        ask_window.geometry('%dx%d+%d+%d' % (300, 200, x, y))
        ask_window.ask_text = ttk.Label(ask_window,
                                        text='请问要返回选择植物和关卡的界面还是退出游戏？')
        ask_window.ask_text.place(x=0, y=0)
        ask_window.back_button = ttk.Button(
            ask_window, text='返回主界面', command=lambda: self.go_back(ask_window))
        ask_window.quit_button = ttk.Button(ask_window,
                                            text='退出',
                                            command=quit)
        ask_window.back_button.place(x=0, y=30)
        ask_window.quit_button.place(x=100, y=30)


root = Root()


def quit():
    pygame.mixer.quit()
    root.destroy()


def read_little_games(filename):
    os.chdir('../小游戏')
    with open(filename, encoding='utf-8') as f:
        exec(f.read(), globals())


root.protocol('WM_DELETE_WINDOW', quit)
root.mainloop()
