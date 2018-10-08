# CHANGE LOG
# Date       Name       Changes
# -------------------------------------------------------------------------
# 10/17/16   Libbey     File creation, moved rate calculation to here
# -------------------------------------------------------------------------

from Car import Car

class Station:

    def __init__(self):
        self.cars = []

    def add_car(self, car):
        """Add a car to a parking spot at charging station."""
        self.cars.append(car)
        car.parkingSpot = self.cars.index(car)

    def remove_car(self, car):
        """Remove a car from a parking spot at charging station."""
        try:
            self.cars.remove(car)
        except:
            pass

    def display_parking_spots(self):
        """Display each car parked at the station and their important data fields"""
        print('Charging Station Parking Configuration')
        # TODO: Way to nicely display each car & its relevant info/data fields

        for car in self.cars:
            print('Spot %d: ' % car.parkingSpot)
            print('  Car ID:',car.parkingSpot)
            print('\tInitial SOC:\t ',car.stateOfCharge)
            print('\tBattery Capacity:',car.batteryCapacity)
            print('\tMax Charge Rate: ',car.maxChargeRate)
            print()

    def calc_rate_options(self, car):
        """Calculate the fast, med, and slow charging rates for customer based on car parameters
           and how long they plan to spend there."""

        car = self.cars[car.parkingSpot]
        car.timeParked = float(input('Driver, enter amount of time vehicle will be parked (hrs): '))

        PRICE = 0.15 # Price per kWh
        STATION_POWER = 13.2 # Max power of station in kW

        car.stateOfCharge = car.stateOfCharge / 100. # convert stateOfCharge percentage into number 0-1
        maxPercentOutcome = ((car.maxChargeRate * car.timeParked) / car.batteryCapacity) + car.stateOfCharge

        if maxPercentOutcome > 1:   # Get High Percentage
            highPercentOutcome = 1
        else:
            highPercentOutcome = maxPercentOutcome

        midPercentOutcome = ((2.0/3) * (highPercentOutcome - car.stateOfCharge)) + car.stateOfCharge   # Get Mid Percentage
        lowPercentOutcome = ((1.0/3) * (highPercentOutcome - car.stateOfCharge)) + car.stateOfCharge   # Get Low Percentage

        rateHigh = ((highPercentOutcome - car.stateOfCharge) * car.batteryCapacity) / car.timeParked    # Rate to charge to high (kW)
        rateMid  = ((midPercentOutcome - car.stateOfCharge) * car.batteryCapacity) / car.timeParked     # Rate to charge to mid
        rateLow  = ((lowPercentOutcome - car.stateOfCharge) * car.batteryCapacity) / car.timeParked     # Rate to charge to mid

        # Assume customer is paying $1/kW

        priceHigh = rateHigh * car.timeParked * PRICE        # Price for high rate of charge
        priceMid = rateMid * car.timeParked * PRICE          # Price for mid rate of charge
        priceLow = rateLow * car.timeParked * PRICE          # Price for low rate of charge

        print('High - Final Percentage: %.2f' %  (highPercentOutcome*100),'%', sep="")     # Print High Button
        print('       Rate: %.2f' % rateHigh, ' kW', sep="")
        print('Cost: $', "%.2f" % priceHigh)
        print()
        print('Mid - Final Percentage: %.2f' % (midPercentOutcome*100),'%', sep="")        # Print Mid Button
        print('      Rate: %.2f' % rateMid, ' kW', sep="")
        print('Cost: $', "%.2f" % priceMid)
        print()
        print('Low - Final Percentage: %.2f' % (lowPercentOutcome*100),'%', sep="")        # Print Low Button
        print('      Rate: %.2f' % rateLow, ' kW', sep="")
        print('Cost: $', "%.2f" % priceLow)

        while(1):
            chosen = input('Choose "high" "med" or "low" rate: ')

            if chosen == "high":
                car.chargeRate = rateHigh
                car.chargePrice = priceHigh
                break
            elif chosen == "med":
                car.chargeRate = rateMid
                car.chargePrice = priceMid
                break
            elif chosen == "low":
                car.chargeRate = rateLow
                car.chargePrice = priceLow
                break
            else:
                print('Invalid option - choose a rate')
