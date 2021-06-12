from plant2 import *
import random, time
from copy import deepcopy


def snow_pea_check(self, games):
    i, j = self.rows, self.columns
    if any(x.status == 1 and x.rows == i and x.columns >= j
           for x in games.whole_zombies):
        if games.current_time - self.time >= self.attack_interval:
            self.time = games.current_time
            new_pea = games.make_label(games.maps, image=self.bullet_img)
            new_pea.image = self.bullet_img
            new_pea.bullet_img_name = self.bullet_img_name
            new_pea.bullet_speed = self.bullet_speed
            new_pea.attack = self.bullet_attack
            new_pea.bullet_sound = self.bullet_sound
            new_pea.rows = i
            new_pea.columns = j
            new_pea.name = 'snow pea'
            new_pea.attributes = 0
            new_pea.stop = False
            new_pea.func = self.bullet_func
            new_pea.target_zombies = None
            new_pea.sound = self.bullet_sound[1]
            new_pea.change_img = self.other_img[0][0]
            new_pea.used = 0
            new_pea.melt = 0
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
            if obj.used:
                if obj.target_zombies.status and games.current_time - (
                        obj.start_frozen + games.paused_time) >= 10:
                    obj.target_zombies.move_speed //= 2
                    obj.target_zombies.attack_speed //= 2
                    obj.target_zombies.frozen = 0
                    return
                else:
                    games.after(10, lambda: moving(games, obj))
            else:
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
                        key=lambda k:
                        (passed_time - k.appear_time) / k.move_speed,
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
                    if not obj.melt:
                        has_frozen = hasattr(hitted_zombies, 'frozen')
                        if (has_frozen and
                                not hitted_zombies.frozen) or (not has_frozen):
                            obj.sound.play()
                            hitted_zombies.frozen = 1
                            hitted_zombies.move_speed *= 2
                            hitted_zombies.attack_speed *= 2
                            obj.target_zombies = hitted_zombies
                            obj.used = 1
                            obj.start_frozen = deepcopy(games.current_time)
                            moving(games, obj)
                        else:
                            return
                    else:
                        return

                else:
                    games.after(obj.bullet_speed,
                                lambda: moving(games, obj, 1))
        else:
            obj.destroy()
            return
    else:
        games.moving_bullets.append(obj)
        return


寒冰射手 = plant2(name='寒冰射手',
              img='寒冰射手.png',
              price=175,
              hp=5,
              cooling_time=7.5,
              attack_interval=1.4,
              bullet_img='snow pea.png',
              bullet_speed=200,
              bullet_attack=1,
              bullet_sound=('sounds/throw.ogg', 'sounds/frozen.ogg'),
              func=snow_pea_check,
              bullet_func=moving,
              other_img=[['pea.png', 3]])
