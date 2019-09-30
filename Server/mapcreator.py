import folium
import numpy
import random

class MapGenerator():
	def __init__(self):
		self.warnicon = 'img/warn.png'
		self.alerticon = 'img/alert.png'
		self.icon_warn = folium.features.CustomIcon(self.warnicon, icon_size=(32, 32))
		self.icon_alert = folium.features.CustomIcon(self.alerticon, icon_size=(32, 32))

	def get_map(self, data, filename):
		# Data_part = [[geo], [trackid], [IsTruth]]
		#data = self.get_anfd(120)
		new_map = folium.Map(location=self.get_map_start_coord(data), zoom_start = 8)
		for data_part in data:
			folium.Marker(location=eval(str(data_part[0])), popup=f'Power: {data_part[1]} \nUserID: {data_part[2]} \nTrackID: {data_part[3]}', icon=folium.features.CustomIcon(self.alerticon, icon_size=(32, 32)) if data_part[4] == 0 else folium.features.CustomIcon(self.warnicon, icon_size=(32, 32))).add_to(new_map)#self.icon_warn if data_part[2] == 0 else self.icon_alert).add_to(new_map)
		new_map.save(outfile=filename)

	def get_map_start_coord(self, data):
		return eval(str(data[0][0]))

	def get_anfd(self, x):
		return [[[random.random() * 60, random.random() * 60 ], [str(random.random())], random.randint(0, 2)] for i in range(0, x)]