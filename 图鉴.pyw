import os, sys
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
with open('wiki_config.py',encoding='utf-8') as f:
    exec(f.read())
os.chdir('plant_scripts')
sys.path.append('.')
filename = os.listdir()
remove_ls = ['__pycache__', '__init__.py', 'plant.py']
for each in remove_ls:
    if each in filename:
        filename.remove(each)
plants_name = [x[:-3] for x in filename]
for k in filename:
    with open(k, encoding='utf-8') as f:
        exec(f.read())
plants_ls = [eval(i) for i in plants_name]
os.chdir('../resource')
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.minsize(*screen_size)
        self.title('图鉴')
        self.plants_frame = ttk.LabelFrame(self)
        self.plants_frame.place(x=0, y=0)
        max_num = num_each_row * max_rows
        N = len(plants_ls)
        self.num_of_pages = N//max_num
        self.pages = [[k*max_num, (k+1)*max_num] for k in range(self.num_of_pages)]
        if self.pages:
            self.pages += [[self.pages[-1][1], N]]
        else:
            max_num = N
        self.current_page = 0
        for i in range(N):
            current = plants_ls[i]
            current_img = Image.open(current.img)
            ratio = current_img.height / height
            current_img = current_img.resize(
                (int(current_img.width/ratio), height),
                Image.ANTIALIAS)
            current.img = ImageTk.PhotoImage(current_img) 
            current.button = ttk.Button(self.plants_frame, image=current.img, command=lambda i=i: self.show_info(i))        
        
        for i in range(max_num):
            current = plants_ls[i]
            current.button.grid(row=i//num_each_row, column=i%num_each_row)             
        self.update()
        plants_sizes = self.plants_frame.winfo_width(), self.plants_frame.winfo_height()
        self.info_frame = ttk.LabelFrame(self)
        self.info_frame.place(x=plants_sizes[0]+50, y=0)
        self.info_text = StringVar()
        self.info_label = ttk.Label(self.info_frame, textvariable=self.info_text, image='', compound=TOP)
        self.info_label.grid(row=0, column=0)
        self.page_frame = ttk.LabelFrame(self)
        self.page_frame.place(x=0, y=plants_sizes[1] + 20)
        self.pre_page = ttk.Button(self.page_frame, text='上一页', command=lambda: self.switch_page(-1))
        self.pre_page.grid(row=0, column=0)
        self.next_page = ttk.Button(self.page_frame, text='下一页', command=lambda: self.switch_page(1))
        self.next_page.grid(row=0, column=1)
    def show_info(self, i):
        choose_plant = plants_ls[i]
        self.info_label.configure(image=choose_plant.img)
        current_info = [choose_plant.name, f'所需阳光：{choose_plant.price}', 
                        f'生命值：{choose_plant.hp}', f'冷却时间：{choose_plant.cooling_time}',
                        choose_plant.information if choose_plant.information else '']
        self.info_text.set('\n'.join(current_info))
    def switch_page(self, num):
        page_num = self.current_page + num
        if 0 <= page_num <= self.num_of_pages:
            m, n = self.pages[self.current_page]
            for each in range(m, n):
                plants_ls[each].button.grid_forget()
            j, k = self.pages[page_num]
            for i in range(j, k):
                current = plants_ls[i]
                current.button.grid(row=(i-j)//num_each_row, column=(i-j)%num_each_row)     
            self.current_page = page_num

root = Root()


root.mainloop()
