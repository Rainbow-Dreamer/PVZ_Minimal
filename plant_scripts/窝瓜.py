from plant import plant
import random


def squash_check(self, games):
    i, j = self.rows, self.columns
    if any(x.status == 1 and x.rows == i and abs(x.columns - j) <= 1
           for x in games.whole_zombies):
        random.choice(self.bullet_sound[0]).play()
        self.status = 0
        games.after(int(self.attack_interval * 1000),
                    lambda: squash_attack(self, games))


def squash_attack(self, games):
    i, j = self.rows, self.columns
    if self.hp > 0:
        self.bullet_sound[1].play()
        hit_zombies = [
            x for x in games.whole_zombies
            if x.status == 1 and x.rows == i and abs(x.columns - j) <= 1
        ]
        hit_zombies_middle = [x for x in hit_zombies if x.columns == j]
        if len(hit_zombies_middle) != 0:
            for each in hit_zombies_middle:
                each.hp -= self.bullet_attack
                if each.hp <= 0:
                    each.status = 0
                    games.killed_zombies += 1
                    games.current_killed_zombies += 1
                    games.killed_zombies_text.set(
                        f'杀死僵尸数: {games.killed_zombies}')
                    each.button.destroy()
        else:
            hit_zombies_right = [x for x in hit_zombies if x.columns - j == 1]
            if len(hit_zombies_right) != 0:
                for each in hit_zombies_right:
                    each.hp -= self.bullet_attack
                    if each.hp <= 0:
                        each.status = 0
                        games.killed_zombies += 1
                        games.current_killed_zombies += 1
                        games.killed_zombies_text.set(
                            f'杀死僵尸数: {games.killed_zombies}')
                        each.button.destroy()
            else:
                hit_zombies_left = [
                    x for x in hit_zombies if x.columns - j == -1
                ]
                if len(hit_zombies_left) != 0:
                    for each in hit_zombies_left:
                        each.hp -= self.bullet_attack
                        if each.hp <= 0:
                            each.status = 0
                            games.killed_zombies += 1
                            games.current_killed_zombies += 1
                            games.killed_zombies_text.set(
                                f'杀死僵尸数: {games.killed_zombies}')
                            each.button.destroy()
        squash_block = games.blocks[i][j]
        squash_block.configure(image=games.lawn_photo)
        squash_block.plants = None


窝瓜 = plant(name='窝瓜',
           img='窝瓜.png',
           price=50,
           hp=5,
           cooling_time=30,
           attack_interval=1.5,
           bullet_attack=90,
           bullet_sound=(['sounds/squash_hmm.ogg', 'sounds/squash_hmm2.ogg'],
                         'sounds/gargantuar_thump.ogg'),
           func=squash_check)
