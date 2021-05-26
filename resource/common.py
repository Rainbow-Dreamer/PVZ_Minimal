os.chdir('..')
sys.path.append('.')
os.chdir('scripts')
for x in zombies_names:
    exec(f'from zombie_scripts.{x} import {x}', globals())
zombies_sample = deepcopy([eval(j, globals()) for j in zombies_names])
for every in zombies_sample:
    exec(f'{every.name} = every', globals())
os.chdir('../resource/')
for current_zombies in zombies_sample:
    current_zombies.attack_sound = [
        sounds(j) for j in current_zombies.attack_sound
    ]
    current_zombies.dead_sound = [
        sounds(j) if type(j) != list else [sounds(k) for k in j]
        for j in current_zombies.dead_sound
    ]
    current_zombies.hit_sound = [sounds(j) for j in current_zombies.hit_sound]
    if current_zombies.hit_sound_ls:
        for k in range(len(current_zombies.hit_sound_ls)):
            current = current_zombies.hit_sound_ls[k][1]
            current_zombies.hit_sound_ls[k][1] = sounds(current) if type(
                current) != list else [sounds(y) for y in current]
    if current_zombies.other_sound:
        current_zombies.other_sound = [
            sounds(k) for k in current_zombies.other_sound
        ]
