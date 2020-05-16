from plant import plant


def wallnut_explode(self, games):
    if self.hp <= 0:
        i, j = self.rows, self.columns
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
        wallnut_block = games.blocks[i][j]
        wallnut_block.configure(image=games.lawn_photo)
        wallnut_block.plants = None


爆炸坚果 = plant(name='爆炸坚果',
             img='Explode-o-nut1.png',
             price=100,
             hp=72,
             bullet_attack=90,
             cooling_time=30,
             bullet_sound=('sounds/cherrybomb.ogg', ),
             func=wallnut_explode,
             dead_normal=False)
