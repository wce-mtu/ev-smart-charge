# CHANGE LOG
# Date       Name       Changes
# -----------------------------------------------------------------------------
# 11/01/16   Libbey     File creation
# 11/13/16   Cason      Comments
# -----------------------------------------------------------------------------
# Station object to store all data for station
# -----------------------------------------------------------------------------

class Station:

    def __init__(self):
		# contained objects
        self.ports = [None]*4					   # array of ports in station
        self.sum_priorities = 0

		# constants
        self.total_power = 30    	   # max station delivered power
        self.max_power = 11.5            # max port delivered power

        # arrays
        # actual station delivered power
        # total priorities of ports