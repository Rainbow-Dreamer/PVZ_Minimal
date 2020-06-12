# 这是一个很简单的预设关卡
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
map_content = [['day' for i in range(map_size[1])] for j in range(map_size[0])]
#以下几行可以把当前关卡的地图的第2到第3行变成水池
#for i in range(1, 3):
    #for j in range(map_size[1]):
        #map_content[i][j] = 'pool'

