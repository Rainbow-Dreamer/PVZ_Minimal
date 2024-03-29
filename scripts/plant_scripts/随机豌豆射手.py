from plant import plant
import random, time


def peashooter_check(self, games):
    i, j = self.rows, self.columns
    if any(x.status == 1 and x.rows == i and x.columns >= j
           for x in games.whole_zombies):
        if games.current_time - self.time >= self.attack_interval:
            self.time = games.current_time
            new_pea = games.make_label(games.maps, image=self.bullet_img)
            new_pea.image = self.bullet_img
            new_pea.bullet_img_name = self.bullet_img_name
            new_pea.bullet_speed = self.bullet_speed
            new_pea.attack = random.choices(
                [1, 2, 5, 10, 50], weights=[0.6, 0.25, 0.1, 0.04,
                                            0.01], k=1)[0]
            new_pea.bullet_sound = self.bullet_sound
            new_pea.rows = random.randint(0, games.map_rows - 1)
            new_pea.columns = j
            new_pea.attributes = 0
            new_pea.stop = False
            new_pea.func = self.bullet_func
            self.bullet_sound[0].play()
            moving(games, new_pea)


def moving(games, obj, columns_move=0, rows_move=0):
    if games.mode != games.PAUSE:
        if obj.stop:
            obj.destroy()
            return
        obj.columns += columns_move
        obj.rows += rows_move
        i, j = obj.rows, obj.columns
        if j < games.map_columns:
            obj.grid(row=i, column=j)
            current_place = games.blocks[i][j]
            if current_place.plants is not None:
                if current_place.plants.effects:
                    if 'bullet' in current_place.plants.effects:
                        current_place.plants.effects['bullet'](
                            current_place.plants, obj)
            passed_time = games.current_time - games.zombie_time
            affect_zombies = [
                x for x in games.whole_zombies
                if x.status == 1 and x.rows == i and x.columns - 1 -
                x.adjust_col == j
            ]
            if affect_zombies:
                affect_zombies.sort(
                    key=lambda k: (passed_time - k.appear_time) / k.move_speed,
                    reverse=True)
                hitted_zombies = affect_zombies[0]
                hitted_zombies.hp -= obj.attack
                if type(hitted_zombies.hit_sound) == list:
                    random.choice(hitted_zombies.hit_sound).play()
                else:
                    hitted_zombies.hit_sound.play()
                if obj.attributes == 1:
                    sputter = obj.attack / len(affect_zombies)
                    for sputter_zombies in affect_zombies[1:]:
                        sputter_zombies.hp -= sputter
                obj.destroy()
                return
            else:
                games.after(obj.bullet_speed, lambda: moving(games, obj, 1))
        else:
            obj.destroy()
            return
    else:
        games.moving_bullets.append(obj)
        return


text = '''
特性：当随机豌豆射手的右边任意一行出现僵尸的时候，从随机的一行发射一个攻击力随机的豌豆，
攻击力从1, 2, 5, 10, 50里面按照出现概率0.6, 0.25, 0.1, 0.04, 0.01里面随机选择。
'''

随机豌豆射手 = plant(name='随机豌豆射手',
               img='随机豌豆射手.png',
               price=200,
               hp=5,
               cooling_time=7.5,
               attack_interval=1.4,
               bullet_img='pea.png',
               bullet_speed=200,
               bullet_attack=1,
               bullet_sound=('sounds/throw.ogg', ),
               func=peashooter_check,
               bullet_func=moving,
               information=text)
