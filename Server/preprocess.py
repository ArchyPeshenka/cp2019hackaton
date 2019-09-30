import numpy as np
import pandas as pd
from mapcreator import MapGenerator
from test_data import RandomDataGenerator
import math

class DataWorker():
	def __init__(self):
		self.dataframe = pd.DataFrame(columns=['UniqueID', 'TrackID', 'Timestamp', 'Geopos', 'Accdata'])
		self.mapgen = MapGenerator()


	def append_data(self, datastring):
		self.dataframe = self.dataframe.append(pd.Series(datastring), ignore_index=True)

	def append_batch(self, batch):
		for datastring in batch:
			self.append_data(datastring)

	def save_data(self, filename, dataframe=None, path='data/', inplace=False):
		if inplace:
			self.dataframe.to_csv(path + filename, index=False)
		else:
			dataframe.to_csv(path + filename, index=False)

	def load_data(self, filename='data.csv', path='data/'):
		self.dataframe = pd.read_csv(path + filename)
		self.dataframe['TrackID'] = self.dataframe.TrackID.apply(str)
		self.dataframe['UniqueID'] = self.dataframe.UniqueID.apply(str)
		print(self.dataframe.info())

	def calc_power(self, x):
		return np.linalg.norm(np.array(eval(str(x))))

	def limit_check(self, dataframe, limit):
		dataframe['Power'] = dataframe.loc[:, 'Accdata'].apply(self.calc_power)
		return dataframe[dataframe['Power'] >= limit]

	def get_destination(self, x1, x2):
		dlat = x2[0] - x1[0]
		dlon = x2[1] - x2[1]

		x1[0] = x1[0] * math.pi * 180
		x2[0] = x2[0] * math.pi * 180

		a = math.sin(dlat/2) * math.sin(dlat/2) + math.sin(dlon/2) * math.sin(dlon/2) * math.cos(x1[0]) * math.cos(x2[0]) * 6371
		return a

	def k_nearest_check(self, data, radius=0.01, k=10):
		print(len(data))
		data = data.reset_index()
		data['IsTruth'] = pd.Series([i for i in range(0, len(data))])
		for index in range(0, len(data) - 1):
			geopos = data.loc[index, 'Geopos']
			k_ = 0
			for index_ in range(index + 1, len(data)):
				geopos_ = data.loc[index_, 'Geopos']
				if self.get_destination(eval(geopos), eval(geopos_)) <= radius:#np.sqrt(np.sum((np.asarray(eval(geopos)) - np.asarray(eval(geopos_))) ** 2)) <= radius:
					#print(self.get_destination(eval(geopos), eval(geopos_)))
					k_ += 1
			if k_ >= k:
				data.loc[index, 'IsTruth'] = 1
			else:
				data.loc[index, 'IsTruth'] = 0
		return data

	# Вспомогательгые функции сортировки и выборки данных

	def get_tracks(self, dataframe):
		return dataframe.iloc[:, 'TrackID'].unique()
	
	def sort_by_track(self, dataframe, track_id, inplace=True):
		if not inplace:
			return dataframe[dataframe['TrackID'] == track_id]
		else:
			self.dataframe = self.dataframe[self.dataframe['TrackID'] == track_id]
			self.dataframe.reset_index()

	def get_users(self, dataframe):
		return dataframe.iloc[:, 'UniqueID'].unique()
	
	def sort_by_users(self, dataframe, user_id, inplace=True):
		if not inplace:
			return dataframe[dataframe['UniqueID'] == user_id]
		else:
			self.dataframe = self.dataframe[self.dataframe['UniqueID'] == user_id]
			self.dataframe.reset_index()

	# Финальные визуализации
	def graph_data(self, data, filename):
		data['Power'] = data.loc[:, 'Accdata'].apply(self.calc_power)
		data = data.loc[:, ['Geopos', 'Power', 'UniqueID', 'TrackID', 'IsTruth']]
		#data.to_csv('svd.csv', index=False)
		data = data.values
		self.mapgen.get_map(data, filename)

	def prod_get_graph(self, limit, filename, radius=0.01, k=6):
		data = self.limit_check(self.dataframe, limit)
		data = self.k_nearest_check(data, radius=radius, k=k)
		self.graph_data(data, filename)


if __name__ == '__main__':
	d = DataWorker()
	r = RandomDataGenerator()
	d.append_batch(r.create_line_data(np.array([55.517298, 36.993981]), np.array([55.667247, 37.426248])))
	d.append_batch(r.create_line_data(np.array([55.608965, 49.300274]), np.array([55.623160, 49.260022]), trid='Kazan'))
	d.append_batch(r.create_line_data(np.array([55.692110, 49.192970]), np.array([55.623160, 49.260022]), trid='Kazan'))	
	d.save_data(filename='data.csv', inplace=True)