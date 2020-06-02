from plant import plant
import random, time


def cat_check(self, games):
    if any(x.status == 1 for x in games.whole_zombies):
        if games.current_time - self.time >= self.attack_interval:
            self.time = games.current_time
            i, j = self.rows, self.columns
            now_zombies = [x for x in games.whole_zombies if x.status == 1]
            distances = [((each.rows - i)**2 + (each.columns - j)**2)**0.5 for each in now_zombies]
            inds = distances.index(min(distances))
            target_zombies = now_zombies[inds]    
            shoot(self, games, target_zombies)
            games.after(200, lambda: shoot(self, games, target_zombies))
            
            
def shoot(self, games, target):
    i, j = self.rows, self.columns
    new_thron = games.make_label(games.maps, image=self.bullet_img)
    new_thron.image = self.bullet_img
    new_thron.bullet_img_name = self.bullet_img_name
    new_thron.bullet_speed = self.bullet_speed
    new_thron.attack = self.bullet_attack
    new_thron.bullet_sound = self.bullet_sound
    new_thron.rows = i
    new_thron.columns = j
    new_thron.attributes = 0
    new_thron.stop = False
    new_thron.func = self.bullet_func
    self.bullet_sound[0].play()
    moving(games, new_thron, target)    

def moving(games, obj, target, columns_move=0, rows_move=0):
    if games.mode != games.PAUSE:
        if obj.stop:
            obj.destroy()
            return
        target_row, target_column = target.rows, target.columns
        obj.columns += columns_move
        obj.rows += rows_move
        i, j = obj.rows, obj.columns
        if target.hp > 0:
            row_diff = target_row - i
            col_diff = target_column - j
            if row_diff == 0 and col_diff == 0:
                obj.grid(row=i, column=j)
                target.hp -= obj.attack
                if type(target.hit_sound) == list:
                    random.choice(target.hit_sound).play()
                else:
                    target.hit_sound.play()
                games.after(500, obj.destroy)
                return
            affect_zombies = [x for x in games.whole_zombies
                    if x.status == 1 and x.rows == i and x.columns == j]
            if affect_zombies:
                passed_time = games.current_time - games.zombie_time
                affect_zombies.sort(
                    key=lambda k: (passed_time - k.appear_time) / k.move_speed,
                    reverse=True)            
                current = affect_zombies[0]
                obj.grid(row=i, column=j)
                current.hp -= obj.attack
                if type(current.hit_sound) == list:
                    random.choice(current.hit_sound).play()
                else:
                    current.hit_sound.play()
                games.after(500, obj.destroy)
                return            
            abs_row_diff = abs(row_diff)
            abs_col_diff = abs(col_diff)
            if abs_row_diff != abs_col_diff:
                if abs_col_diff > abs_row_diff:
                    rows_move = 0 
                    if col_diff >= 0:
                        columns_move = 1
                    else:
                        columns_move = -1
                else:
                    columns_move = 0
                    if row_diff >= 0:
                        rows_move = 1
                    else:
                        rows_move = -1
            else:
                if row_diff >= 0:
                    rows_move = 1
                else:
                    rows_move = -1
                if col_diff >= 0:
                    columns_move = 1
                else:
                    columns_move = -1     
        else:
            affect_zombies = [x for x in games.whole_zombies
                    if x.status == 1 and x.rows == i and x.columns == j]
            if affect_zombies:
                passed_time = games.current_time - games.zombie_time
                affect_zombies.sort(
                    key=lambda k: (passed_time - k.appear_time) / k.move_speed,
                    reverse=True)            
                current = affect_zombies[0]
                obj.grid(row=i, column=j)
                current.hp -= obj.attack
                if type(current.hit_sound) == list:
                    random.choice(current.hit_sound).play()
                else:
                    current.hit_sound.play()
                games.after(500, obj.destroy)
                return                        
            if columns_move == 0 and rows_move == 0:
                columns_move = 1
        if 0 <= j < games.map_columns and 0 <= i < games.map_rows:
            obj.grid(row=i, column=j)
            games.after(obj.bullet_speed, lambda: moving(games, obj, target, columns_move, rows_move))
        else:
            obj.destroy()
            return
    else:
        games.moving_bullets.append(obj)
        return


香蒲 = plant(name='香蒲',
             img='Cattail1.png',
             price=0,
             hp=5,
             cooling_time=0,
             attack_interval=1.4,
             bullet_img='thron.png',
             bullet_speed=200,
             bullet_attack=1,
             bullet_sound=('sounds/throw.ogg', ),
             func=cat_check,
             bullet_func=moving)
