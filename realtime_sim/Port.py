# CHANGE LOG
# Date       Name       Changes
# -----------------------------------------------------------------------------
# 11/01/16   Libbey     File creation
# 11/13/16   Cason      Comments
# -----------------------------------------------------------------------------
# Port object to store data for a specific port
# -----------------------------------------------------------------------------

class Port:

	def __init__(self, vehicles, max_power, time):
		# contained objects
		self.vehicles = vehicles				# array of vehicles visiting 
		
		# constants
		self.max_power = max_power				# max charge rate of port (kW)
		
		# arrays
		self.priority = [0] * len(time)			# priority of current vehicle
		self.delivered_power = [0] * len(time)	# actual port delivered power