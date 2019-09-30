import random
import time
import numpy as np 
import math

class RandomDataGenerator():

	def __init__(self):
		pass

	def get_samples(self, x):
		d = []
		for i in range(0, x):
			d.append({'UniqueID': str(random.choice([1, 2, 3, 4, 5])), 'TrackID': str(random.choice([1, 2, 3])), 'Timestamp': time.time(), 'Geopos': str([random.random() * 20 for i in range(0, 2)]), 'Accdata': str([random.random() * 20 for i in range(0, 3)])})
		return d

	def create_line_data(self, v1, v2, n=100, randmod=1, trid=1):
		d = []
		for i in range(0, n):
			x = np.min(np.array([v1[0], v2[0]])) + random.random() * randmod * (np.max(np.array([v1[0], v2[0]])) - np.min(np.array([v1[0], v2[0]])))
			#y = x * v[1] / v[0]
			
			y = ( (-1) * (v1[1] - v2[1]) * x - v1[0]*v2[1] + v2[0]*v1[1]) / (v2[0] - v1[0])
			d.append({'UniqueID': str(random.choice([1, 2, 3, 4, 5])), 'TrackID': str(trid), 'Timestamp': time.time(), 'Geopos': str([x, y]), 'Accdata': str([random.random() * 20, random.random() * 2, random.random() * 2])})
		return d		
