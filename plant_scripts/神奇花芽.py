from plant import *
import random
def random_choose(self, games):
    if games.current_time - self.time >= self.attack_interval:
        choosed_plant = random.randint(0, games.plants_num-1)
        j, k = self.rows, self.columns
        current = games.blocks[j][k]
        current.plants = None
        current_time = games.current_time
        choose_plant = games.plants_generate[choosed_plant]
        current.plants = games.get_plant(choose_plant, j, k)
        games.make_img(current.plants)
        if current.plants.use_bullet_img_first:
            current.configure(image=current.plants.bullet_img)
        else:
            current.configure(image=current.plants.img)

        current.plants.time = current_time
        current_plant_name = current.plants.name
        current_choosed_plants = games.choosed_plants[choosed_plant]
        current.plants.button = current_choosed_plants.button
        games.action_text.set(
            f'你成功放置了{current_plant_name}在第{j+1}行，第{k+1}列')
        current.plants.button.textvariable.set(
            f'${current.plants.price} 冷却中')
        current_choosed_plants.counter = current_time
        current_choosed_plants.enable = 0
    


神奇花芽 = plant(name='神奇花芽',
             img='Sprout1.png',
             price=100,
             hp=5,
             cooling_time=7.5,
             attack_interval=2,
             func=random_choose)
