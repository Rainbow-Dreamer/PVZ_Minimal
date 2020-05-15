from plant import plant


def potato_checking(self, games):
    if games.current_time - self.time >= self.attack_interval:
        games.blocks[self.rows][self.columns].configure(image=self.img)
        self.bullet_sound[0].play()
        self.status = 0
        potato_detect(self, games)


def potato_detect(self, games):
    i, j = self.rows, self.columns
    if self.hp <= 0:
        return
    attack_zombies = [
        x for x in games.whole_zombies
        if x.status == 1 and x.rows == i and x.columns == j
    ]
    if len(attack_zombies) != 0:
        self.bullet_sound[1].play()
        for each in attack_zombies:
            each.hp -= self.bullet_attack
            if each.hp <= 0:
                each.status = 0
                games.killed_zombies += 1
                games.current_killed_zombies += 1
                games.killed_zombies_text.set(f'杀死僵尸数: {games.killed_zombies}')
                each.button.configure(image=games.zombie_explode_img)
                games.after(3000, lambda t=each: t.button.destroy())
        potato_block = games.blocks[i][j]
        potato_block.configure(image=games.lawn_photo)
        potato_block.plants = None
        return
    games.after(50, lambda: potato_detect(self, games))


土豆雷 = plant(name='土豆雷',
            img='Potato_Mine1.png',
            price=25,
            hp=5,
            cooling_time=30,
            attack_interval=15,
            bullet_img='UnarmedPotatoMine.png',
            bullet_attack=90,
            bullet_sound=('sounds/dirt_rise.ogg', 'sounds/potato_mine.ogg'),
            func=potato_checking,
            is_bullet=False)
