from plant2 import *

text = '''
爆炸坚果

特性：防御力和普通坚果墙一样，区别是僵尸吃完的时候，爆炸坚果会爆炸，
造成3x3范围的灰烬植物伤害。

爆炸坚果一直是坚果家族里的一个不合群的家伙，他总是对很多事都不满意，
总是红着脸生着不知道哪里来的气。僵尸们如果碰到他，那可就要小心了，
因为他可不是好惹之辈。别看坚果家族貌似都挺和善，但是这家伙可不一样。
'''


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


爆炸坚果 = plant2(name='爆炸坚果',
              img='爆炸坚果.png',
              price=100,
              hp=72,
              bullet_attack=90,
              cooling_time=30,
              bullet_sound=('sounds/cherrybomb.ogg', ),
              func=wallnut_explode,
              dead_normal=False,
              information=text,
              hp_img=((2 / 3, 'Explode-o-nut2.png'), (1 / 3,
                                                      'Explode-o-nut3.png')))
