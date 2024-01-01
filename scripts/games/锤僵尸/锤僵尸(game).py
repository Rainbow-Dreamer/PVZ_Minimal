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


class Root(Tk):

    def __init__(self):
        super(Root, self).__init__()
        self.protocol('WM_DELETE_WINDOW', quit)
        pygame.mixer.init()
        self.init_main_window()
        self.after(100, self.init_stage)

    def init_main_window(self):
        os.chdir('锤僵尸')
        self.json_config_path = "game_config.json"
        self.current_config = json_module(self.json_config_path)
        os.chdir('../../../resources')
        self.wm_iconbitmap(self.current_config.icon_name)
        self.title('锤僵尸')
        self.minsize(*self.current_config.screen_size)
        self.back_button = ttk.Button(self, text='返回', command=go_back)
        self.back_button.place(x=self.current_config.screen_size[0] - 100, y=0)
        self.make_label = ttk.Label
        self.make_button = ttk.Button
        self.NULL, self.PLACE, self.REMOVE, self.PAUSE = self.current_config.NULL, self.current_config.PLACE, self.current_config.REMOVE, self.current_config.PAUSE
        self.lawn_photo = Image.open(self.current_config.lawn_photo)

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

        self.choose = ttk.LabelFrame(self)
        self.maps = ttk.LabelFrame(self)
        self.init_sunshine()
        self.choose.grid(row=0, column=0, sticky='W')
        self.lawnmowers = [0 for j in range(self.current_config.map_size[0])]
        self.lawnmower_img = Image.open(self.current_config.lawnmower_img)
        self.lawnmower_img = self.lawnmower_img.resize(
            (self.lawn_width, self.lawn_height), Image.Resampling.LANCZOS)
        self.lawnmower_img = ImageTk.PhotoImage(self.lawnmower_img)
        self.no_lawnmower_img = Image.open(
            self.current_config.no_lawnmower_img)
        self.no_lawnmower_img = self.no_lawnmower_img.resize(
            (self.lawn_width, self.lawn_height), Image.Resampling.LANCZOS)
        self.no_lawnmower_img = ImageTk.PhotoImage(self.no_lawnmower_img)
        if self.current_config.lawnmower_rows:
            self.mower_part = ttk.LabelFrame(self)
            self.mower_part.place(x=0, y=100)
            for k in self.current_config.lawnmower_rows:
                current_mower = lawnmower(k, 0,
                                          self.current_config.lawnmower_mode,
                                          self.current_config.lawnmower_speed,
                                          self.current_config.lawnmower_atack)
                current_mower.show = ttk.Button(
                    self.mower_part,
                    image=self.lawnmower_img,
                    command=lambda: self.action_text.set('我是一辆小推车'))
                current_mower.show.grid(row=k, column=0, sticky='W')
                self.lawnmowers[k] = current_mower

        self.init_map(*self.current_config.map_size)
        self.maps.place(x=65, y=100)

        self.choosed_plant = None
        self.sunshine_ls = []
        self.map_rows, self.map_columns = self.current_config.map_size

        self.bind("<Button-3>", lambda e: self.action_text.set(''))
        self.zombie_explode_img = Image.open(
            self.current_config.zombie_explode)
        self.zombie_explode_img = self.zombie_explode_img.resize(
            (self.lawn_width, self.lawn_height), Image.Resampling.LANCZOS)
        self.zombie_explode_img = ImageTk.PhotoImage(self.zombie_explode_img)
        self.normal_zombies_num = 0
        self.big_waves_zombies_num = 0
        self.normal_or_wave = 0

    def init_stage(self):
        current_choosed_stage_file = '../scripts/games/锤僵尸/锤僵尸简单难度.json'
        self.stage_file_contents = json_module(current_choosed_stage_file)
        for each in self.stage_file_contents.apply_scripts:
            with open(each, encoding='utf-8') as f:
                exec(f.read(), globals())
        self.current_stage = Stage(self.stage_file_contents.stages)
        self.whole_zombies = self.current_stage.get(0)
        self.killed_zombies = 0
        self.zombie_time = self.game_start_time + self.stage_file_contents.start_time
        self.killed_zombies_text = StringVar()
        self.killed_zombies_text.set(f'杀死僵尸数: {self.killed_zombies}')
        self.killed_zombies_show = ttk.Label(
            textvariable=self.killed_zombies_text)
        self.killed_zombies_show.place(
            x=self.current_config.action_text_place_x + 200,
            y=self.action_text_place_y,
            anchor='center')
        self.flag_img = Image.open(self.current_config.flag_img)
        self.flag_img = self.flag_img.resize(
            (self.lawn_width // 2, self.lawn_height // 2),
            Image.Resampling.LANCZOS)
        self.flag_img = ImageTk.PhotoImage(self.flag_img)
        self.damaged_flag_img = Image.open(
            self.current_config.damaged_flag_img)
        self.damaged_flag_img = self.damaged_flag_img.resize(
            (self.lawn_width // 2, self.lawn_height // 2),
            Image.Resampling.LANCZOS)
        self.damaged_flag_img = ImageTk.PhotoImage(self.damaged_flag_img)
        self.head_img = Image.open(self.current_config.zombie_head_img)
        self.head_img = self.head_img.resize(
            (self.lawn_width // 2, self.lawn_height // 2),
            Image.Resampling.LANCZOS)
        self.head_img = ImageTk.PhotoImage(self.head_img)
        self.zombie_bar = ttk.LabelFrame(self)
        self.zombie_bar_normal_labels = []
        self.zombie_bar_wave_labels = []
        unit_width = int(50 / (self.current_stage.num_of_waves +
                               (self.current_stage.num_of_waves + 1) * 5))
        long_width = unit_width * 5
        short_width = unit_width
        counter = 6 * self.current_stage.num_of_waves + 4
        for k in range(self.current_stage.num_of_waves * 2 + 1):
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
        self.zombie_bar.place(x=self.current_config.action_text_place_x,
                              y=self.action_text_place_y + 50,
                              anchor='center')
        self.current_ind = -1
        self.current_zombies_num = len(self.whole_zombies)
        self.current_killed_zombies = 0
        self.after(int(self.stage_file_contents.start_time * 1000),
                   self.current_config.zombies_coming_sound.play)
        self.after(int(self.stage_file_contents.start_time * 1000),
                   self.check_zombies)

    def get_plant(self, plant_obj, rows=None, columns=None):
        result = deepcopy(plant_obj)
        if result.bullet_sound:
            result.bullet_sound = [
                pygame.mixer.Sound(j)
                if type(j) != list else [pygame.mixer.Sound(k) for k in j]
                for j in result.bullet_sound
            ]
            self.current_config.whole_sounds.extend(result.bullet_sound)
        if result.bullet_sound and result.sound_volume:
            for j in range(len(result.bullet_sound)):
                result.bullet_sound[j].set_volume(result.sound_volume[j])
        result.rows = rows
        result.columns = columns
        return result

    def get_zombies(self, zombies_obj, rows, columns, appear_time):
        result = deepcopy(zombies_obj)
        result.rows = rows
        result.columns = columns
        result.appear_time = appear_time
        return result

    def init_whole_plants_name(self):
        whole_plants_name = os.listdir('scripts/plant_scripts')
        except_ls = ['__pycache__', '__init__.py', 'plant.py', 'bullets.py']
        for each in except_ls:
            if each in whole_plants_name:
                whole_plants_name.remove(each)
        whole_plants_name = [x[:-3] for x in whole_plants_name]
        self.current_config.whole_plants = [(x, f"{x}.png")
                                            for x in whole_plants_name]
        return whole_plants_name, self.current_config.whole_plants

    def pause(self):
        if self.mode != self.PAUSE:
            self.mode = self.PAUSE
            self.action_text.set("游戏暂停,按P继续")
            pygame.mixer.music.pause()
            self.current_config.pause_sound.play()
            self.paused_start = time.time()

    def hammer_attack(self, each):
        each.hp -= 22
        if each.hp > 0:
            random.choice(each.hit_sound).play()
        else:
            self.current_config.hammer_sound.play()
            each.button.destroy()
            each.status = 0
            self.killed_zombies += 1
            self.current_killed_zombies += 1
            self.killed_zombies_text.set(f'杀死僵尸数: {self.killed_zombies}')

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

    def init_map(self, rows, columns):
        lawn_photo = self.lawn_photo
        for j in range(rows):
            block_row = []
            for k in range(columns):
                current_block = ttk.Button(
                    self.maps,
                    image=lawn_photo,
                    command=self.current_config.swing_sound.play)
                current_block.plants = None
                current_block.image = lawn_photo
                current_block.grid(row=j, column=k)
                block_row.append(current_block)
            self.blocks.append(block_row)
        self.lawn_photo = lawn_photo

    def appear_sunshine(self):
        if self.mode != self.PAUSE:
            sunshine_appear = ttk.Button(self.choose,
                                         image=self.fall_sunshine_img,
                                         command=self.get_sunshine)
            sunshine_appear.image = self.fall_sunshine_img
            sunshine_appear.grid(row=0, column=self.plants_num + 2)
            self.sunshine_ls.append(sunshine_appear)

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
        current_zombies.dead_sound = [
            pygame.mixer.Sound(j)
            if type(j) != list else [pygame.mixer.Sound(k) for k in j]
            for j in current_zombies.dead_sound
        ]
        current_zombies.hit_sound = [
            pygame.mixer.Sound(j) for j in current_zombies.hit_sound
        ]
        if current_zombies.hit_sound_ls:
            for k in range(len(current_zombies.hit_sound_ls)):
                current = current_zombies.hit_sound_ls[k][1]
                current_zombies.hit_sound_ls[k][1] = pygame.mixer.Sound(
                    current) if type(current) != list else [
                        pygame.mixer.Sound(y) for y in current
                    ]
        if current_zombies.other_sound:
            current_zombies.other_sound = [
                pygame.mixer.Sound(k) for k in current_zombies.other_sound
            ]
        zombie_img = Image.open(current_zombies.img)
        zombie_img = zombie_img.resize((self.lawn_width, self.lawn_height),
                                       Image.Resampling.LANCZOS)
        zombie_img = ImageTk.PhotoImage(zombie_img)
        current_zombies_button = ttk.Button(
            self.maps,
            image=zombie_img,
            command=lambda: self.hammer_attack(current_zombies))
        current_zombies_button.image = zombie_img
        current_zombies.button = current_zombies_button
        current_zombies.next_to_plants = False
        current_zombies.eating = False
        current_zombies.time = self.current_time

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

    def check_zombies(self):

        if self.mode != self.PAUSE:
            self.current_time = time.time()
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
                self.zombie_time = self.current_time
                if self.normal_or_wave == 0:
                    self.normal_or_wave = 1
                    if self.normal_zombies_num == self.current_stage.num_of_waves:
                        self.action_text.set('你赢了！')
                        self.mode = self.PAUSE
                        self.win()
                        return
                    self.normal_zombies_num += 1
                    self.whole_zombies = self.current_stage.get(
                        self.big_waves_zombies_num, 1)
                    self.current_zombies_num = len(self.whole_zombies)
                    self.after(2000, self.current_config.huge_wave_sound.play)
                    self.after(2000,
                               lambda: self.action_text.set('一大波僵尸要来袭了！'))
                    self.after(5000,
                               self.current_config.zombies_coming_sound.play)
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
                    self.whole_zombies = self.current_stage.get(
                        self.normal_zombies_num)
                    self.current_zombies_num = len(self.whole_zombies)

            passed_time = self.current_time - self.zombie_time
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
        self.current_config.lose_sound.play()
        self.after(7000, quit)

    def win(self):
        self.after(7000, quit)


if __name__ == '__main__':
    root = Root()
    root.mainloop()
