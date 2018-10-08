# CHANGE LOG
# Date       Name       Changes
# -------------------------------------------------------------------------
# 10/17/16   Libbey     File creation
# -------------------------------------------------------------------------

class Car:
    'Base class for all cars parking at a charging station'

    def __init__(self, stateOfCharge, batteryCapacity, maxChargeRate):
        self.stateOfCharge = stateOfCharge
        self.batteryCapacity = batteryCapacity
        self.maxChargeRate = maxChargeRate
