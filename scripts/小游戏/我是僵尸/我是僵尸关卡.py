# 随机生成植物，按照一定的难度规则
plants_list = [[random.choice(whole_plants) for j in range(plant_line)]
               for i in range(map_size[0])]
num_of_sunflowers = len([i for j in plants_list for i in j if i.name == '向日葵'])
if num_of_sunflowers < 2:
    difference = 2 - num_of_sunflowers
    sunflower_obj = [i for i in whole_plants if i.name == '向日葵'][0]
    whole_inds = [[i, j] for i in range(plant_line)
                  for j in range(map_size[0])]
    replace_inds = random.sample(whole_inds, difference)
    for k in replace_inds:
        plants_list[k[0]][k[1]] = sunflower_obj