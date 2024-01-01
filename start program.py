import os
import sys

abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
sys.path.append(abs_path)
sys.path.append('scripts')

import importlib
import pygame
import time
import random
import keyboard
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from copy import deepcopy

with open('scripts/pvz极简版.pyw', encoding='utf-8') as f:
    datas = f.read()
    exec(datas, globals())
