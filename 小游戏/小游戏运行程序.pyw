import os, sys, importlib, pygame
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import datetime, time, random, keyboard
import time, random, os
from copy import deepcopy
abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
with open('game_path.py', encoding='utf-8-sig') as f:
    game_path = f.read().replace('\n', '')
with open(game_path, encoding='utf-8') as f:
    exec(f.read())