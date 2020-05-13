# 这是一个很简单的预设关卡
start_time = 5
part1 = [
    get_zombies(random.choice(['普通僵尸', '路障僵尸']), random.randint(0, 4), 8,
                random.randint(1, 120)) for i in range(20)
]

part2 = [
    get_zombies(random.choice(['普通僵尸', '路障僵尸']), random.randint(0, 4), 8,
                random.randint(1, 120)) for i in range(20)
]

part3 = [
    get_zombies(
        random.choices(['普通僵尸', '路障僵尸', '铁桶僵尸'], [0.45, 0.45, 0.1])[0],
        random.randint(0, 4), 8, random.randint(1, 60)) for i in range(20)
]
big_wave1 = [
    get_zombies('普通僵尸', random.randint(0, 4), 8, random.randint(1, 5))
    for i in range(25)
]
big_wave2 = [
    get_zombies(random.choice(['普通僵尸', '路障僵尸']), random.randint(0, 4), 8,
                random.randint(1, 5)) for i in range(25)
]
current_stage = Stage(2)
current_stage.set_normal(0, part1)
current_stage.set_normal(1, part2)
current_stage.set_normal(2, part3)
current_stage.set_waves(0, big_wave1)
current_stage.set_waves(1, big_wave2)