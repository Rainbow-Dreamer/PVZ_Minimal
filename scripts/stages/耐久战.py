# 这关有很多僵尸，需要考验你的耐久能力，有很多波，请好好布置阵型
zombies_names = ['普通僵尸', '路障僵尸', '铁桶僵尸', '舞王僵尸', '撑杆僵尸']
with open('common.py', encoding='utf-8') as f:
    exec(f.read(), globals())
start_time = 5
part1 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸]), random.randint(0, 4), 8,
                random.randint(1, 120)) for i in range(80)
]

part2 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 撑杆僵尸]), random.randint(0, 4), 8,
                random.randint(1, 120)) for i in range(80)
]

part3 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4), 8,
                random.randint(1, 120)) for i in range(120)
]
part4 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸, 撑杆僵尸]), random.randint(0, 4),
                8, random.randint(1, 120)) for i in range(120)
]
part5 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 铁桶僵尸, 撑杆僵尸, 舞王僵尸]),
                random.randint(0, 4), 8, random.randint(1, 120))
    for i in range(180)
]
part6 = [
    get_zombies(random.choice([路障僵尸, 铁桶僵尸, 撑杆僵尸, 舞王僵尸]), random.randint(0, 4),
                8, random.randint(1, 120)) for i in range(180)
]
part7 = [
    get_zombies(random.choice([铁桶僵尸, 撑杆僵尸, 舞王僵尸]), random.randint(0, 4), 8,
                random.randint(1, 120)) for i in range(300)
]
big_wave1 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸]), random.randint(0, 4), 8,
                random.randint(1, 10)) for i in range(200)
]
big_wave2 = [
    get_zombies(random.choice([普通僵尸, 路障僵尸, 撑杆僵尸]), random.randint(0, 4), 8,
                random.randint(1, 10)) for i in range(200)
]
big_wave3 = [
    get_zombies(random.choice([撑杆僵尸, 路障僵尸, 铁桶僵尸]), random.randint(0, 4), 8,
                random.randint(1, 10)) for i in range(300)
]
big_wave4 = [
    get_zombies(random.choice([撑杆僵尸, 铁桶僵尸, 舞王僵尸]), random.randint(0, 4), 8,
                random.randint(1, 10)) for i in range(300)
]
big_wave5 = [
    get_zombies(random.choice([铁桶僵尸, 舞王僵尸]), random.randint(0, 4), 8,
                random.randint(1, 20)) for i in range(450)
]
big_wave6 = [
    get_zombies(random.choice([撑杆僵尸, 路障僵尸, 铁桶僵尸, 舞王僵尸]), random.randint(0, 4),
                8, random.randint(1, 20)) for i in range(600)
]
current_stage = Stage(6)
current_stage.set_normal_all(part1, part2, part3, part4, part5, part6, part7)
current_stage.set_waves_all(big_wave1, big_wave2, big_wave3, big_wave4,
                            big_wave5, big_wave6)
map_content = [['day' for i in range(map_size[1])] for j in range(map_size[0])]
#以下几行可以把当前关卡的地图的第2到第3行变成水池
#for i in range(1, 3):
#for j in range(map_size[1]):
#map_content[i][j] = 'pool'
