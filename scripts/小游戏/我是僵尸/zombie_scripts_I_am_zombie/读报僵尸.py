from zombies2 import *
from regular import *
import random


def reset_func(self, games):
    self.stop = False
    zombie_move(self, games, -1)


def newspaper(self, games):
    if self.hp >= 0:
        next_to_plant(self, games)
        if not self.angry:
            if self.hp <= 10:
                random.choice(self.other_sound).play()
                self.angry = 1
                self.move_speed = 0.5
                self.attack = 36
                self.attack_speed = 100
                self.stop = True
                games.after(500, lambda: reset_func(self, games))


读报僵尸 = zombies2(name='读报僵尸',
                img='Newspaper_Zombie1.png',
                hp=17.5,
                price=200,
                move_speed=9,
                attack=1,
                attack_speed=1000,
                attack_sound=regular_attack_sound,
                dead_sound=regular_dead_sound,
                hit_sound=regular_hit_sound,
                hp_img=[(7.5, 'newspaper angry.png')],
                change_mode=2,
                start_func=zombie_move,
                eachtime_func=newspaper,
                repause_func=repause,
                other_sound=[
                    'sounds/newspaper_rarrgh.ogg',
                    'sounds/newspaper_rarrgh2.ogg'
                ])
读报僵尸.angry = 0
