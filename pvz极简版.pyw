from tkinter import *
from tkinter import ttk
from pvz_config import *
from PIL import Image, ImageTk
import datetime, time, random, keyboard


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.wm_iconbitmap(icon_name)
        self.title(title_name)
        self.minsize(*screen_size)
        self.action_text = StringVar()
        self.action_text_show = ttk.Label(textvariable=self.action_text)
        self.action_text_show.place(x=action_text_place_x,
                                    y=action_text_place_y,
                                    anchor='center')
        self.lawn_photo = PhotoImage(file=lawn_img).subsample(2, 2)
        self.lawn_width, self.lawn_height = self.lawn_photo.width(
        ), self.lawn_photo.height()
        for each in whole_plants:
            current_img = Image.open(each.img)
            current_img = current_img.resize(
                (self.lawn_width, self.lawn_height), Image.ANTIALIAS)
            each.img = ImageTk.PhotoImage(current_img)
            if each.bullet_img != None:
                if each.name in ['土豆雷', '火爆辣椒']:
                    current_img = Image.open(each.bullet_img)
                    current_img = current_img.resize(
                        (self.lawn_width, self.lawn_height), Image.ANTIALIAS)
                    each.bullet_img = ImageTk.PhotoImage(current_img)
                else:
                    each.bullet_img = PhotoImage(
                        file=each.bullet_img).subsample(5, 5)
        pygame.mixer.music.set_volume(choose_seed_volume)
        pygame.mixer.music.play(loops=-1)
        self.plants_already_choosed = ttk.LabelFrame(self, height=200)
        self.plants_already_choosed.grid(sticky='w')
        self.choose_plants_screen = ttk.LabelFrame(self)
        self.choose_buttons = []
        self.append_plants_buttons = []
        for i in range(len(whole_plants)):
            current_button = ttk.Button(
                self.choose_plants_screen,
                image=whole_plants[i].img,
                command=lambda i=i: self.append_plants(i))
            current_button.grid(row=i // 10, column=i % 10)
            self.choose_buttons.append(current_button)
        self.choose_plants_screen.place(x=0, y=200)
        self.start_game = ttk.Button(text='开始游戏', command=self.start_init)
        self.start_game.place(x=0, y=300)

    def append_plants(self, i):
        the_append_plant = whole_plants[i]
        self.action_text.set(f'你选择了{the_append_plant.name}')
        choose_plant_sound.play()
        choosed_plants.append(the_append_plant)
        current_index = len(choosed_plants) - 1
        append_button = ttk.Button(
            self.plants_already_choosed,
            image=the_append_plant.img,
            command=lambda x=the_append_plant, y=i: self.remove_plants(x, y))
        append_button.grid(row=0, column=current_index)
        self.append_plants_buttons.append(append_button)
        self.choose_buttons[i].grid_forget()

    def remove_plants(self, x, y):
        self.action_text.set(f'你取消选择了{x.name}')
        ind = choosed_plants.index(x)
        self.append_plants_buttons[ind].destroy()
        del self.append_plants_buttons[ind]
        del choosed_plants[ind]
        self.choose_buttons[y].grid(row=y // 10, column=y % 10)

    def start_init(self):
        pygame.mixer.music.stop()
        bg_music = pygame.mixer.music.load(background_music)
        pygame.mixer.music.set_volume(background_volume)
        pygame.mixer.music.play(loops=-1)
        self.plants_already_choosed.destroy()
        self.choose_plants_screen.destroy()
        self.start_game.destroy()
        game_start_time = time.time()
        self.game_start_time = game_start_time
        self.mode = NULL
        self.blocks = []
        self.moving_bullets = []
        self.sunshine_time = game_start_time

        self.bullets_dict = {}
        for each in choosed_plants:
            if each.bullet_img != None and each.name not in ['土豆雷', '火爆辣椒']:
                self.bullets_dict[each.bullet_img] = each.bullet_attack
        self.choose = ttk.LabelFrame(self)
        self.maps = ttk.LabelFrame(self)
        self.init_sunshine()
        self.init_plants()
        self.init_shovel()
        self.init_map(*map_size)
        self.choose.grid(sticky='w')
        self.maps.grid(sticky='w')

        self.choosed_plant = None
        self.sunshine_ls = []
        self.map_rows, self.map_columns = map_size

        self.bind("<Button-3>", lambda e: self.reset())
        self.bind("<space>", lambda e: self.pause())
        self.zombie_explode_img = Image.open(zombie_explode)
        self.zombie_explode_img = self.zombie_explode_img.resize(
            (self.lawn_width, self.lawn_height), Image.ANTIALIAS)
        self.zombie_explode_img = ImageTk.PhotoImage(self.zombie_explode_img)
        self.check_plants()
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
                                       y=action_text_place_y,
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
        counter = 6 * current_stage.num_of_waves + 4
        for k in range(current_stage.num_of_waves * 2 + 1):
            if k % 2 == 0:
                normal_labels = []
                for j in range(5):
                    current_bar = ttk.Label(self.zombie_bar, width=2)
                    current_bar.grid(row=0, column=counter - j)
                    normal_labels.append(current_bar)
                self.zombie_bar_normal_labels.append(normal_labels)
                counter -= 5
            else:
                current_bar = ttk.Label(self.zombie_bar,
                                        image=self.flag_img,
                                        width=10)
                current_bar.grid(row=0, column=counter)
                self.zombie_bar_wave_labels.append(current_bar)
                counter -= 1
        self.zombie_bar.place(x=action_text_place_x,
                              y=action_text_place_y + 50,
                              anchor='center')
        self.current_ind = -1
        self.current_zombies_num = len(self.whole_zombies)
        self.current_killed_zombies = 0
        self.after(int(start_time * 1000), zombies_coming_sound.play)
        self.after(int(start_time * 1000), self.check_zombies)

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

    def init_sunshine(self):
        sun_photo = PhotoImage(file=sunshine_img).subsample(2, 2)
        self.sunshine = init_sunshine
        self.sunshine_text = StringVar()
        self.sunshine_text.set(self.sunshine)
        self.sunshine_show = ttk.Label(self.choose,
                                       textvariable=self.sunshine_text,
                                       image=sun_photo,
                                       compound=TOP)
        self.sunshine_show.image = sun_photo
        self.sunshine_show.grid(row=0, column=0)
        self.fall_sunshine_img = PhotoImage(file=fall_sunshine_img).subsample(
            3, 3)
        self.flower_sunshine_img = PhotoImage(
            file=fall_sunshine_img).subsample(4, 4)

    def init_plants(self):
        self.plants_num = len(choosed_plants)
        for i in range(self.plants_num):
            plants_info = choosed_plants[i]
            current_text = StringVar()
            current_text.set(f'${plants_info.price} 冷却中')
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
            plants_info.counter = time.time()
            plants_info.enable = 0

    def init_shovel(self):
        shovel_photo = PhotoImage(file=shovel_img).subsample(2, 2)
        self.shovel_button = ttk.Button(
            self.choose,
            image=shovel_photo,
            command=lambda: self.change_mode(REMOVE))
        self.shovel_button.image = shovel_photo
        self.shovel_button.grid(row=0, column=self.plants_num + 1)

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
                dim = j.rows, j.columns + 1 + j.adjust_col
                j, k = dim
            if self.mode == PLACE:
                current = self.blocks[j][k]
                current_time = time.time()
                choose_plant = choosed_plants[self.choosed_plant]
                if current.plants is None:
                    if choose_plant.name == '土豆雷':
                        current.configure(image=choose_plant.bullet_img)
                        current.img = choose_plant.img
                    else:
                        current.configure(image=choose_plant.img)
                        if choose_plant.bullet_img != None:
                            current.bullet_image = choose_plant.bullet_img
                    current.plants = get_plant(choose_plant.name, j, k)
                    current.time = current_time
                    current_plant_name = choose_plant.name
                    if current_plant_name == '向日葵':
                        current.sunshine_ls = []
                    set_plants_sound.play()
                    self.action_text.set(
                        f'你成功放置了{current_plant_name}在第{j+1}行，第{k+1}列')
                    choose_plant.button.textvariable.set(
                        f'${choose_plant.price} 冷却中')
                    choose_plant.counter = current_time
                    choose_plant.enable = 0
                    self.sunshine -= choose_plant.price
                    self.sunshine_text.set(self.sunshine)
                    self.choosed_plant = None
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
                    block.plants.status = 0
                    block.plants = None
                else:
                    self.action_text.set('这里并没有植物，请问您要铲什么？')
                self.mode = NULL
            else:
                plants_on_block = self.blocks[j][k].plants
                if plants_on_block is None:
                    self.action_text.set('这是一块空荡荡的草坪')
                else:
                    self.action_text.set(f'这上面有个{plants_on_block.name}')

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
            self.sunshine += 25
            self.sunshine_text.set(self.sunshine)
            get_sunshine_sound.play()
            self.action_text.set('成功拿到了25点阳光')
            if self.sunshine_ls:
                self.sunshine_ls.pop().destroy()

    def flower_get_sunshine(self, i, j):
        if self.mode != PAUSE:
            self.sunshine += 25
            self.sunshine_text.set(self.sunshine)
            get_sunshine_sound.play()
            self.action_text.set('成功拿到了25点阳光')
            block_sunshine = self.blocks[i][j].sunshine_ls
            if block_sunshine:
                block_sunshine.pop().grid_forget()

    def pea_attack(self, i, j):
        pass

    def moving(self, obj, columns_move=0, rows_move=0, stop=False):
        if self.mode != PAUSE:
            if stop:
                obj.grid_forget()
                return
            obj.columns += columns_move
            obj.rows += rows_move
            i, j = obj.rows, obj.columns
            if j < self.map_columns:
                obj.grid(row=i, column=j)
                current_place = self.blocks[i][j]
                if obj.attributes == 0:
                    if current_place.plants is not None:
                        if current_place.plants.name == '火炬树桩':
                            obj.attack *= 2
                            obj.configure(image=current_place.bullet_image)
                            obj.attributes = 1
                zombie_row = [
                    x for x in self.whole_zombies
                    if x.rows == i and x.status == 1
                ]
                if any(x.columns + 1 + x.adjust_col == j for x in zombie_row):
                    zombie_row.sort(key=lambda y: y.columns + 1 + y.adjust_col)
                    hitted_zombies = zombie_row[0]
                    hitted_zombies.hp -= obj.attack
                    if type(hitted_zombies.hit_sound) == list:
                        random.choice(hitted_zombies.hit_sound).play()
                    else:
                        hitted_zombies.hit_sound.play()
                    obj.grid_forget()
                    return
                else:
                    self.after(obj.bullet_speed, lambda: self.moving(obj, 1))
            else:
                obj.grid_forget()
                return
        else:
            self.moving_bullets.append(obj)
            return

    def set_zombies(self, current_zombies):
        zombie_img = Image.open(current_zombies.img)
        zombie_img = zombie_img.resize((self.lawn_width, self.lawn_height),
                                       Image.ANTIALIAS)
        zombie_img = ImageTk.PhotoImage(zombie_img)
        current_zombies_button = ttk.Button(
            self.maps,
            image=zombie_img,
            command=lambda current_zombies=current_zombies: self.block_action(
                current_zombies, mode=1))
        current_zombies_button.image = zombie_img
        current_zombies.button = current_zombies_button
        current_zombies.next_to_plants = False

    def zombie_move(self,
                    obj,
                    columns_move,
                    rows_move=0,
                    stop=False,
                    reset=False):
        if reset:
            obj.adjust_col = -1
        if stop or self.mode == PAUSE:
            return
        if obj.status == 0:
            return
        check_if_plants = self.blocks[obj.rows][obj.columns].plants
        if check_if_plants is not None:
            obj.next_to_plants = True
            obj.nexted_plants = check_if_plants
            obj.adjust_col = -1
            return
        check_if_plants2 = self.blocks[obj.rows][obj.columns +
                                                 columns_move].plants
        if check_if_plants2 is not None:
            obj.columns += columns_move
            obj.next_to_plants = True
            obj.nexted_plants = check_if_plants2
            obj.adjust_col = 0
            return
        obj.rows += rows_move
        obj.columns += columns_move
        if obj.columns < 0:
            self.lose()
            self.mode = PAUSE
            return
        i, j = obj.rows, obj.columns
        #try:
        obj.button.grid(row=i, column=j)

        current_grid = self.maps.grid_slaves(row=i, column=j)
        if any(x.image in self.bullets_dict for x in current_grid):
            hit_bullets = [
                x for x in current_grid if x.image in self.bullets_dict
            ][0]
            self.moving(hit_bullets, stop=True)
            if type(obj.hit_sound) == list:
                random.choice(obj.hit_sound).play()
            else:
                obj.hit_sound.play()
            obj.hp -= self.bullets_dict[hit_bullets.image]
        self.after(obj.move_speed, lambda: self.zombie_move(obj, -1))
        #except:
        #obj.status = 0
        #obj.button.grid_forget()
        #return

    def zombie_eat_plants(self, plants, zombies):
        if self.mode != PAUSE:
            if plants is None or plants.hp <= 0 or plants.status == 0 or zombies.hp <= 0:
                zombies.next_to_plants = False
                self.after(
                    zombies.move_speed, lambda: self.zombie_move(
                        zombies, zombies.adjust_col, reset=True))
                return
            else:
                if type(zombies.attack_sound) == list:
                    random.choice(zombies.attack_sound).play()
                else:
                    zombies.attack_sound.play()
                plants.hp -= zombies.attack
                self.after(
                    zombies.attack_speed,
                    lambda x=plants, y=zombies: self.zombie_eat_plants(x, y))

    def cherry_explode(self, i, j):
        cherry_block = self.blocks[i][j]
        if cherry_block.plants != None and cherry_block.plants.hp > 0:
            cherry_block.plants.bullet_sound[0].play()
            around = [[i - 1 + x, j - 1 + y] for x in range(3)
                      for y in range(3)]
            around = [
                k for k in around
                if 0 <= k[0] < self.map_rows and 0 <= k[1] < self.map_columns
            ]
            around_zombies = [
                q for q in self.whole_zombies
                if q.status == 1 and [q.rows, q.columns] in around
            ]
            for each in around_zombies:
                each.hp -= 90
                if each.hp <= 0:
                    each.status = 0
                    self.killed_zombies += 1
                    self.current_killed_zombies += 1
                    self.killed_zombies_text.set(
                        f'杀死僵尸数: {self.killed_zombies}')
                    each.button.configure(image=self.zombie_explode_img)
                    self.after(3000, lambda t=each: t.button.grid_forget())
            cherry_block.configure(image=self.lawn_photo)
            cherry_block.plants = None

    def squash_attack(self, i, j):
        squash_block = self.blocks[i][j]
        if squash_block.plants != None and squash_block.plants.hp > 0:
            squash_block.plants.bullet_sound[1].play()
            hit_zombies = [
                x for x in self.whole_zombies
                if x.status == 1 and x.rows == i and abs(x.columns - j) <= 1
            ]
            hit_zombies_middle = [x for x in hit_zombies if x.columns == j]
            if len(hit_zombies_middle) != 0:
                for each in hit_zombies_middle:
                    each.hp -= 90
                    if each.hp <= 0:
                        each.status = 0
                        self.killed_zombies += 1
                        self.current_killed_zombies += 1
                        self.killed_zombies_text.set(
                            f'杀死僵尸数: {self.killed_zombies}')
                        each.button.grid_forget()
            else:
                hit_zombies_right = [
                    x for x in hit_zombies if x.columns - j == 1
                ]
                if len(hit_zombies_right) != 0:
                    for each in hit_zombies_right:
                        each.hp -= 90
                        if each.hp <= 0:
                            each.status = 0
                            self.killed_zombies += 1
                            self.current_killed_zombies += 1
                            self.killed_zombies_text.set(
                                f'杀死僵尸数: {self.killed_zombies}')
                            each.button.grid_forget()
                else:
                    hit_zombies_left = [
                        x for x in hit_zombies if x.columns - j == -1
                    ]
                    if len(hit_zombies_left) != 0:
                        for each in hit_zombies_left:
                            each.hp -= 90
                            if each.hp <= 0:
                                each.status = 0
                                self.killed_zombies += 1
                                self.current_killed_zombies += 1
                                self.killed_zombies_text.set(
                                    f'杀死僵尸数: {self.killed_zombies}')
                                each.button.grid_forget()
            squash_block.configure(image=self.lawn_photo)
            squash_block.plants = None

    def potato_detect(self, i, j):
        potato_check = self.blocks[i][j]
        if potato_check.plants is None or potato_check.plants.hp <= 0:
            return
        attack_zombies = [
            x for x in self.whole_zombies
            if x.status == 1 and x.rows == i and x.columns == j
        ]
        if len(attack_zombies) != 0:
            potato_check.plants.bullet_sound[1].play()
            for each in attack_zombies:
                each.hp -= 90
                if each.hp <= 0:
                    each.status = 0
                    self.killed_zombies += 1
                    self.current_killed_zombies += 1
                    self.killed_zombies_text.set(
                        f'杀死僵尸数: {self.killed_zombies}')
                    each.button.configure(image=self.zombie_explode_img)
                    self.after(3000, lambda t=each: t.button.grid_forget())
            potato_check.configure(image=self.lawn_photo)
            potato_check.plants = None
            return
        self.after(50, lambda: self.potato_detect(i, j))

    def jalapeno_explode(self, i, j):
        jalapeno_blocks = self.blocks[i][j]
        if jalapeno_blocks.plants is not None and jalapeno_blocks.plants.hp > 0:
            jalapeno_blocks.plants.bullet_sound[0].play()
            fire_ls = []
            for k in range(self.map_columns):
                current_button = ttk.Button(
                    self.maps,
                    image=jalapeno_blocks.bullet_image,
                    command=lambda i=i, k=k: self.block_action(i, k))
                current_button.image = jalapeno_blocks.bullet_image
                current_button.grid(row=i, column=k)
                fire_ls.append(current_button)
                self.after(2000, current_button.destroy)

            attack_zombies = [
                x for x in self.whole_zombies if x.status == 1 and x.rows == i
            ]
            for each in attack_zombies:
                each.hp -= 90
                if each.hp <= 0:
                    each.status = 0
                    self.killed_zombies += 1
                    self.current_killed_zombies += 1
                    self.killed_zombies_text.set(
                        f'杀死僵尸数: {self.killed_zombies}')
                    each.button.configure(image=self.zombie_explode_img)
                    fire_ls[each.columns + 1 + each.adjust_col].grid_forget()
                    self.after(3000, lambda t=each: t.button.grid_forget())
            jalapeno_blocks.configure(image=self.lawn_photo)
            jalapeno_blocks.plants = None

    def zombie_dead_normal(self, obj):
        obj.button.grid_forget()
        obj.dead_sound[0].play()
        self.after(2000, lambda: random.choice(obj.dead_sound[1]).play())

    def check_plants(self):
        if self.mode == PAUSE:
            if keyboard.is_pressed('p'):
                self.mode = NULL
                self.action_text.set('游戏继续')
                pygame.mixer.music.unpause()
                repause_current_time = time.time()
                self.paused_time = repause_current_time - self.paused_start
                self.sunshine_time += self.paused_time
                self.paused_start = None
                for k in self.whole_zombies:
                    if k.status == 0 and k.hp > 0:
                        k.appear_time += self.paused_time
                self.zombies_move_call()
                for each_bullet in self.moving_bullets:
                    self.moving(each_bullet)
                self.moving_bullets = []
                for g in self.blocks:
                    for h in g:
                        h.time = repause_current_time
        else:
            nrow, ncol = map_size
            current_time = time.time()
            if current_time - self.sunshine_time >= sunshine_cooling_time:
                self.appear_sunshine()
                self.sunshine_time = current_time
            for each_plant in choosed_plants:
                if current_time - each_plant.counter > each_plant.cooling_time:
                    each_plant.enable = 1
                    each_plant.button.textvariable.set(f'${each_plant.price}')
            for i in range(nrow):
                j = 0
                while j < ncol:
                    current = self.blocks[i][j]
                    if current.plants is not None:
                        if current.plants.hp <= 0:
                            plant_bite_sound.play()
                            self.action_text.set(
                                f'第{i+1}行，第{j+1}列的植物{current.plants.name}被吃掉了')
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
                                current.image = new_hp_img
                                current.plants.hp_img = current.plants.hp_img[
                                    1:]
                        if current.plants.status == 1:
                            current_plant = current.plants.name
                            if current_plant == '向日葵':
                                if current_time - current.time >= current.plants.attack_interval:
                                    current.time = current_time
                                    flower_sunshine = ttk.Button(
                                        self.maps,
                                        image=self.flower_sunshine_img,
                                        command=lambda i=i, j=j: self.
                                        flower_get_sunshine(i, j))
                                    flower_sunshine.image = self.fall_sunshine_img
                                    flower_sunshine.grid(row=i, column=j)
                                    current.sunshine_ls.append(flower_sunshine)
                            elif current_plant == '豌豆射手':
                                if any(x.status == 1 and x.rows == i
                                       for x in self.whole_zombies):
                                    if current_time - current.time >= current.plants.attack_interval:
                                        current.time = current_time
                                        new_pea = ttk.Label(
                                            self.maps,
                                            image=current.bullet_image)
                                        new_pea.image = current.bullet_image
                                        new_pea.bullet_speed = current.plants.bullet_speed
                                        new_pea.attack = current.plants.bullet_attack
                                        new_pea.rows = i
                                        new_pea.columns = j
                                        new_pea.attributes = 0
                                        current.plants.bullet_sound[0].play()
                                        self.moving(new_pea)

                            elif current_plant == '樱桃炸弹':
                                if current_time - current.time >= current.plants.attack_interval:
                                    current.plants.status = 0
                                    self.cherry_explode(i, j)
                            elif current_plant == '窝瓜':
                                if any(x.status == 1 and x.rows == i
                                       and abs(x.columns - j) <= 1
                                       for x in self.whole_zombies):
                                    random.choice(
                                        current.plants.bullet_sound[0]).play()
                                    current.plants.status = 0
                                    self.after(int(
                                        current.plants.attack_interval * 1000),
                                               lambda i=i, j=j: self.
                                               squash_attack(i, j))
                            elif current_plant == '土豆雷':
                                if current_time - current.time >= current.plants.attack_interval:
                                    current.configure(image=current.img)
                                    current.plants.bullet_sound[0].play()
                                    current.plants.status = 0
                                    self.potato_detect(i, j)
                            elif current_plant == '火爆辣椒':
                                if current_time - current.time >= current.plants.attack_interval:
                                    current.plants.status = 0
                                    self.jalapeno_explode(i, j)

                    j += 1

        self.after(1, self.check_plants)

    def check_zombies(self):

        if self.mode != PAUSE:
            current_time = time.time()
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
                        if each.next_to_plants:
                            each.next_to_plants = False
                            self.after(
                                each.attack_speed,
                                lambda plants=each.nexted_plants, zombies=each:
                                self.zombie_eat_plants(plants, zombies))
                else:
                    if each.hp > 0 and passed_time >= each.appear_time:
                        self.set_zombies(each)
                        each.alive()
                        self.zombie_move(each, 0)
        self.after(1, self.check_zombies)

    def zombies_move_call(self):
        for each in self.whole_zombies:
            if each.status == 1 and each.hp > 0:
                if each.next_to_plants:
                    self.after(each.attack_speed,
                               lambda plants=each.nexted_plants, zombies=each:
                               self.zombie_eat_plants(plants, zombies))
                else:
                    self.zombie_move(each, 0)

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
