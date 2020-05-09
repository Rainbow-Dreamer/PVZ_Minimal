for k in zombies_dict:
    each = zombies_dict[k]
    each.move_speed = 200
    each.attack_speed = 500
for each in whole_plants:
    each.price = 0
    each.cooling_time = 0
part1 = [
    get_zombies(random.choice(['普通僵尸', '路障僵尸', '铁桶僵尸']), random.randint(0, 4),
                8, random.randint(1, 60)) for i in range(200)
]

part2 = [
    get_zombies(random.choice(['普通僵尸', '路障僵尸', '铁桶僵尸']), random.randint(0, 4),
                8, random.randint(1, 60)) for i in range(300)
]

part3 = [
    get_zombies(random.choice(['普通僵尸', '路障僵尸', '铁桶僵尸']), random.randint(0, 4),
                8, random.randint(1, 60)) for i in range(300)
]
big_wave1 = [
    get_zombies('普通僵尸', random.randint(0, 4), 8, random.randint(1, 5))
    for i in range(100)
]
big_wave2 = [
    get_zombies(random.choice(['普通僵尸', '路障僵尸', '铁桶僵尸']), random.randint(0, 4),
                8, random.randint(1, 5)) for i in range(100)
]
current_stage = Stage(2)
current_stage.set_normal(0, part1)
current_stage.set_normal(1, part2)
current_stage.set_normal(2, part3)
current_stage.set_waves(0, big_wave1)
current_stage.set_waves(1, big_wave2)