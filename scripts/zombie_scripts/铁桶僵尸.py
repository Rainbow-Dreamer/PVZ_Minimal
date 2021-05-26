from zombies import *
from regular import *

铁桶僵尸 = zombies(name='铁桶僵尸',
               img='bucket.png',
               hp=66,
               move_speed=9,
               attack=1,
               attack_speed=1000,
               attack_sound=regular_attack_sound,
               dead_sound=regular_dead_sound,
               hit_sound=['sounds/shieldhit.ogg', 'sounds/shieldhit2.ogg'],
               hit_sound_ls=[[56, regular_hit_sound]],
               hp_img=[(19, 'bucket_first_damage.png'),
                       (38, 'bucket_second_damage.png'), (56, '0.png')],
               change_mode=2,
               start_func=zombie_move,
               eachtime_func=next_to_plant,
               repause_func=repause)
