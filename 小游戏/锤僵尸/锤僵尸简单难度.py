# 这是一个很简单的预设关卡
zombies_names = ['普通僵尸', '路障僵尸', '读报僵尸', '铁桶僵尸']
with open('common.py', encoding='utf-8') as f:
    exec(f.read())
for each in [普通僵尸, 路障僵尸, 读报僵尸, 铁桶僵尸]:
    each.move_speed = 2
读报僵尸.hp = 30
start_time = 5
part1 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸]), random.randint(0, 4),
                random.randint(3, 6), random.randint(1, 60))
    for i in range(100)
]

part2 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4),
                random.randint(3, 6), random.randint(1, 60))
    for i in range(100)
]

part3 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸, 读报僵尸]), random.randint(0, 4),
                random.randint(3, 6), random.randint(1, 60))
    for i in range(100)
]
big_wave1 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4),
                random.randint(3, 6), random.randint(1, 5)) for i in range(30)
]
big_wave2 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸, 读报僵尸]), random.randint(0, 4),
                random.randint(3, 6), random.randint(1, 5)) for i in range(30)
]
current_stage = Stage(2)
current_stage.set_normal_all(part1, part2, part3)
current_stage.set_waves_all(big_wave1, big_wave2)