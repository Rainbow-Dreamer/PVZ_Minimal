from plant import plant
import random, time


def chomper_check(self, games):
    i, j = self.rows, self.columns
    if self.eating:
        pass_time = time.time() - self.eating_time
        if pass_time >= 42:
            self.eating = False
            games.blocks[i][j].configure(image=self.img)
    else:
        if any(x.status == 1 and x.rows == i and 0 <= x.columns - 1 -
               x.adjust_col - j <= 1 for x in games.whole_zombies):
            self.eating = True
            self.eating_time = time.time()
            games.after(1000, lambda: chomper_attack(self, games))


def chomper_attack(self, games):
    i, j = self.rows, self.columns
    self.bullet_sound[0].play()
    hit_zombies = [
        x for x in games.whole_zombies
        if x.status == 1 and x.rows == i and 0 <= x.columns - 1 -
        x.adjust_col - j <= 1
    ]
    hit_zombies.sort(key=lambda s: s.columns - 1 - s.adjust_col - j)
    if hit_zombies:
        attack_zombies = hit_zombies[0]
        attack_zombies.hp = 0
        attack_zombies.status = 0
        games.killed_zombies += 1
        games.current_killed_zombies += 1
        games.killed_zombies_text.set(f'杀死僵尸数: {games.killed_zombies}')
        attack_zombies.button.destroy()
        games.blocks[i][j].configure(image=self.other_img[0][0])


大嘴花 = plant(name='大嘴花',
            img='大嘴花.png',
            price=150,
            hp=5,
            cooling_time=7.5,
            attack_interval=42,
            bullet_sound=('sounds/bigchomp.ogg', ),
            func=chomper_check,
            other_img=[['大嘴花2.png', 1]])
大嘴花.eating = False
大嘴花.eating_time = time.time()