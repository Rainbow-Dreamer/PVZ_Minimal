from plant import plant
import random, time


def peashooter_check(self, games):
    i, j = self.rows, self.columns
    self.time = games.current_time
    new_pea = games.make_label(games.maps, image=self.bullet_img)
    new_pea.image = self.bullet_img
    new_pea.bullet_img_name = self.bullet_img_name
    new_pea.bullet_speed = self.bullet_speed
    new_pea.attack = self.bullet_attack
    new_pea.bullet_sound = self.bullet_sound
    new_pea.rows = i
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





def cat_check(self, games):
        self.time = games.current_time
        i, j = self.rows, self.columns
        now_zombies = [x for x in games.whole_zombies if x.status == 1]
        distances = [((each.rows - i)**2 + (each.columns - j)**2)**0.5 for each in now_zombies]
        if now_zombies:
            inds = distances.index(min(distances))
            target_zombies = now_zombies[inds]    
            shoot(self, games, target_zombies)
            
            
def shoot(self, games, target):
    i, j = self.rows, self.columns
    new_thron = games.make_label(games.maps, image=self.other_img[0][0])
    new_thron.image = [k[0] for k in self.other_img]
    new_thron.bullet_img_name = self.bullet_img_name
    new_thron.bullet_speed = self.bullet_speed
    new_thron.attack = self.bullet_attack
    new_thron.bullet_sound = self.bullet_sound
    new_thron.rows = i
    new_thron.columns = j
    new_thron.attributes = 0
    new_thron.stop = False
    new_thron.func = self.bullet_func
    new_thron.direction = 0
    self.bullet_sound[0].play()
    moving_cat(games, new_thron, target)    

def moving_cat(games, obj, target, columns_move=0, rows_move=0):
    '''
    direction:
    0: right
    1: left
    2: up
    3: down
    4: rightup
    5: leftup
    6: rightdown
    7: leftdown
    '''    
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
                        direction = 0
                    else:
                        columns_move = -1
                        direction = 1
                else:
                    columns_move = 0
                    if row_diff >= 0:
                        rows_move = 1
                        direction = 3
                    else:
                        rows_move = -1
                        direction = 2
            else:
                if row_diff >= 0:
                    rows_move = 1
                else:
                    rows_move = -1
                if col_diff >= 0:
                    columns_move = 1
                else:
                    columns_move = -1 
                if rows_move == 1 and columns_move == 1:
                    direction = 6
                elif rows_move == 1 and columns_move == -1:
                    direction = 7
                elif rows_move == -1 and columns_move == 1:
                    direction = 4
                elif rows_move == -1 and columns_move == -1:
                    direction = 5   
            if direction != obj.direction:
                obj.direction = direction
                obj.configure(image=obj.image[direction])
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
            games.after(obj.bullet_speed, lambda: moving_cat(games, obj, target, columns_move, rows_move))
        else:
            obj.destroy()
            return
    else:
        games.moving_bullets.append(obj)
        return








豌豆射手_枪林弹雨 = plant(name='豌豆射手',
             img='豌豆射手.png',
             price=100,
             hp=5,
             cooling_time=7.5,
             attack_interval=1.4,
             bullet_img='pea.png',
             bullet_speed=200,
             bullet_attack=1,
             bullet_sound=('sounds/throw.ogg', ),
             func=cat_check,
             bullet_func=moving,
             other_img=[['thron.png', 3, True]] + [[f'thron{k}.png', 3, True] for k in [4, 2, 6, 1, 3, 7, 5]])
