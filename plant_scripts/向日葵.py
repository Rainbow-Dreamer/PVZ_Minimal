from plant import plant


def sunflower_check(self, games):
    i, j = self.rows, self.columns
    if games.current_time - self.time >= self.attack_interval:
        self.time = games.current_time
        flower_sunshine = games.make_button(
            games.maps,
            image=games.flower_sunshine_img,
            command=lambda: games.flower_get_sunshine(i, j, self.bullet_attack
                                                      ))
        flower_sunshine.image = games.fall_sunshine_img
        flower_sunshine.grid(row=i, column=j)
        self.sunshine_ls.append(flower_sunshine)


向日葵 = plant(name='向日葵',
            img='Sunflower1.png',
            price=50,
            hp=5,
            cooling_time=7.5,
            attack_interval=10,
            bullet_img='sun.png',
            bullet_attack=25,
            no_cooling_start=True,
            func=sunflower_check,
            is_bullet=False)
