from plant import plant
'''
十字火爆辣椒

特性：对当前所在行和所在列都进行一整排的燃烧，伤害和火爆辣椒一样。

火爆辣椒总是很羡慕他的哥哥，因为他的哥哥很喜欢搞发明创造，虽然实际上
很多时候看着并不是很有用。这一次，哥哥做了一个新发明，比起之前的整行
攻击，现在也可以同时烧整列了。“哇，好厉害”，火爆辣椒对他哥哥说道。
樱桃炸弹和毁灭菇在旁边窃窃私语：“好像也没有什么用呀”， “或许某些
时候会派上用场呢”。哥哥说道：“虽然我觉得还可以，但是我的价格肯定是要
贵一些的了。”
'''

def jalapeno_check(self, games):
    if games.current_time - self.time >= self.attack_interval:
        self.status = 0
        jalapeno_explode(self, games)


def jalapeno_explode(self, games):
    i, j = self.rows, self.columns
    if self.hp > 0:
        self.bullet_sound[0].play()
        fire_ls_row = []
        for k in range(games.map_columns):
            current_button = games.make_button(
                games.maps,
                image=self.bullet_img,
                command=lambda i=i, k=k: games.block_action(i, k))
            current_button.image = self.bullet_img
            current_button.grid(row=i, column=k)
            fire_ls_row.append(current_button)
            games.after(2000, current_button.destroy)
        fire_ls_col = [0 for r in range(games.map_rows)]
        for t in range(games.map_rows):
            if t != i:
                current_button = games.make_button(
                    games.maps,
                    image=self.bullet_img,
                    command=lambda t=t, j=j: games.block_action(t, j))
                current_button.image = self.bullet_img
                current_button.grid(row=t, column=j)
                fire_ls_col[t] = current_button
                games.after(2000, current_button.destroy)

        attack_zombies_row = [
            x for x in games.whole_zombies if x.status == 1 and x.rows == i
        ]
        attack_zombies_col = [
            x for x in games.whole_zombies
            if x.status == 1 and x.rows != i and x.columns + x.adjust_col +
            1 == j
        ]
        for each in attack_zombies_row:
            each.hp -= self.bullet_attack
            if each.hp <= 0:
                each.status = 0
                games.killed_zombies += 1
                games.current_killed_zombies += 1
                games.killed_zombies_text.set(f'杀死僵尸数: {games.killed_zombies}')
                each.button.configure(image=games.zombie_explode_img)
                fire_ls_row[each.columns + 1 + each.adjust_col].destroy()
                games.after(3000, lambda t=each: t.button.destroy())
        for each in attack_zombies_col:
            each.hp -= self.bullet_attack
            if each.hp <= 0:
                each.status = 0
                games.killed_zombies += 1
                games.current_killed_zombies += 1
                games.killed_zombies_text.set(f'杀死僵尸数: {games.killed_zombies}')
                each.button.configure(image=games.zombie_explode_img)
                fire_ls_col[each.rows].destroy()
                games.after(3000, lambda t=each: t.button.destroy())
        jalapeno_blocks = games.blocks[i][j]
        jalapeno_blocks.configure(image=games.lawn_photo)
        jalapeno_blocks.plants = None


十字火爆辣椒 = plant(name='十字火爆辣椒',
               img='super_jalapeno.png',
               price=150,
               hp=5,
               cooling_time=50,
               attack_interval=2,
               bullet_img='Fire1_1.png',
               bullet_attack=90,
               bullet_sound=('sounds/jalapeno.ogg', ),
               is_bullet=False,
               func=jalapeno_check)
