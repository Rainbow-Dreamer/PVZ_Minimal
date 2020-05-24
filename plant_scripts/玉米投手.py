from plant import plant
import random, time


def corn_check(self, games):
    i, j = self.rows, self.columns
    if any(x.status == 1 and x.rows == i and x.columns + 1 + x.adjust_col >= j
           for x in games.whole_zombies):
        if games.current_time - self.time >= self.attack_interval:
            self.time = games.current_time
            which = random.choices([0, 1], weights=[0.75, 0.25], k=1)[0]
            if which == 0:
                new_bullet = games.make_label(games.maps,
                                              image=self.bullet_img)
                new_bullet.image = self.bullet_img
                new_bullet.bullet_img_name = self.bullet_img_name
                new_bullet.attack = self.bullet_attack
                new_bullet.is_butter = 0
            else:
                butter_img = self.other_img[0][0]
                new_bullet = games.make_label(games.maps, image=butter_img)
                new_bullet.image = butter_img
                new_bullet.bullet_img_name = self.other_img[0][1]
                new_bullet.attack = self.bullet_attack * 2
                new_bullet.is_butter = 1
            new_bullet.waiting = 0
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
        if obj.stop:
            obj.destroy()
            return
        if obj.waiting:
            if obj.hit_zombies.hp <= 0:
                for k in obj.hit_zombies.butter_obj:
                    k.destroy()
                return
            if games.current_time - obj.time >= 5:
                if obj.hit_zombies.stick_butter == 1:
                    obj.hit_zombies.stick_butter = 0
                    obj.hit_zombies.time = games.current_time - obj.hit_zombies.remain_time
                    obj.hit_zombies.stop = False
                    for k in obj.hit_zombies.butter_obj:
                        k.destroy()
                    obj.hit_zombies.butter_obj = []
                    obj.hit_zombies.start_func(obj.hit_zombies, games)
                else:
                    obj.hit_zombies.stick_butter -= 1
                return
            else:
                games.after(10, lambda: moving(games, obj))
        else:
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
                        key=lambda k:
                        (passed_time - k.appear_time) / k.move_speed,
                        reverse=True)
                    hitted_zombies = affect_zombies[0]
                    hitted_zombies.hp -= obj.attack
                    if type(hitted_zombies.hit_sound) == list:
                        random.choice(hitted_zombies.hit_sound).play()
                    else:
                        hitted_zombies.hit_sound.play()
                    if not obj.is_butter:
                        obj.destroy()
                        return
                    else:
                        obj.waiting = 1
                        hitted_zombies.stop = True
                        if not hasattr(hitted_zombies, 'stick_butter'):
                            hitted_zombies.remain_time = games.current_time - hitted_zombies.time
                            hitted_zombies.stick_butter = 1
                            hitted_zombies.butter_obj = [obj]
                        else:
                            if hitted_zombies.stick_butter == 0:
                                hitted_zombies.remain_time = games.current_time - hitted_zombies.time                            
                            hitted_zombies.stick_butter += 1
                            hitted_zombies.butter_obj.append(obj)
                        obj.hit_zombies = hitted_zombies
                        obj.time = games.current_time
                        games.after(10, lambda: moving(games, obj))
                else:
                    games.after(obj.bullet_speed,
                                lambda: moving(games, obj, 1))
            else:
                obj.destroy()
                return
    else:
        games.moving_bullets.append(obj)
        return


玉米投手 = plant(name='玉米投手',
             img='Kernel-pult1.png',
             price=100,
             hp=5,
             cooling_time=7.5,
             attack_interval=3,
             bullet_img='Cornpult_kernal.png',
             bullet_speed=200,
             bullet_attack=1,
             bullet_sound=('sounds/throw.ogg', ),
             func=corn_check,
             other_img=[['Cornpult_butter.png', 3, True]],
             bullet_func=moving)
