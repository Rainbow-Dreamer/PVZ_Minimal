import os, sys, importlib, pygame, time, random, keyboard
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from copy import deepcopy

abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
with open('scripts/game_path.py', encoding='utf-8') as f:
    game_path = f.read()
with open(game_path, encoding='utf-8') as f:
    exec(f.read())