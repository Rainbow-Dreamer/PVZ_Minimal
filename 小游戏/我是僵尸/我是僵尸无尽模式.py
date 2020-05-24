os.chdir('我是僵尸')
with open('config.py', encoding='utf-8') as f:
    datas = f.read()
    exec(datas, globals())


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.wm_iconbitmap(icon_name)
        self.title('我是僵尸无尽模式')
        self.minsize(*screen_size)
        self.make_label = ttk.Label
        self.make_button = ttk.Button
        self.get_zombies = get_zombies
        self.NULL, self.PLACE, self.REMOVE, self.PAUSE = 0, 1, 2, 3
        self.whole_zombies = []
        self.lawn_photo = Image.open(lawn_img)
        self.plants_num = plants_num
        self.whole_plants = whole_plants
        self.get_plant = get_plant
        self.paused_time = 0
        lawn_size = 250 // map_size[0]
        self.lawn_photo = self.lawn_photo.resize((lawn_size, lawn_size),
                                                 Image.ANTIALIAS)
        self.background_img = self.lawn_photo.copy()
        self.lawn_photo = ImageTk.PhotoImage(self.lawn_photo)
        self.lawn_width, self.lawn_height = self.lawn_photo.width(
        ), self.lawn_photo.height()
        self.action_text = StringVar()
        self.action_text_show = ttk.Label(textvariable=self.action_text)
        self.action_text_place_y = map_size[0] * (self.lawn_height + 10) + 150
        self.action_text_show.place(x=action_text_place_x,
                                    y=self.action_text_place_y,
                                    anchor='center')

        global choosed_zombies
        bg_music = pygame.mixer.music.load(background_music)
        pygame.mixer.music.set_volume(background_volume)
        pygame.mixer.music.play(loops=-1)
        game_start_time = time.time()
        self.game_start_time = game_start_time
        self.mode = NULL
        self.blocks = []
        self.moving_bullets = []
        self.sunshine_time = game_start_time
        if modified_file:
            with open(modified_file, encoding='utf-8') as f:
                exec(f.read())

        self.plants_generate = deepcopy(choosed_zombies)

        self.choose = ttk.LabelFrame(self)
        self.maps = ttk.LabelFrame(self)
        self.init_sunshine()
        self.init_zombies()
        self.plant_bite_sound = plant_bite_sound
        self.choose.grid(row=0, column=0, sticky='W')
        self.brain_img = brain_img
        self.brains = [5 for j in range(map_size[0])]
        self.brains_show = []
        self.brain_img = Image.open(brain_img)
        self.brain_img = self.brain_img.resize(
            (self.lawn_width, self.lawn_height), Image.ANTIALIAS)
        self.brain_img = ImageTk.PhotoImage(self.brain_img)
        self.no_brain_img = Image.open(no_lawnmower_img)
        self.no_brain_img = self.no_brain_img.resize(
            (self.lawn_width, self.lawn_height), Image.ANTIALIAS)
        self.no_brain_img = ImageTk.PhotoImage(self.no_brain_img)
        self.brain_part = ttk.LabelFrame(self)
        self.brain_part.place(x=0, y=100)
        for k in range(map_size[0]):
            current_brain = ttk.Button(
                self.brain_part,
                image=self.brain_img,
                command=lambda: self.action_text.set('我是一个脑子'))
            current_brain.grid(row=k, column=0, sticky='W')
            self.brains_show.append(current_brain)

        self.init_map(*map_size)
        self.maps.place(x=65, y=100)

        self.choosed_zombies = None
        self.sunshine_ls = []
        self.map_rows, self.map_columns = map_size
        self.init_plant_ls()
        self.bind("<Button-3>", lambda e: self.reset())
        self.bind("<space>", lambda e: self.pause())
        self.zombie_explode_img = Image.open(zombie_explode)
        self.zombie_explode_img = self.zombie_explode_img.resize(
            (self.lawn_width, self.lawn_height), Image.ANTIALIAS)
        self.zombie_explode_img = ImageTk.PhotoImage(self.zombie_explode_img)

        self.killed_zombies = 0
        self.killed_zombies_text = StringVar()
        self.current_killed_zombies = 0
        self.killed_zombies_text.set(f'杀死僵尸数: {self.killed_zombies}')
        self.killed_zombies_show = ttk.Label(
            textvariable=self.killed_zombies_text)
        self.killed_zombies_show.place(x=action_text_place_x + 200,
                                       y=self.action_text_place_y,
                                       anchor='center')
        self.win_stages = 0
        self.win_stages_text = StringVar()
        self.win_stages_text.set(f'通关数：{self.win_stages}')
        self.win_stages_label = ttk.Label(self,
                                          textvariable=self.win_stages_text)
        self.win_stages_label.place(x=action_text_place_x + 300,
                                    y=self.action_text_place_y,
                                    anchor='center')
        self.zombie_time = time.time()
        self.check_plants()
        self.check_zombies()

    def next_stage(self):
        self.brains = [5 for j in range(map_size[0])]
        self.brains_show = []
        for k in range(map_size[0]):
            current_brain = ttk.Button(
                self.brain_part,
                image=self.brain_img,
                command=lambda: self.action_text.set('我是一个脑子'))
            current_brain.grid(row=k, column=0, sticky='W')
            self.brains_show.append(current_brain)
        self.choosed_zombies = None
        self.whole_zombies = []
        self.init_plant_ls()
        self.zombie_time = time.time()
        self.check_plants()

    def init_plant_ls(self):
        self.bullets_ls = []
        current_time = time.time()
        for i in range(map_size[0]):
            for j in range(plant_line):
                current_plant = plants_list[i][j]
                current = self.blocks[i][j]
                current.plants = get_plant(current_plant, i, j)
                current.plants.counter = current_time
                current.plants.time = current_time
                self.make_img(current.plants)
                if current.plants.bullet_img and current.plants.is_bullet and current.plants.bullet_img_name not in self.bullets_ls:
                    self.bullets_ls.append(current.plants.bullet_img_name)
                if current.plants.use_bullet_img_first:
                    current.configure(image=current.plants.bullet_img)
                else:
                    current.configure(image=current.plants.img)

    def make_img(self, each, resize_num=1):
        current_img = Image.open(each.img)
        if each.img_transparent:
            ratio = self.lawn_height / current_img.height
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
                    each.bullet_img = ImageTk.PhotoImage(
                        Image.open(each.bullet_img).resize(
                            (self.lawn_width // 3, self.lawn_height // 3),
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
                    current_other_img = current_other_img.resize(
                        (int(self.lawn_width / resize_num),
                         int(self.lawn_height / resize_num)), Image.ANTIALIAS)
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

    def reset(self):
        if self.mode == PLACE or self.mode == REMOVE:
            random.choice(reset_sound).play()
        self.change_mode(NULL)

    def init_sunshine(self):
        sun_photo = ImageTk.PhotoImage(
            Image.open(sunshine_img).resize(
                (self.lawn_width, self.lawn_height), Image.ANTIALIAS))
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
            Image.open(fall_sunshine_img).resize(
                (self.lawn_width, self.lawn_height), Image.ANTIALIAS))
        self.flower_sunshine_img = ImageTk.PhotoImage(
            Image.open(fall_sunshine_img).resize(
                (self.lawn_width, self.lawn_height), Image.ANTIALIAS))

    def init_zombies(self):
        self.zombies_num = len(choosed_zombies)
        for i in range(self.zombies_num):
            zombies_info = choosed_zombies[i]
            self.make_img(zombies_info)
            current_text = StringVar()
            current_text.set(f'${zombies_info.price}')
            current_button = ttk.Button(
                self.choose,
                image=zombies_info.img,
                textvariable=current_text,
                compound=TOP,
                command=lambda i=i: self.change_mode(PLACE, i))
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

    def change_mode(self, num, zombies=None):
        if self.mode != PAUSE:
            self.mode = num
            if num == PLACE:
                current_plant = choosed_zombies[zombies]
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
                    self.choosed_zombies = zombies

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
                if k < plant_line - 1:
                    sunshine_not_enough.play()
                    self.action_text.set('请种植在第5列或者其右边')
                    self.mode = NULL
                else:
                    current = self.blocks[j][k]
                    current_time = self.current_time
                    choose_zombies = self.plants_generate[self.choosed_zombies]
                    current_zombies = get_zombies(choose_zombies, j, k, 0)
                    self.make_img(current_zombies)
                    self.set_zombies(current_zombies)
                    if current.plants:
                        current_zombies.button.grid(row=j, column=k)
                    current_zombies.alive()
                    if current_zombies.start_func:
                        current_zombies.runs(self, num=0)
                    current_zombies.time = current_time
                    current_zombies_name = current_zombies.name
                    set_plants_sound.play()
                    self.action_text.set(
                        f'你成功放置了{current_zombies_name}在第{j+1}行，第{k+1}列')
                    self.sunshine -= current_zombies.price
                    self.sunshine_text.set(self.sunshine)
                    self.whole_zombies.append(current_zombies)
                    self.choosed_zombies = None
                    self.mode = NULL

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
                if plants_on_block:
                    self.action_text.set(
                        f'这上面有个{plants_on_block.name}, 当前生命值{plants_on_block.hp}'
                    )

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
        current_zombies_button = ttk.Button(
            self.maps,
            image=current_zombies.img,
            command=lambda current_zombies=current_zombies: self.block_action(
                current_zombies, mode=1))
        current_zombies_button.image = current_zombies.img
        current_zombies.button = current_zombies_button
        current_zombies.next_to_plants = False

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
        if all(x <= 0 for x in self.brains):
            self.action_text.set('你赢了')
            self.after(3000, self.win)
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
                for k in self.whole_zombies:
                    if k.status == 0 and k.hp > 0:
                        k.appear_time += self.paused_time
                self.zombies_move_call()
                for each_bullet in self.moving_bullets:
                    if each_bullet.func:
                        each_bullet.func(self, each_bullet)
                self.moving_bullets = []
                for g in self.blocks:
                    for h in g:
                        h.time = repause_current_time
        else:
            nrow, ncol = map_size
            self.current_time = time.time()
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
        self.win_stages += 1
        self.win_stages_text.set(f'通关数：{self.win_stages}')
        exec(stage_file_contents)
        self.next_stage()


root = Root()


def quit():
    pygame.mixer.quit()
    root.destroy()


root.protocol('WM_DELETE_WINDOW', quit)
root.mainloop()
