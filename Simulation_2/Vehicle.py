# CHANGE LOG
# Date       Name       Changes
# -----------------------------------------------------------------------------
# 11/01/16   Libbey     File creation
# 11/13/16   Cason      Comments & add < full charge request option
# -----------------------------------------------------------------------------
# Vehicle object to store all data relevant to a specific vehicle
# -----------------------------------------------------------------------------

class Vehicle:

	def __init__(self, packCapacity, arrivalTime, projDeparture, requestedCharge, maxChargeRate, initialSOC, time):

		# constants
		self.packCapacity = packCapacity        # total battery capacity (kWh)
		self.arrivalTime = arrivalTime          # arrival time
		self.projDeparture = projDeparture      # projected departure time
		self.requestedCharge = requestedCharge  # requested final SOC (kWh)
		self.maxChargeRate = maxChargeRate      # max charge rate of car (kW)
		self.finalCharge = 0                    # final state of charge (kWh)

		# arrays
		self.stateOfCharge = [initialSOC] * len(time)	# current charge of car
