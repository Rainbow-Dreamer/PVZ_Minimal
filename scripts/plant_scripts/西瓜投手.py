from plant import plant
import random


def watermelon_check(self, games):
    i, j = self.rows, self.columns
    if any(x.status == 1 and x.rows == i and x.columns >= j
           for x in games.whole_zombies):
        if games.current_time - self.time >= self.attack_interval:
            self.time = games.current_time
            new_bullet = games.make_label(games.maps, image=self.bullet_img)
            new_bullet.image = self.bullet_img
            new_bullet.bullet_img_name = self.bullet_img_name
            new_bullet.attack = self.bullet_attack
            new_bullet.bullet_speed = self.bullet_speed
            new_bullet.bullet_sound = self.bullet_sound
            new_bullet.rows = i
            new_bullet.columns = j
            new_bullet.stop = False
            new_bullet.func = self.bullet_func
            self.bullet_sound[0].play()
            moving(games, new_bullet)


def moving(games, obj, columns_move=0, rows_move=0):
    if games.mode != games.PAUSE:
        obj.columns += columns_move
        obj.rows += rows_move
        i, j = obj.rows, obj.columns
        if j < games.map_columns:
            obj.grid(row=i, column=j)
            passed_time = games.current_time - games.zombie_time
            affect_zombies = [
                x for x in games.whole_zombies
                if x.status == 1 and x.rows == i and x.columns == j
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
                affect_attack = obj.attack / 2
                around = [[i - 1 + x, j - 1 + y] for x in range(3)
                          for y in range(3)]
                around = [
                    k for k in around if 0 <= k[0] < games.map_rows
                    and 0 <= k[1] < games.map_columns
                ]
                around_zombies = [
                    q for q in games.whole_zombies
                    if q.status == 1 and [q.rows, q.columns] in around
                ]
                if hitted_zombies in around_zombies:
                    around_zombies.remove(hitted_zombies)
                for each in around_zombies:
                    each.hp -= affect_attack
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


西瓜投手 = plant(name='西瓜投手',
             img='西瓜投手.png',
             price=300,
             hp=5,
             cooling_time=7.5,
             attack_interval=3,
             bullet_img='Melonpult_melon.png',
             bullet_speed=200,
             bullet_attack=4,
             bullet_sound=('sounds/throw.ogg', ),
             func=watermelon_check,
             bullet_func=moving)
