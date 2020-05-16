from zombies import *
from regular import *
路障僵尸 = zombies(name='路障僵尸',
               img='Conehead_Zombie1.png',
               hp=28,
               price=75,
               move_speed=9000,
               attack=1,
               attack_speed=1000,
               attack_sound=regular_attack_sound,
               dead_sound=regular_dead_sound,
               hit_sound=['sounds/plastichit.ogg', 'sounds/plastichit2.ogg'],
               hit_sound_ls=[[19, regular_hit_sound]],
               hp_img=((19, '0.png'), ),
               change_mode=2,
               start_func=zombie_move,
               eachtime_func=next_to_plant,
               repause_func=repause)
