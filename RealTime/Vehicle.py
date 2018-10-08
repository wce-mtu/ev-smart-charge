# CHANGE LOG
# Date       Name       Changes
# -----------------------------------------------------------------------------
# 11/01/16   Libbey     File creation
# 11/13/16   Cason      Comments & add < full charge request option
# -----------------------------------------------------------------------------
# Vehicle object to store all data relevant to a specific vehicle
# -----------------------------------------------------------------------------

class Vehicle:
    def __init__(self, cmd):
        self.packCapacity = float(cmd[2]) #Capacity of the car's battery
        self.maxChargeRate = float(cmd[3]) #Max charge rate of the car
        self.SOC = float(cmd[4]) #The current state of charge of the car
        self.fullnotified = 0; #Change to 1 to stop notification
        self.chargenotified = 0; #Change to 1 to stop notification
        
        # Device Registration ID from app - if applicable
        try:
            self.username = cmd[7] 
        except:
            self.username = "None"
            
        hours, mins = str(cmd[5]).split(":")

        hours = int(hours)
        hours = (hours-8)*12
        mins = int(mins)
        mins = mins/5

        ret = hours+mins
        tempDepHours, tempDepMins = str(cmd[5]).split(":")
        self.depHours = int(tempDepHours)
        self.depMins = int(tempDepMins)
        self.projDeparture = ret #Expected departure time
        self.requestedCharge = int(cmd[6]) #Requested SOC from driver

        self.priority = 0
        self.SOCd = self.SOC
