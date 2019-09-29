# *-* coding: utf-8 *-*
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

from sensors import Accelerometer, GPSTracker
from deploy import DataDeploy

class MainScreen(Screen):
	def __init__(self):
		super(MainScreen, self).__init__()
		self.ids["'flt'"].color = (0.71, 0.02, 0.02, 1.0)

class RailDefectionDetectorApp(App):

	def build(self):
		self.fake = True
		self.standardserver = 'http://127.0.0.1:80/'
		self.active = False
		self.batch_size = 200
		self.color = {'Off': (0.71, 0.02, 0.02, 1.0), 'On': (0.4, 0.76, 0.1, 1.0)}
		self.button_on = True

		self.set_configs(480, 800, 1)
		self.build_interface()
		self.init_services(server=self.standardserver)
		self.schedule_dataflow(0.005)
		self.mainscreen = MainScreen()
		return self.mainscreen
	
	def get_fake_data(self):
		return {'geo': [random.randint(0, 1000) * 0.2, random.randint(0, 1000) * 0.2], 'acc': [random.randint(0, 1000) * 0.2, random.randint(0, 1000) * 0.2, random.randint(0, 1000) * 0.2]}
	
	def get_data(self):
		if self.active:
			if not self.fake:
				if self.gps.check_active():
					self.datadeploy.add_to_buffer(self.gps.get_location()[0], self.acc.get_state())
				else:
					# -404 means No Data
					self.datadeploy.add_to_buffer([-404, -404], self.acc.get_state())
			else:
				#Generate fake data (for testing purposes only)
				self.datadeploy.add_to_buffer(**self.get_fake_data())

	def send_data(self):
		if self.active:
			print(self.datadeploy.get_buffer_len())
			while self.datadeploy.get_buffer_len() >= self.batch_size and self.datadeploy.check_connection():
				self.datadeploy.post_from_buffer(self.batch_size)

	def schedule_dataflow(self, frequency):
		Clock.schedule_interval(lambda somefunc_one: self.get_data(), frequency)
		Clock.schedule_interval(lambda somefunc_two: self.send_data(), frequency)

	def init_services(self, server):
		self.gps = GPSTracker()
		self.acc = Accelerometer()
		self.datadeploy = DataDeploy(server)

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
		self.active = not self.active
		if self.button_on:
			print(self.mainscreen.ids)
			self.mainscreen.ids["'mainbutton'"].text = 'Stop services'
			self.mainscreen.ids["'flt'"].color = self.color['On']
			self.mainscreen.ids["'btn'"].src = 'data/img/btnred.png'
			self.run_services()
		else:
			self.mainscreen.ids["'mainbutton'"].text = 'Run services'
			self.stop_services()
			self.mainscreen.ids["'flt'"].color = self.color['Off']
			self.mainscreen.ids["'btn'"].src = 'data/img/btn.png'
		self.button_on = not self.button_on

		return True	

if __name__ == '__main__':
	RailDefectionDetectorApp().run()