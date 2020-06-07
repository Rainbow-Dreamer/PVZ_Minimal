# 这是一个很简单的预设关卡

def shooting_move(self, games, columns_move=0, rows_move=0):
    if self.stop or games.mode == games.PAUSE:
        return
    if self.hp <= 0 or self.status == 0:
        return
    self.rows += rows_move
    self.columns += columns_move
    if self.columns < 0:
        lawnmower_here = games.lawnmowers[self.rows]
        if lawnmower_here != 0:
            generate_lawnmower = games.make_button(
                games.maps,
                image=games.lawnmower_img,
                command=lambda: games.action_text.set('我是一辆小推车'))
            generate_lawnmower.image = games.lawnmower_img
            generate_lawnmower.__dict__.update(lawnmower_here.__dict__)
            if generate_lawnmower.mode == 0:
                self.hp = 0
                self.status = 0
                games.killed_zombies += 1
                games.current_killed_zombies += 1
                games.killed_zombies_text.set(f'杀死僵尸数: {games.killed_zombies}')
                games.zombie_dead_normal(self)
            elif generate_lawnmower.mode == 1:
                self.hp -= generate_lawnmower.attack
            games.lawnmower_move(generate_lawnmower)
            lawnmower_here.show.configure(
                image=games.no_lawnmower_img,
                command=lambda: games.action_text.set('这里没有小推车了'))
            lawnmower_here.show.grid(row=self.rows, column=0)
            games.lawnmowers[self.rows] = 0
            return
    
        else:
            games.lose()
            games.mode = games.PAUSE
            return
    
    i, j = self.rows, self.columns
    self.button.grid(row=i, column=j)
    i, j = self.rows, self.columns
    current_grid = games.maps.grid_slaves(row=i, column=j)
    current_bullets = [
        x for x in current_grid if hasattr(x, 'bullet_img_name')
        and x.bullet_img_name in games.bullets_ls
    ]
    if current_bullets:
        attack_bullet = current_bullets[0]
        attack_bullet.bullet_sound[0].play()
        self.hp -= attack_bullet.attack
        attack_bullet.stop = True    



def shooting_check(self, games):
    if self.hp > 0:
        if not self.stop:
            if games.current_time - self.time >= self.move_speed:
                self.time = games.current_time
                shooting_move(self, games, -1)
    
def reset_func(self, games):
    self.stop = False
    shooting_move(self, games)

def shooting_newspaper(self, games):
    shooting_check(self, games)
    if self.hp >= 0:
        if not self.angry:
            if self.hp <= 10:
                random.choice(self.other_sound).play()
                self.angry = 1
                self.move_speed = 0.5
                self.attack = 36
                self.attack_speed = 100
                self.stop = True
                games.after(500, lambda: reset_func(self, games))

zombies_names = ['普通僵尸', '路障僵尸', '读报僵尸', '铁桶僵尸']
with open('common.py', encoding='utf-8') as f:
    exec(f.read())
for each in [普通僵尸, 路障僵尸, 铁桶僵尸]:
    each.move_speed = 5
    each.start_func = shooting_move
    each.eachtime_func = shooting_check
读报僵尸.start_func = shooting_move
读报僵尸.eachtime_func = shooting_newspaper

start_time = 2
part1 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 读报僵尸]), random.randint(0, 4),
                8, random.randint(1, 60))
    for i in range(20)
]

part2 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4),
                8, random.randint(1, 60))
    for i in range(20)
]

part3 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸, 读报僵尸]), random.randint(0, 4),
                8, random.randint(1, 60))
    for i in range(30)
]
big_wave1 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4),
                8, random.randint(1, 5)) for i in range(20)
]
big_wave2 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸, 读报僵尸]), random.randint(0, 4),
                8, random.randint(1, 5)) for i in range(20)
]
current_stage = Stage(2)
current_stage.set_normal_all(part1, part2, part3)
current_stage.set_waves_all(big_wave1, big_wave2)