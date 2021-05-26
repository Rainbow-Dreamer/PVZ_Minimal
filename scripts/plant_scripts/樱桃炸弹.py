from plant import plant


def cherry_check(self, games):
    if games.current_time - self.time >= self.attack_interval:
        self.status = 0
        cherry_explode(self, games)


def cherry_explode(self, games):
    i, j = self.rows, self.columns
    if self.hp > 0:
        self.bullet_sound[0].play()
        around = [[i - 1 + x, j - 1 + y] for x in range(3) for y in range(3)]
        around = [
            k for k in around
            if 0 <= k[0] < games.map_rows and 0 <= k[1] < games.map_columns
        ]
        around_zombies = [
            q for q in games.whole_zombies
            if q.status == 1 and [q.rows, q.columns] in around
        ]
        for each in around_zombies:
            each.hp -= self.bullet_attack
            if each.hp <= 0:
                each.status = 0
                games.killed_zombies += 1
                games.current_killed_zombies += 1
                games.killed_zombies_text.set(f'杀死僵尸数: {games.killed_zombies}')
                each.button.configure(image=games.zombie_explode_img)
                games.after(3000, lambda t=each: t.button.destroy())
        cherry_block = games.blocks[i][j]
        cherry_block.configure(image=games.lawn_photo)
        cherry_block.plants = None


樱桃炸弹 = plant(name='樱桃炸弹',
             img='樱桃炸弹.png',
             price=150,
             hp=5,
             cooling_time=30,
             attack_interval=2,
             bullet_attack=90,
             bullet_sound=('sounds/cherrybomb.ogg', ),
             sound_volume=(0.5, ),
             func=cherry_check)
