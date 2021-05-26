from zombies import *
from regular import *

普通僵尸 = zombies(name='普通僵尸',
               img='0.png',
               hp=10,
               move_speed=9,
               attack=1,
               attack_speed=1000,
               attack_sound=regular_attack_sound,
               dead_sound=regular_dead_sound,
               hit_sound=regular_hit_sound,
               start_func=zombie_move,
               eachtime_func=next_to_plant,
               repause_func=repause)