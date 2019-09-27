from plyer import accelerometer
from plyer import gps
from kivy.clock import Clock, mainthread

class Accelerometer():
	def __init__(self, debug=False):
		self.debug = debug

	def get_state(self):
		try:
			output = accelerometer.acceleration()[:3]

			if self.debug:
				print(output)

			if output == (None, None, None):
				output = (0, 0, 0)

			return output
		except Exception as e:
			print('Accelerometer Error')

class GPSTracker():
	def __init__(self):
		self.active = True
		try:
			gps.configure(on_location=self.on_location, on_status=self.on_status)
		except Exception as e:
			print('GPS Error')
			self.active = False

	def check_active(self):
		return self.active

	@mainthread
	def on_location(self, **kwargs):
		self.gps_location = list(kwargs.items)

	@mainthread
	def on_status(self, stype, status):
		self.gps_status = (stype, status)

	def activate(self, minTime=1000, minDistance=0):
		gps.start(minTime, minDistance)

	def deactivate(self):
		gps.stop()
