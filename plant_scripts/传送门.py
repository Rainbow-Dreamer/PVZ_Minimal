from plant import plant


SET_MODE = 'portal'

info = '''
传送门

特性：可以自己设置入口和出口的传送门，僵尸进入入口会从出口出来，
植物的子弹经过入口会从出口出来。每个传送门维持限时150秒，
放置150秒之后传送门会自己消失。
'''

def set_portal(self, i, j, games):
    if games.mode == SET_MODE:
        current = games.blocks[i][j]
        self.places.append([i, j])
        current.configure(image=self.other_img[0][0])
        games.mode = games.NULL
        games.action_text.set('成功放置传送门的另一端')
        for i in range(games.map_rows):
            for j in range(games.map_columns):
                games.blocks[i][j].configure(command=lambda i=i, j=j: games.block_action(i, j)) 
        games.bind("<Button-3>", lambda e: games.reset())
        self.place_time = games.current_time
        self.func = transport

def portal_reset(self, games):
    for i in range(games.map_rows):
        for j in range(games.map_columns):
            games.blocks[i][j].configure(command=lambda i=i, j=j: games.block_action(i, j))  
    games.action_text.set('已取消放置传送门')
    current = games.blocks[self.rows][self.columns]
    current.configure(image=games.lawn_photo)
    current.plants = None
    games.mode = games.NULL
    games.bind("<Button-3>", lambda e: games.reset())

def transport_set(self, games):
    self.places = [[self.rows, self.columns]]
    games.mode = SET_MODE
    games.action_text.set('传送门入口已放置，请选择传送门的另一端')
    for i in range(games.map_rows):
        for j in range(games.map_columns):
            games.blocks[i][j].configure(command=lambda i=i, j=j:set_portal(self, i, j, games))
    games.bind("<Button-3>", lambda e: portal_reset(self, games))
    self.func = None
    

def transport(self, games):
    i, j = self.rows, self.columns
    if games.current_time - self.place_time >= 150:
        block = games.blocks[i][j]
        block.configure(image=games.lawn_photo)
        block.plants.away_func(block.plants, games)
        block.plants.status = 0
        block.plants = None
        return
    affect_zombies = [each for each in games.whole_zombies if each.status == 1 and each.rows == i and each.columns - 1 - each.adjust_col == j]
    if affect_zombies:
        trans = self.places[1]
        for each in affect_zombies:
            each.stop = True
            each.nexted_plants = None
            each.button.grid_forget()
            each.rows = trans[0]
            each.columns = trans[1]
            each.button.grid(row=each.rows, column=each.columns)        
            each.stop = False


def transport_bullet(self, obj):
    if len(self.places) == 2:
        trans = self.places[1]
        obj.rows = trans[0]
        obj.columns = trans[1]

def portal_away(self, games):
        if len(self.places) == 2:
            trans = self.places[1]
            games.blocks[trans[0]][trans[1]].configure(image=games.lawn_photo)


传送门 = plant(name='传送门',
            img='传送门.png',
            price=200,
            hp=5,
            cooling_time=7.5,
            func=transport_set,
            away_func=portal_away,
            information=info,
            other_img=[['Portal2.jpg',1]],
            effects={'bullet':transport_bullet})
