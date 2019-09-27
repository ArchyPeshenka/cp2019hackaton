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
			response = requests.post(self.server, data={'String': standard_protocol})
			con_is_available = True
		except requests.exceptions.ConnectionsError:
			con_is_available = False

		return con_is_available

	def add_to_buffer(self, acc, geo):
		"""
		PostId: Int | (from time.time()) Unique id of every part of data
		GeoData: List | (from geo) Geo position of unique part of data (pos1, pos2)
		AccData: List | (from acc) Data from accelerometer of unique part of data (x, y, z)

		"""
		self.databuffer.append({'PostId': time.time(), 'GeoData': geo, 'AccData': acc})

		return True

	def get_from_buffer(self):

		#Len (databuffer) MUST be > 1!
		if len(self.databuffer) > 1:
			return self.databuffer.pop(0)
		else:
			print('Databuffer len < 0!')

	def post_data(self, data):
		response = requests.post(self.server, data=data)
		return response
