# 子弹脚本包含多种游戏中会用到的子弹类型，可自行设计添加新的子弹
class bullet:
    def __init__(self, name, img, move_speed, attack, func, check_dict={}, sound=None, rows=None, columns=None, img_transparent=True, resize_num=3):
        self.name = name
        self.img = img
        self.img_name = img
        self.move_speed = move_speed
        self.attack = attack
        self.func = func
        self.check_dict = check_dict
        self.sound = sound
        self.rows = rows
        self.columns = columns
        self.stop = False
        self.img_transparent = img_transparent
        self.resize_num = resize_num


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
                        current_place.plants.effects['bullet'](obj)
            passed_time = time.time() - games.zombie_time
            affect_zombies = [
                x for x in games.whole_zombies if x.status == 1 and x.rows == i and x.columns + 1 + x.adjust_col == j
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
                    sputter = obj.attack/len(affect_zombies)
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



def snowpea_moving(games, obj, columns_move=0, rows_move=0):
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
                            current_place.plants.effects['bullet'](obj)
                passed_time = time.time() - games.zombie_time
                affect_zombies = [
                x for x in games.whole_zombies if x.status == 1 and x.rows == i and x.columns + 1 + x.adjust_col == j
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
                        sputter = obj.attack/len(affect_zombies)
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






普通豌豆 = bullet(name='普通豌豆',
                 img='pea.png',
                 move_speed=200,
                 attack=1,
                 func=moving,
                 sound=('sounds/throw.ogg', ),
                 check_dict={'attributes':0})

冰豌豆 = bullet(name='冰豌豆',
                 img='snow pea.png',
                 move_speed=200,
                 attack=1,
                 func=snowpea_moving,
                 sound=('sounds/throw.ogg', ),
                 check_dict={'attributes':0, 'used':0, 'melt':0})