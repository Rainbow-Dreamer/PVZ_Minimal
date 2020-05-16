from plant import plant


def move_here(each, i):
    each.rows = i
    each.button.grid(row=i, column=each.columns)


def attract(self, games):
    i, j = self.rows, self.columns
    adjacent_rows = [i - 1, i + 1]
    adjacent_rows = [k for k in adjacent_rows if 0 <= k < games.map_rows]
    adjacent_zombies = [
        x for x in games.whole_zombies if x.status == 1 and x.columns + 1 +
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
           func=attract)
