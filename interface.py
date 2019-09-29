import kivy

kivy.require('1.10.1')
__version__ = '0.1'

import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button 
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config

from preprocess import DataWorker
import webbrowser

