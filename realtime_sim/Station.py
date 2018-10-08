# CHANGE LOG
# Date       Name       Changes
# -----------------------------------------------------------------------------
# 11/01/16   Libbey     File creation
# 11/13/16   Cason      Comments
# -----------------------------------------------------------------------------
# Station object to store all data for station
# -----------------------------------------------------------------------------

class Station:

	def __init__(self, ports, total_power, time):
		# contained objects
		self.ports = ports					   # array of ports in station
		
		# constants
		self.total_power = total_power		   # max station delivered power

		# arrays
		self.delivered_power = [0] * len(time) # actual station delivered power
		self.sum_priorities = [0] * len(time)  # total priorities of ports