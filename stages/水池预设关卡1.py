# 水池预设关卡1
zombies_names = ['普通僵尸', '路障僵尸', '铁桶僵尸']
with open('common.py', encoding='utf-8') as f:
    exec(f.read(), globals())
start_time = 5
part1 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸]), random.randint(0, 4), 8, random.randint(1, 120))
    for i in range(20)
]

part2 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸]), random.randint(0, 4), 8,
                random.randint(1, 120)) for i in range(30)
]

part3 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4), 8,
                random.randint(1, 120)) for i in range(20)
]
big_wave1 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸]), random.randint(0, 4), 8, random.randint(1, 5))
    for i in range(25)
]
big_wave2 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4), 8,
                random.randint(1, 5)) for i in range(25)
]
current_stage = Stage(2)
current_stage.set_normal_all(part1, part2, part3)
current_stage.set_waves_all(big_wave1, big_wave2)
map_size = 6, 9
lawn_size = 50
lawnmower_rows = [0, 1, 2, 3, 4, 5]
map_content = [['day' for i in range(map_size[1])] for j in range(map_size[0])]
for i in range(2, 4):
    for j in range(map_size[1]):
        map_content[i][j] = 'pool'
