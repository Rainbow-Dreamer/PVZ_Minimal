import os, sys, importlib, pygame
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import datetime, time, random, keyboard
import time, random, os
from copy import deepcopy
from game_path import game_path
with open(game_path, encoding='utf-8') as f:
    exec(f.read())