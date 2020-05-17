# 这是一个魔鬼难度的关卡，给你的植物开挂了你也打不过系列
start_time = 5
zombies_names = ['普通僵尸', '路障僵尸', '读报僵尸', '撑杆僵尸', '铁桶僵尸']
with open('common.py', encoding='utf-8') as f:
    exec(f.read())
start_time = 5
for each in zombies_sample:
    each.move_speed = 200
    each.attack_speed = 500
# 这个modified.py给你的植物可以给你的植物全部价格设为0，冷却时间也设为0，
# 但是就这样你也是打不过
modified_file = 'modified.py'
part1 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4),
                8, random.randint(1, 60)) for i in range(200)
]

part2 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4),
                8, random.randint(1, 60)) for i in range(300)
]

part3 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4),
                8, random.randint(1, 60)) for i in range(300)
]
big_wave1 = [
    get_zombies(普通僵尸, random.randint(0, 4), 8, random.randint(1, 5))
    for i in range(100)
]
big_wave2 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4),
                8, random.randint(1, 5)) for i in range(100)
]
current_stage = Stage(2)
current_stage.set_normal(0, part1)
current_stage.set_normal(1, part2)
current_stage.set_normal(2, part3)
current_stage.set_waves(0, big_wave1)
current_stage.set_waves(1, big_wave2)