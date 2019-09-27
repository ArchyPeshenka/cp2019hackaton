# *-* coding: utf-8 *-*
import kivy

kivy.require('1.10.1')
__version__ = '0.1'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button 

from kivy.lang import Builder
from kivy.config import Config

from sensors import Accelerometer, GPSTracker
from deploy import DataDeploy

class MainScreen(Screen):
	def __init__(self):
		super(MainScreen, self).__init__()
		

class RailDefectionDetectorApp(App):

	def build(self):
		self.button_on = True
		self.set_configs(480, 800, 1)
		self.build_interface()
		self.mainscreen = MainScreen()
		return self.mainscreen
		
	def init_services(self):
		self.gps = GPSTracker()
		self.acc = Accelerometer()
		self.datadeploy = DataDeploy('none')

	def stop_services(self):
		if self.gps.check_active():
			self.gps.deactivate()

	def run_services(self):
		if self.gps.check_active():
			self.gps.activate()

	def set_configs(self, width, height, resizable):
		self.width, self.height, self.resizable = width, height, resizable
		Config.set("graphics", "width", str(self.width))
		Config.set("graphics", "height", str(self.height))
		Config.set("graphics", "resizable", self.resizable)	

	def build_interface(self, kvfile='main.kv'):
		with open(kvfile, 'r') as f:
			Builder.load_string(f.read())

	def toggle_button(self):
		if self.button_on:
			print(self.mainscreen.ids)
			self.mainscreen.ids["'mainbutton'"].text = 'Stop services'
			self.run_services()
		else:
			self.mainscreen.ids["'mainbutton'"].text = 'Run services'
			self.stop_services()

		self.button_on = not self.button_on

		return True	

if __name__ == '__main__':
	RailDefectionDetectorApp().run()