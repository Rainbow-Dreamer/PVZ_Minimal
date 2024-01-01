import os
import sys
import importlib
import pygame
import time
import random
import keyboard
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from copy import deepcopy
import json


def go_back():
    pygame.mixer.quit()
    root.destroy()
    os.chdir('..')
    os.startfile('pvz极简版.exe')


def quit():
    pygame.mixer.quit()
    root.destroy()


def sounds(x):
    return pygame.mixer.Sound(x).get_raw()


class json_module:

    def __init__(self, file, text=None):
        if text is None:
            with open(file, encoding='utf-8') as f:
                text = json.load(f)
        for i, j in text.items():
            setattr(self, i, j)

    def to_json(self):
        return vars(self)


class Stage:

    def __init__(self, stages):
        # number of waves means number of flags (when a big wave of zombies will come)
        normals = []
        waves = []
        for stage in stages:
            current_zombies = [
                root.get_zombies(
                    random.choice(
                        [globals()[each] for each in stage['zombies']]),
                    random.randint(*stage['appear_rows_range'])
                    if len(stage['appear_rows_range']) == 2 else
                    stage['appear_rows_range'][0],
                    random.randint(*stage['appear_columns_range'])
                    if len(stage['appear_columns_range']) == 2 else
                    stage['appear_columns_range'][0],
                    random.randint(*stage['appear_times_range'])
                    if len(stage['appear_times_range']) == 2 else
                    stage['appear_times_range'][0])
                for i in range(stage['quantity'])
            ]
            if not stage['is_big_wave']:
                normals.append(current_zombies)
            else:
                waves.append(current_zombies)

        self.num_of_waves = len(waves)
        self.normal_zombies = [[]
                               for i in range(len(stages) - self.num_of_waves)]
        self.big_waves_zombies = [[] for i in range(self.num_of_waves)]
        self.set_normal_all(normals)
        self.set_waves_all(waves)

    def set_normal(self, num, zombie_ls):
        if num in range(self.num_of_waves + 1):
            self.normal_zombies[num] = zombie_ls

    def set_waves(self, num, zombie_ls):
        if num in range(self.num_of_waves):
            self.big_waves_zombies[num] = zombie_ls

    def set_normal_all(self, zombie_ls):
        for k in range(len(zombie_ls)):
            self.normal_zombies[k] = zombie_ls[k]

    def set_waves_all(self, zombie_ls):
        for k in range(len(zombie_ls)):
            self.big_waves_zombies[k] = zombie_ls[k]

    def get(self, num, mode=0):
        if mode == 0:
            return self.normal_zombies[num]
        elif mode == 1:
            return self.big_waves_zombies[num]


class lawnmower:

    def __init__(self, rows, columns, mode=0, move_speed=500, attack=None):
        # if mode == 0, the lawn mower will kill all zombies in the row by setting their hp to 0
        # if mode == 1, the lawn mower will have only give an attack to all of the zombies i the row
        self.rows = rows
        self.columns = columns
        self.mode = mode
        self.move_speed = move_speed
        self.attack = attack


def go_back():
    pygame.mixer.quit()
    root.destroy()
    os.chdir('..')
    os.startfile('pvz极简版.exe')


class Root(Tk):

    def __init__(self):
        super(Root, self).__init__()
        self.protocol('WM_DELETE_WINDOW', quit)
        pygame.mixer.init()
        self.init_main_window()

    def init_main_window(self):
        os.chdir('我是僵尸')
        self.json_config_path = "game_config.json"
        self.current_config = json_module(self.json_config_path)
        os.chdir('../../../resources')
        self.wm_iconbitmap(self.current_config.icon_name)
        self.title('我是僵尸')
        self.minsize(*self.current_config.screen_size)
        self.back_button = ttk.Button(self, text='返回', command=go_back)
        self.back_button.place(x=self.current_config.screen_size[0] - 100, y=0)
        self.make_label = ttk.Label
        self.make_button = ttk.Button
        self.NULL, self.PLACE, self.REMOVE, self.PAUSE = self.current_config.NULL, self.current_config.PLACE, self.current_config.REMOVE, self.current_config.PAUSE
        self.whole_zombies = []
        self.lawn_photo = Image.open(self.current_config.lawn_photo)
        os.chdir('../scripts/games/我是僵尸')
        whole_plants_name = None
        if whole_plants_name is None:
            whole_plants_name = os.listdir('plant_scripts_I_am_zombie')
            except_ls = [
                '__pycache__', '__init__.py', 'plant2.py', 'bullets.py'
            ]
            for each in except_ls:
                if each in whole_plants_name:
                    whole_plants_name.remove(each)
            whole_plants_name = [x[:-3] for x in whole_plants_name]
        sys.path.append('.')
        self.whole_plants = [
            eval(
                f'__import__("plant_scripts_I_am_zombie.{x}", fromlist=["plant_scripts_I_am_zombie"]).{x}'
            ) for x in whole_plants_name
        ]
        os.chdir('../../../resources')
        self.plants_num = len(self.whole_plants)
        self.whole_plants = self.whole_plants
        self.paused_time = 0
        self.sound_volume = self.current_config.whole_sound_volume
        self.music_flag = 1
        lawn_size = 250 // self.current_config.map_size[0]
        self.lawn_photo = self.lawn_photo.resize((lawn_size, lawn_size),
                                                 Image.Resampling.LANCZOS)
        self.background_img = self.lawn_photo.copy()
        self.lawn_photo = ImageTk.PhotoImage(self.lawn_photo)
        self.lawn_width, self.lawn_height = self.lawn_photo.width(
        ), self.lawn_photo.height()
        self.action_text = StringVar()
        self.action_text_show = ttk.Label(self, textvariable=self.action_text)
        self.action_text_place_y = self.current_config.map_size[0] * (
            self.lawn_height + 10) + 150
        self.action_text_show.place(x=self.current_config.action_text_place_x,
                                    y=self.action_text_place_y,
                                    anchor='center')

        self.current_config.whole_sound_names = [
            'sunshine_not_enough', 'choose_plants_sound', 'set_plants_sound',
            'unset_plants_sound', 'pick_shovel_sound', 'get_sunshine_sound',
            'plant_bite_sound', 'reset_sound', 'pause_sound', 'lose_sound',
            'choose_plant_sound', 'zombies_coming_sound', 'huge_wave_sound',
            'lawnmower_sound', 'win_sound', "swing_sound", "hammer_sound"
        ]
        for each in self.current_config.whole_sound_names:
            setattr(self.current_config, each,
                    pygame.mixer.Sound(getattr(self.current_config, each)))
        self.current_config.choosed_plants = []
        self.current_config.whole_sounds = [
            getattr(self.current_config, i)
            for i in self.current_config.whole_sound_names
        ]

        pygame.mixer.music.load(self.current_config.background_music)
        pygame.mixer.music.set_volume(self.current_config.background_volume)
        pygame.mixer.music.play(loops=-1)
        game_start_time = time.time()
        self.game_start_time = game_start_time
        self.mode = self.NULL
        self.blocks = []
        self.moving_bullets = []
        self.sunshine_time = game_start_time
        if self.current_config.modified_file:
            with open(self.current_config.modified_file,
                      encoding='utf-8') as f:
                exec(f.read())

        self.init_stage()

        self.plants_generate = deepcopy(self.choosed_zombies_list)

        self.configs = ttk.Button(self,
                                  text='设置',
                                  command=self.make_config_window)

        self.configs.place(x=self.current_config.screen_size[0] - 100,
                           y=self.current_config.screen_size[1] - 60)

        self.choose = ttk.LabelFrame(self)
        self.maps = ttk.LabelFrame(self)
        self.init_sunshine()
        self.init_zombies()
        self.plant_bite_sound = self.current_config.plant_bite_sound
        self.choose.grid(row=0, column=0, sticky='W')
        self.brains = [5 for j in range(self.current_config.map_size[0])]
        self.brains_show = []
        self.brain_img = Image.open(self.current_config.brain_img)
        self.brain_img = self.brain_img.resize(
            (self.lawn_width, self.lawn_height), Image.Resampling.LANCZOS)
        self.brain_img = ImageTk.PhotoImage(self.brain_img)
        self.no_brain_img = Image.open(self.current_config.no_lawnmower_img)
        self.no_brain_img = self.no_brain_img.resize(
            (self.lawn_width, self.lawn_height), Image.Resampling.LANCZOS)
        self.no_brain_img = ImageTk.PhotoImage(self.no_brain_img)
        self.brain_part = ttk.LabelFrame(self)
        self.brain_part.place(x=0, y=100)
        for k in range(self.current_config.map_size[0]):
            current_brain = ttk.Button(
                self.brain_part,
                image=self.brain_img,
                command=lambda: self.action_text.set('我是一个脑子'))
            current_brain.grid(row=k, column=0, sticky='W')
            self.brains_show.append(current_brain)

        self.init_map(*self.current_config.map_size)
        self.maps.place(x=65, y=100)
        self.sunshine_ls = []
        self.map_rows, self.map_columns = self.current_config.map_size
        self.init_plant_ls()
        self.bind("<Button-3>", lambda e: self.reset())
        self.bind("<space>", lambda e: self.pause())
        self.zombie_explode_img = Image.open(
            self.current_config.zombie_explode)
        self.zombie_explode_img = self.zombie_explode_img.resize(
            (self.lawn_width, self.lawn_height), Image.Resampling.LANCZOS)
        self.zombie_explode_img = ImageTk.PhotoImage(self.zombie_explode_img)

        self.killed_zombies = 0
        self.killed_zombies_text = StringVar()
        self.current_killed_zombies = 0
        self.killed_zombies_text.set(f'杀死僵尸数: {self.killed_zombies}')
        self.killed_zombies_show = ttk.Label(
            textvariable=self.killed_zombies_text)
        self.killed_zombies_show.place(
            x=self.current_config.action_text_place_x + 200,
            y=self.action_text_place_y,
            anchor='center')

        self.zombie_time = time.time()
        self.check_plants()
        self.check_zombies()

    def init_stage(self):
        self.plant_line = 5
        self.plants_list = [[
            random.choice(self.whole_plants) for j in range(self.plant_line)
        ] for i in range(self.current_config.map_size[0])]
        num_of_sunflowers = len(
            [i for j in self.plants_list for i in j if i.name == '向日葵'])
        if num_of_sunflowers < 5:
            difference = 5 - num_of_sunflowers
            sunflower_obj = [i for i in self.whole_plants
                             if i.name == '向日葵'][0]
            whole_inds = [[i, j] for i in range(self.plant_line)
                          for j in range(self.current_config.map_size[0])]
            replace_inds = random.sample(whole_inds, difference)
            for k in replace_inds:
                self.plants_list[k[0]][k[1]] = sunflower_obj
        os.chdir('../scripts/games/我是僵尸')
        sys.path.append('.')
        zombies_names = ['普通僵尸', '路障僵尸', '读报僵尸', '铁桶僵尸', '撑杆僵尸', '舞王僵尸']
        for x in zombies_names:
            exec(f'from zombie_scripts_I_am_zombie.{x} import {x}', globals(),
                 globals())
        zombies_sample = [eval(j, globals(), globals()) for j in zombies_names]
        for each in zombies_sample:
            each.move_speed /= 1.4
        os.chdir('../../../resources/')
        for current_zombies in zombies_sample:
            current_zombies.attack_sound = [
                sounds(j) for j in current_zombies.attack_sound
            ]
            current_zombies.dead_sound = [
                sounds(j) if type(j) != list else [sounds(k) for k in j]
                for j in current_zombies.dead_sound
            ]
            current_zombies.hit_sound = [
                sounds(j) for j in current_zombies.hit_sound
            ]
            if current_zombies.hit_sound_ls:
                for k in range(len(current_zombies.hit_sound_ls)):
                    current = current_zombies.hit_sound_ls[k][1]
                    current_zombies.hit_sound_ls[k][1] = sounds(
                        current) if type(current) != list else [
                            sounds(y) for y in current
                        ]
            if current_zombies.other_sound:
                current_zombies.other_sound = [
                    sounds(k) for k in current_zombies.other_sound
                ]
        self.choosed_zombies_list = zombies_sample

    def reset_whole_sounds(self):
        for each in self.current_config.whole_sounds:
            if type(each) == list:
                for i in each:
                    i.set_volume(self.sound_volume)
            else:
                each.set_volume(self.sound_volume)

    def init_plant_ls(self):
        self.bullets_ls = []
        current_time = time.time()
        for i in range(self.current_config.map_size[0]):
            for j in range(self.plant_line):
                current_plant = self.plants_list[i][j]
                current = self.blocks[i][j]
                current.plants = self.get_plant(current_plant, i, j)
                current.plants.counter = current_time
                current.plants.time = current_time
                self.make_img(current.plants)
                if current.plants.bullet_img and current.plants.is_bullet and current.plants.bullet_img_name not in self.bullets_ls:
                    self.bullets_ls.append(current.plants.bullet_img_name)
                if current.plants.use_bullet_img_first:
                    current.configure(image=current.plants.bullet_img)
                else:
                    current.configure(image=current.plants.img)

    def get_plant(self, plant_obj, rows=None, columns=None):
        result = deepcopy(plant_obj)
        if result.bullet_sound:
            result.bullet_sound = [
                pygame.mixer.Sound(j)
                if type(j) != list else [pygame.mixer.Sound(k) for k in j]
                for j in result.bullet_sound
            ]
            self.current_config.whole_sounds.extend(result.bullet_sound)
        result.rows = rows
        result.columns = columns
        self.reset_whole_sounds()
        return result

    def get_zombies(self, zombies_obj, rows, columns, appear_time=None):
        result = deepcopy(zombies_obj)
        result.rows = rows
        result.columns = columns
        result.appear_time = appear_time
        return result

    def make_img(self, each, resize_num=1):
        current_img = Image.open(each.img)
        if each.img_transparent:
            ratio = self.lawn_height / current_img.height
            current_img = current_img.resize(
                (int(current_img.width * ratio / resize_num),
                 int(current_img.height * ratio / resize_num)),
                Image.Resampling.LANCZOS)
            center_width = int(self.lawn_width / 2 - current_img.width / 2)
            temp = self.background_img.copy()
            temp.paste(current_img, (center_width, 0), current_img)
            each.img = ImageTk.PhotoImage(temp)

        else:
            current_img = current_img.resize(
                (int(self.lawn_width / resize_num),
                 int(self.lawn_height / resize_num)), Image.Resampling.LANCZOS)
            each.img = ImageTk.PhotoImage(current_img)
        try:
            if each.bullet_img:
                if not each.is_bullet:
                    current_img = Image.open(each.bullet_img)
                    current_img = current_img.resize(
                        (self.lawn_width, self.lawn_height),
                        Image.Resampling.LANCZOS)
                    each.bullet_img = ImageTk.PhotoImage(current_img)
                else:
                    each.bullet_img = ImageTk.PhotoImage(
                        Image.open(each.bullet_img).resize(
                            (self.lawn_width // 3, self.lawn_height // 3),
                            Image.Resampling.LANCZOS))
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
                    current_other_img = current_other_img.resize(
                        (int(self.lawn_width / resize_num),
                         int(self.lawn_height / resize_num)),
                        Image.Resampling.LANCZOS)
                    current_other_img_ls[1] = img_name
                    current_other_img_ls[0] = ImageTk.PhotoImage(
                        current_other_img)
                    if as_bullet:
                        self.bullets_ls.append(img_name)
        except:
            pass

    def pause(self):
        if self.mode != self.PAUSE:
            self.mode = self.PAUSE
            self.action_text.set("游戏暂停,按P继续")
            pygame.mixer.music.pause()
            self.current_config.pause_sound.play()
            self.paused_start = time.time()

    def reset(self):
        if self.mode == self.PLACE or self.mode == self.REMOVE:
            self.current_config.reset_sound.play()
        self.change_mode(self.NULL)

    def init_sunshine(self):
        sun_photo = ImageTk.PhotoImage(
            Image.open(self.current_config.sunshine_img).resize(
                (self.lawn_width, self.lawn_height), Image.Resampling.LANCZOS))
        self.sunshine = self.current_config.init_sunshine
        self.sunshine_text = StringVar()
        self.sunshine_text.set(self.sunshine)
        self.sunshine_show = ttk.Label(self.choose,
                                       textvariable=self.sunshine_text,
                                       image=sun_photo,
                                       compound=TOP)
        self.sunshine_show.image = sun_photo
        self.sunshine_show.grid(row=0, column=0)
        self.fall_sunshine_img = ImageTk.PhotoImage(
            Image.open(self.current_config.fall_sunshine_img).resize(
                (self.lawn_width, self.lawn_height), Image.Resampling.LANCZOS))
        self.flower_sunshine_img = ImageTk.PhotoImage(
            Image.open(self.current_config.fall_sunshine_img).resize(
                (self.lawn_width, self.lawn_height), Image.Resampling.LANCZOS))

    def init_zombies(self):
        self.zombies_num = len(self.choosed_zombies_list)
        for i in range(self.zombies_num):
            zombies_info = self.choosed_zombies_list[i]
            self.make_img(zombies_info)
            current_text = StringVar()
            current_text.set(f'${zombies_info.price}')
            current_button = ttk.Button(
                self.choose,
                image=zombies_info.img,
                textvariable=current_text,
                compound=TOP,
                command=lambda i=i: self.change_mode(self.PLACE, i))
            current_button.image = zombies_info.img
            current_button.textvariable = current_text
            current_button.grid(row=0, column=i + 1)
            zombies_info.button = current_button
            zombies_info.enable = 1

    def init_map(self, rows, columns):
        lawn_photo = self.lawn_photo
        for j in range(rows):
            block_row = []
            for k in range(columns):
                current_block = ttk.Button(
                    self.maps,
                    image=lawn_photo,
                    command=lambda j=j, k=k: self.block_action(j, k))
                current_block.plants = None
                current_block.image = lawn_photo
                current_block.grid(row=j, column=k)
                block_row.append(current_block)
            self.blocks.append(block_row)
        self.lawn_photo = lawn_photo

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
            config_window.bg.insert(END, self.current_config.background_music)
        elif self.music_flag == 0:
            config_window.bg.insert(END,
                                    self.current_config.choose_plants_music)
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

    def change_bg(self, config_window):
        filename = filedialog.askopenfilename(title="选择你想播放的背景音乐",
                                              filetypes=(("音乐文件",
                                                          ".mp3 .ogg .wav"),
                                                         ("所有文件", "*.*")))
        if filename:
            if self.music_flag == 1:
                background_music = filename
                pygame.mixer.music.stop()
                pygame.mixer.music.load(background_music)
                pygame.mixer.music.play(loops=-1)
                config_window.bg.delete('1.0', END)
                config_window.bg.insert(END, background_music)
            elif self.music_flag == 0:
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

    def change_sound_volume(self, config_window):
        new_volume = config_window.sound_volume.get()
        if new_volume != int(self.sound_volume * 100):
            new_set_volume = new_volume / 100
            self.reset_whole_sounds()
            self.sound_volume = new_set_volume

    def change_mode(self, num, zombies=None):
        if self.mode != self.PAUSE:
            self.mode = num
            if num == self.PLACE:
                current_plant = self.choosed_zombies_list[zombies]
                if current_plant.enable == 0:
                    self.current_config.sunshine_not_enough.play()
                    self.action_text.set(f'{current_plant.name}正在冷却中')
                    self.mode = self.NULL
                elif self.sunshine < current_plant.price:
                    self.current_config.sunshine_not_enough.play()
                    self.action_text.set('阳光不够哦')
                    self.mode = self.NULL
                else:
                    self.current_config.choose_plants_sound.play()
                    self.action_text.set(f'你选择了{current_plant.name}')
                    self.choosed_zombies = zombies

            elif num == self.REMOVE:
                self.current_config.pick_shovel_sound.play()
                self.action_text.set('请选择一个草地上的植物铲除')
            elif num == self.NULL:
                self.action_text.set('')

    def block_action(self, j, k=None, mode=0):
        if self.mode != self.PAUSE:
            if mode == 1:
                dim = j.rows, j.columns
                j, k = dim
            if self.mode == self.PLACE:
                if k < self.plant_line - 1:
                    self.current_config.sunshine_not_enough.play()
                    self.action_text.set('请种植在第5列或者其右边')
                    self.mode = self.NULL
                else:
                    current = self.blocks[j][k]
                    current_time = self.current_time
                    choose_zombies = self.plants_generate[self.choosed_zombies]
                    current_zombies = self.get_zombies(choose_zombies, j, k, 0)
                    self.make_img(current_zombies)
                    self.set_zombies(current_zombies)
                    if current.plants:
                        current_zombies.button.grid(row=j, column=k)
                    current_zombies.alive()
                    if current_zombies.start_func:
                        current_zombies.runs(self, num=0)
                    current_zombies.time = current_time
                    current_zombies_name = current_zombies.name
                    self.current_config.set_plants_sound.play()
                    self.action_text.set(
                        f'你成功放置了{current_zombies_name}在第{j+1}行，第{k+1}列')
                    self.sunshine -= current_zombies.price
                    self.sunshine_text.set(self.sunshine)
                    self.whole_zombies.append(current_zombies)
                    self.mode = self.NULL

            elif self.mode == self.REMOVE:
                block = self.blocks[j][k]
                if block.plants is not None:
                    block.configure(image=self.lawn_photo)
                    self.current_config.unset_plants_sound.play()
                    self.action_text.set(
                        f'你铲除了第{j+1}行，第{k+1}列的植物{block.plants.name}')
                    block.plants.status = 0
                    block.plants = None
                else:
                    self.action_text.set('这里并没有植物，请问您要铲什么？')
                self.mode = self.NULL
            else:
                if mode == 1 and self.current_config.show_zombies:
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

    def get_sunshine(self):
        if self.mode != self.PAUSE:
            self.sunshine += self.current_config.sky_sunshine
            self.sunshine_text.set(self.sunshine)
            self.current_config.get_sunshine_sound.play()
            self.action_text.set(f'成功拿到了{self.current_config.sky_sunshine}点阳光')
            if self.sunshine_ls:
                self.sunshine_ls.pop().destroy()

    def flower_get_sunshine(self, sun, obj):
        if self.mode != self.PAUSE:
            self.sunshine += obj.bullet_attack
            self.sunshine_text.set(self.sunshine)
            self.current_config.get_sunshine_sound.play()
            self.action_text.set(f'成功拿到了{obj.bullet_attack}点阳光')
            sun.destroy()

    def set_zombies(self, current_zombies):
        current_zombies.attack_sound = [
            pygame.mixer.Sound(j) for j in current_zombies.attack_sound
        ]
        self.current_config.whole_sounds.extend(current_zombies.attack_sound)
        current_zombies.dead_sound = [
            pygame.mixer.Sound(j)
            if type(j) != list else [pygame.mixer.Sound(k) for k in j]
            for j in current_zombies.dead_sound
        ]
        self.current_config.whole_sounds.extend(current_zombies.dead_sound)
        current_zombies.hit_sound = [
            pygame.mixer.Sound(j) for j in current_zombies.hit_sound
        ]
        self.current_config.whole_sounds.extend(current_zombies.hit_sound)
        if current_zombies.hit_sound_ls:
            for k in range(len(current_zombies.hit_sound_ls)):
                current = current_zombies.hit_sound_ls[k][1]
                current_zombies.hit_sound_ls[k][1] = pygame.mixer.Sound(
                    current) if type(current) != list else [
                        pygame.mixer.Sound(y) for y in current
                    ]
            self.current_config.whole_sounds.extend(
                [i[1] for i in current_zombies.hit_sound_ls])
        if current_zombies.other_sound:
            current_zombies.other_sound = [
                pygame.mixer.Sound(k) for k in current_zombies.other_sound
            ]
            self.current_config.whole_sounds.extend(
                current_zombies.other_sound)
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
        self.reset_whole_sounds()

    def lawnmower_move(self, obj):
        if obj.columns == 0:
            self.current_config.lawnmower_sound.play()
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
        if all(x <= 0 for x in self.brains):
            self.action_text.set('你赢了')
            self.after(3000, self.win)
            return
        if self.mode == self.PAUSE:
            if keyboard.is_pressed('p'):
                self.mode = self.NULL
                self.action_text.set('游戏继续')
                pygame.mixer.music.unpause()
                repause_current_time = time.time()
                self.paused_time = repause_current_time - self.paused_start
                self.sunshine_time += self.paused_time
                self.paused_start = None
                for i in range(self.current_config.map_size[0]):
                    for j in range(self.current_config.map_size[1]):
                        block_here = self.blocks[i][j]
                        if block_here.plants != None:
                            block_here.plants.time += self.paused_time
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
                for g in self.blocks:
                    for h in g:
                        h.time = repause_current_time
        else:
            nrow, ncol = self.current_config.map_size
            self.current_time = time.time()
            for i in range(nrow):
                j = 0
                while j < ncol:
                    current = self.blocks[i][j]
                    if current.plants is not None:
                        if current.plants.hp <= 0:
                            if current.plants.dead_normal:
                                self.current_config.plant_bite_sound.play()
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
                                    Image.Resampling.LANCZOS)
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

        if self.mode != self.PAUSE:
            current_time = self.current_time
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
                                    (self.lawn_width, self.lawn_height),
                                    Image.Resampling.LANCZOS)
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
        self.current_config.lose_sound.play()
        self.after(7000, quit)

    def win(self):
        self.mode = self.PAUSE
        self.after(7000, quit)


root = Root()


def quit():
    pygame.mixer.quit()
    root.destroy()


root.protocol('WM_DELETE_WINDOW', quit)
root.mainloop()
