import requests
import time
class DataDeploy():

	def __init__(self, server, app_id=0):
		self.app_id = 0
		self.server = server
		self.databuffer = []

	def check_connection(self, standard_protocol="Check-Con"):
		con_is_available = False
		try:
			#print('Try to check connection')
			response = requests.get(self.server + '/chk')

			con_is_available = True
		except Exception as e:
			#print(e)
			con_is_available = False

		return con_is_available

	def get_buffer_len(self):
		return len(self.databuffer)

	def get_unique_id(self):
		return 0

	def get_track_id(self):
		return 0
	def add_to_buffer(self, acc, geo):
		"""
		PostId: Int | (from time.time()) Unique id of every part of data
		GeoData: List | (from geo) Geo position of unique part of data (pos1, pos2)
		AccData: List | (from acc) Data from accelerometer of unique part of data (x, y, z)

		"""
		self.databuffer.append({'UniqueID': self.get_unique_id(), 'TrackID': self.get_track_id(), 'Timestamp': time.time(), 'Geopos': geo, 'Accdata': acc})

		return True

	def get_from_buffer(self, batch_size):

		data = []
		for i in range(0, batch_size):
			data.append(self.databuffer.pop(0))

		return data

	def post_data(self, data):
		response = requests.post(self.server, data=data)
		return response

	def post_from_buffer(self, batch_size=1000):
		self.post_data({'data': str(self.get_from_buffer(batch_size))})

