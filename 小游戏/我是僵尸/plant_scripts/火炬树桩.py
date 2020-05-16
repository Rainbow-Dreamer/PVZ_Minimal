from plant import plant
火炬树桩 = plant(name='火炬树桩',
             img='Torchwood1.png',
             price=175,
             hp=5,
             cooling_time=7.5,
             bullet_img='FirePea.png')


def fire_update(obj, self):
    if obj.attributes == 0:
        obj.attack *= 2
        obj.configure(image=self.bullet_img)
        obj.attributes = 1


火炬树桩.effects = {'bullet': fire_update}
