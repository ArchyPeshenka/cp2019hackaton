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
class MainScreen(Screen):
	def __init__(self):
		super(MainScreen, self).__init__()
		self.map_button_state = True #True -> Not clicked ; False -> Clicked
		self.ksettings_button_state = True
		self.psettings_button_state = True

	def toggle_map_button(self):
		if self.map_button_state:
			self.ids["'mapimage'"].image_source = 'img/openmapon.png'
		else:
			self.ids["'mapimage'"].image_source = 'img/openmap.png'	
		self.map_button_state = not self.map_button_state

	def toggle_ksettings_button(self):
		if self.ksettings_button_state:
			self.ids["'ksettings'"].image_source = 'img/seton.png'
		else:
			self.ids["'ksettings'"].image_source = 'img/setoff.png'	
		self.ksettings_button_state = not self.ksettings_button_state

	def toggle_k_indicator(self, path):
		self.ids["'kind'"].i_image_source = path	

	def toggle_psettings_button(self):
		if self.psettings_button_state:
			self.ids["'psettings'"].image_source = 'img/seton.png'
		else:
			self.ids["'psettings'"].image_source = 'img/setoff.png'	
		self.psettings_button_state = not self.psettings_button_state

	def toggle_p_indicator(self, path):
		self.ids["'pind'"].i_image_source = path


class ServerInterfaceApp(App):
	def build(self, ):
		self.build_interface()
		self.mainscreen = MainScreen()

		#Settings of our ЭВРИСТИЧЕСКАЯ НА ВСЕ СТО model
		self.k_value = 1
		self.p_value = 1
		self.radius_value = 0.001

		#Settings for ui
		self.k_modifier = 0
		self.p_modifier = 0
		self.k_ui = {0:'img/light.png', 1:'img/normal.png', 2:'img/hard.png'}
		self.p_ui = {0:'img/light.png', 1:'img/normal.png', 2:'img/hard.png'}

		self.DataWorker = DataWorker()
		self.DataWorker.load_data()
		return self.mainscreen

	def build_interface(self, kvfile='main.kv'):
		with open(kvfile, 'r') as f:
			Builder.load_string(f.read())

	def toggle_map_btn(self):
		self.mainscreen.toggle_map_button()
		Clock.schedule_once(lambda x: self.mainscreen.toggle_map_button(), 0.04)

	def toggle_ks_btn(self):
		self.mainscreen.toggle_ksettings_button()

		if self.k_modifier != 2:
			self.k_modifier += 1
			self.k_value += 3
		else: 
			self.k_modifier = 0
			self.k_value = 0

		self.toggle_k_indicator(self.k_ui[self.k_modifier])
		Clock.schedule_once(lambda x: self.mainscreen.toggle_ksettings_button(), 0.04)

	def toggle_k_indicator(self, path):
		self.mainscreen.toggle_k_indicator(path)

	def toggle_ps_btn(self):
		self.mainscreen.toggle_psettings_button()

		if self.p_modifier != 2:
			self.p_modifier += 1
			self.p_value += 0.6
		else: 
			self.p_modifier = 0
			self.p_value = 0.6

		self.toggle_p_indicator(self.p_ui[self.p_modifier])
		Clock.schedule_once(lambda x: self.mainscreen.toggle_psettings_button(), 0.04)

	def toggle_p_indicator(self, path):
		self.mainscreen.toggle_p_indicator(path)

	def get_values(self):
		if self.mainscreen.ids["'userid'"].text != '' or self.mainscreen.ids["'userid'"].text != 'None':
			userid = self.mainscreen.ids["'userid'"].text
		else:
			userid = False

		if self.mainscreen.ids["'trackid'"].text != '' or self.mainscreen.ids["'trackid'"].text != 'None':
			trackid = self.mainscreen.ids["'userid'"].text
		else:
			trackid = False

		if self.mainscreen.ids["'email'"].text != '' or self.mainscreen.ids["'email'"].text != 'None':
			email = self.mainscreen.ids["'email'"].text
		else:
			email = False

		return userid, trackid, email

	def generate_map_and_open(self):
		userid, trackid, email = self.get_values()
		self.DataWorker.load_data()
		self.DataWorker.prod_get_graph(self.p_value, 'map.html', radius=0.0005, k=self.k_value)
		webbrowser.open('map.html')



if __name__ == '__main__':
	ServerInterfaceApp().run()
