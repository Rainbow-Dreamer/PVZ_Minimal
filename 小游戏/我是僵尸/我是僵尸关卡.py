# 随机生成植物，按照一定的难度规则
plants_list = [[random.choice(whole_plants) for j in range(plant_line)] for i in range(map_size[0])]