from plant import plant
text = '''
番薯

特性：吸引前方1x3的相邻行的僵尸到自己的行，防御力比坚果墙稍弱。

番薯总是散发着清香，让饥肠辘辘的僵尸们闻到味道就迫不及待地改变自己的行军路线。
没错，有什么先吃什么才是真理，何况是淀粉含量高的番薯，吃几口就马上有饱足感了。
'''


def move_here(each, i):
    each.rows = i
    if each.button.winfo_exists():
        each.button.grid(row=i, column=each.columns)


def attract(self, games):
    i, j = self.rows, self.columns
    adjacent_rows = [i - 1, i + 1]
    adjacent_rows = [k for k in adjacent_rows if 0 <= k < games.map_rows]
    adjacent_zombies = [
        x for x in games.whole_zombies if x.status == 1 and x.columns - 1 -
        x.adjust_col == j + 1 and x.rows in adjacent_rows
    ]
    for each in adjacent_zombies:
        games.after(2000, lambda each=each: move_here(each, i))


番薯 = plant(name='番薯',
           img='HDSweetPotato.png',
           price=150,
           hp=40,
           cooling_time=20,
           img_transparent=True,
           func=attract,
           information=text)
