from plant2 import *
import random

text = '''
神奇花芽

特性：随机变成一个当前所选的植物。

小花芽刚从泥土里探出脑袋，就看到一堆高大很多的植物围在身边，
大家都不知道她未来会长成什么样的植物，因此都带着期盼的目光。
没错，这只是一株不知名的小花芽罢了，但是这是什么植物的花芽呢？
戴夫前几天在批发市场上看到有个小摊把一堆花芽摆在一起以同样的
价格出售，想着说不定能赚到一些好植物，也就估且买了一些回来。
现在，就是见证手气的时刻了。
'''


def random_choose(self, games):
    if games.current_time - self.time >= self.attack_interval:
        choosed_plant = random.randint(0, games.plants_num - 1)
        j, k = self.rows, self.columns
        current = games.blocks[j][k]
        current.plants = None
        current_time = games.current_time
        choose_plant = games.whole_plants[choosed_plant]
        current.plants = games.get_plant(choose_plant, j, k)
        games.make_img(current.plants)
        if current.plants.use_bullet_img_first:
            current.configure(image=current.plants.bullet_img)
        else:
            current.configure(image=current.plants.img)

        current.plants.time = current_time
        current_plant_name = current.plants.name
        games.action_text.set(f'你成功放置了{current_plant_name}在第{j+1}行，第{k+1}列')


神奇花芽 = plant2(name='神奇花芽',
              img='神奇花芽.png',
              price=100,
              hp=5,
              cooling_time=7.5,
              attack_interval=2,
              func=random_choose,
              information=text)
