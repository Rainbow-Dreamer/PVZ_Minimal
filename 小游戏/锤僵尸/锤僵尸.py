os.chdir('锤僵尸')
with open('config.py', encoding='utf-8') as f:
    exec(f.read())


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.wm_iconbitmap(icon_name)
        self.title('锤僵尸')
        self.minsize(*screen_size)
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
        self.action_text = StringVar()
        self.action_text_show = ttk.Label(textvariable=self.action_text)
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
        self.init_sunshine()
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

        self.bind("<Button-3>", lambda e: self.action_text.set(''))
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
        self.after(int(start_time * 1000), zombies_coming_sound.play)
        self.after(int(start_time * 1000), self.check_zombies)

    def pause(self):
        if self.mode != PAUSE:
            self.mode = PAUSE
            self.action_text.set("游戏暂停,按P继续")
            pygame.mixer.music.pause()
            pause_sound.play()
            self.paused_start = time.time()

    def hammer_attack(self, each):
        each.hp -= 22
        if each.hp > 0:
            random.choice(each.hit_sound).play()
        else:
            hammer_sound.play()
            each.button.destroy()
            each.status = 0
            self.killed_zombies += 1
            self.current_killed_zombies += 1
            self.killed_zombies_text.set(f'杀死僵尸数: {self.killed_zombies}')

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

    def init_map(self, rows, columns):
        lawn_photo = self.lawn_photo
        for j in range(rows):
            block_row = []
            for k in range(columns):
                current_block = ttk.Button(self.maps,
                                           image=lawn_photo,
                                           command=swing_sound.play)
                current_block.plants = None
                current_block.image = lawn_photo
                current_block.grid(row=j, column=k)
                block_row.append(current_block)
            self.blocks.append(block_row)
        self.lawn_photo = lawn_photo

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
                                       Image.ANTIALIAS)
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

    def check_zombies(self):

        if self.mode != PAUSE:
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
