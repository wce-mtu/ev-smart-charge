# CHANGE LOG
# Date       Name       Changes
# -------------------------------------------------------------------------
# 10/17/16   Libbey     Added options, continuous simulation
# -------------------------------------------------------------------------

from Car import *
from Station import *

def main():
    #Constants for ease of use/test
    TIMEPARKED_CONST = 5
    SOC_CONST = 44
    BATCAPACITY_CONST = 60
    MAXCHARGERATE_CONST = 10

    print('Ford EV Smart Charge - Charging Station Simulation')
    chargingStation = Station()

    while(1):
        print('What would you like to do?\n' ,
              '1. Add car to parking spot on station\n' ,
              '2. Remove car from parking spot on station\n',
              '3. Display current parking spot configuration\n'
              '...\n',
              '9. Quit simulation', sep="")
        option = int(input(""))

        if option == 1:
            if len(chargingStation.cars) >= 6:
                print('All parking spots are currently full.\n')
            else:
                SOC = float(input('Enter current state of charge of battery (%): '))
                batCapacity = float(input('Enter max capacity of battery (kWh): '))
                maxChargeRate = float(input('Enter max rate of charge battery can handle (kW): '))


            car = Car(SOC, batCapacity, maxChargeRate)
            chargingStation.add_car(car)
            print('Car\'s parking spot is', car.parkingSpot)
            chargingStation.calc_rate_options(car)

        elif option == 2:
            chargingStation.remove_car(car)

        elif option == 3:
            chargingStation.display_parking_spots()

        elif option == 9:
            return

if __name__ == '__main__':
    main()
