# CHANGE LOG
# Date       Name       Changes
# -----------------------------------------------------------------------------
# 11/01/16   Libbey     File creation
# 11/13/16   Cason      Fixed all of the problems - removed broken debug
# 11/13/16   Cason      Commented everything & made option for < full charge
#                       Now prints out if car reaches desired charge or not
# 11/27/16   Libbey     Socket connection with Android application
# -----------------------------------------------------------------------------

from Vehicle import *
from Port import *
from Station import *

import numpy as np
import matplotlib.pyplot as plt
from socket import *
from sys import *
from threading import *
from struct import *


#ENABLE/DISABLE FLAGS
ADD_CAR = 0
DEBUG = 0


# -----------------------------------------------------------------------------
# Func: Calculates the charge rate in kilowatts for each of the cars parked
#       at the station, and the total station power.
# -----------------------------------------------------------------------------
def stationAlg(station, time, pause_time):

    # for every time sampling point
    for x in range(len(time)):

        if(ADD_CAR and time[x] == pause_time):
            # Add a car to 3rd car spot in Port 3
            addCar(station, pause_time, time)

        # go through every vehicle in every port to get priorities
        for port in station.ports:
            for vehicle in port.vehicles:

                # if the vehicle is currently parked
                if(vehicle != None and vehicle.arrivalTime <= time[x] and vehicle.projDeparture > time[x]):

                    # calculate expected remaining time
                    hrs_remaining = vehicle.projDeparture - time[x]

                    # calculate port's priority if not fully charged
                    if((vehicle.requestedCharge-vehicle.stateOfCharge[x]) > 0):
                        port.priority[x] = (vehicle.requestedCharge - vehicle.stateOfCharge[x]) / (vehicle.maxChargeRate * hrs_remaining)

                    # add current vehicle priority to the current total priority
                    station.sum_priorities[x] += port.priority[x]

        # go through every vehicle in every port to get port's delivered power (kW)
        for port in station.ports:
            for vehicle in port.vehicles:

                # if the vehicle is currently parked
                if(vehicle != None and vehicle.arrivalTime <= time[x] and vehicle.projDeparture > time[x]):

                    # calculate port's delivered power if priority isn't zero
                    if(port.priority[x] > 0):

                        # if calculated rate is more than vehicle's max, charge at vehicle's max
                        if((port.priority[x] / station.sum_priorities[x]) * station.total_power) > vehicle.maxChargeRate:
                            port.delivered_power[x] = vehicle.maxChargeRate
                        # otherwise, use calculated rate
                        else:
                            port.delivered_power[x] = (port.priority[x] / station.sum_priorities[x]) * station.total_power

                        # if calculated rate is more than port's max, charge at port's max
                        if (port.delivered_power[x] > port.max_power):
                            port.delivered_power[x] = port.max_power

                    # add current port's delivered power to the current station total power
                    station.delivered_power[x] += port.delivered_power[x]

                    # set state of charge as final value
                    vehicle.finalCharge = vehicle.stateOfCharge[x]

                    # if state of charge at next time interval is more than 100%, set SOC to 100%
                    if(x+1 < len(time)):
                        if(vehicle.stateOfCharge[x]+(port.delivered_power[x]*0.25) > vehicle.packCapacity):
                            vehicle.stateOfCharge[x+1] = vehicle.packCapacity
                        # otherwise, get the state of charge for the next point in time
                        else:
                            vehicle.stateOfCharge[x+1] = vehicle.stateOfCharge[x]+(port.delivered_power[x]*0.25)


# -----------------------------------------------------------------------------
# Func: Adds a car to the simulation based on data fields gathered from
#       Android application. Currently only "works" for Port 3, Car 2
# -----------------------------------------------------------------------------
def addCar(station, arrive_time, time):
    # DEFAULT VALUES FROM CAR
    packCapacity = 30 #kWh
    maxChargeRate = 16 #kW
    initialSOC = 5 #kWh

    # Bind socket & grab info from app, print info
    print("Collecting data from phone application...")
    data = gather_app_data()

    print("Data = ", data)
    departure_time = data[0] + data[1]
    requestedCharge = data[3] * packCapacity

    print("Driver arrives at %.2f and requests to leave at %.2f with charge of %.2f kWh\n"
          % (arrive_time, departure_time, requestedCharge),
          "Car has initial charge of %.2f kWh, pack capacity of %.2f kWh, and max charge rate of %.2f kW "
          % (initialSOC, packCapacity, maxChargeRate), sep="")


    # Put vehicle in last spot of port 3
    station.ports[3].vehicles[2] = Vehicle(packCapacity, arrive_time, departure_time,
                                           requestedCharge, maxChargeRate, initialSOC, time)

    return

# -----------------------------------------------------------------------------
# Func: Listens on socket for connection from Android app and takes in data
#       fields. Formats fields for easy of use in rest of program.
# -----------------------------------------------------------------------------
def gather_app_data():
    HOST = ''
    PORT = 8888

    s = socket(AF_INET, SOCK_STREAM)
    print('Socket created')

    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except error as msg:
        print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        exit()

    print ('Socket bind complete')

    #Start listening on socket
    s.listen(10)
    print ('Socket now listening')

    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))

    data = conn.recv(1024).decode('UTF-8')
    if not data:
        return
    data = data.split(" ")

    conn.close()
    s.close()

    # Format data correctly for further manipulation
    data[0] = float(data[0]) #hour
    data[1] = float(data[1]) #mins
    data[3] = float(data[3]) #reqChargePct

    if(data[2] == "PM"):
        data[0] = float(data[0])+12
    data[1] = data[1]/60.
    data[3] = data[3]/100.

    return data

# -----------------------------------------------------------------------------
# Func: Main method
# -----------------------------------------------------------------------------
def main():
    # These variables can be changed to fit simulation needs
    STATION_TOTAL_POWER = 40 # kW
    PORT_MAX_POWER = 30 #kW
    STATION_PORTS = 4
    x = 0

    time = np.arange(6., 20., 0.25) # time sampling array
    total_power_line = [STATION_TOTAL_POWER] * len(time)

    pause_time = 0
    if ADD_CAR:
        pause_time = float(input("Enter time to pause simulation (6 - 20): "))
        print("Pause time is", pause_time )


    # ------------ initialize the day of vehicles for simulation ------------ #

    # init vehicle arrays (packCapacity, arrival, departure, requestedCharge, maxChargeRate, initialSOC, time)
    vehicles_port0 = [Vehicle(40., 7.5,   11.5, 32., 16., 20., time),   # 7:30 am - 11:30 am
                      Vehicle(50., 13.25, 17.,  40., 16., 15., time),   # 1:15 pm - 5 pm
                      Vehicle(23., 17.5,  18.,  15., 50., 14., time)]   # 5:30 pm - 6 pm

    vehicles_port1 = [Vehicle(35., 7.75,  14.5, 30., 16., 10., time),   # 7:45 am  - 2:30 pm
                      Vehicle(40., 14.75, 17.,  25., 16., 20., time),   # 2:45 pm - 5 pm
                      Vehicle(50., 17.25, 18.,  40., 50., 30., time)]   # 5:15 pm  - 6 pm

    vehicles_port2 = [Vehicle(40., 7.5,  11.5, 32., 16., 30., time),    # 7:30 am - 11:30 am
                      Vehicle(50., 11.5, 17.,  40., 16., 2., time),     # 11:30 am - 5 pm
                      Vehicle(50., 17.5, 18.,  40., 50., 37., time)]    # 5:30 pm - 6 pm

    vehicles_port3 = [Vehicle(50., 7.75,  13.5, 50., 20., 34., time),   # 7:45 am - 1:30 pm
                      Vehicle(40., 13.5,  17.,  30., 19., 20., time),   # 1:30 pm - 5 pm
                      #Vehicle(30., 17.5 , 18.,  15., 30., 10., time)]  # 5:30 pm - 6 pm
                      None]     # Where vehicle from app interaction goes

    # init ports
    station_ports = [Port(vehicles_port0, PORT_MAX_POWER, time),
                     Port(vehicles_port1, PORT_MAX_POWER, time),
                     Port(vehicles_port2, PORT_MAX_POWER, time),
                     Port(vehicles_port3, PORT_MAX_POWER, time)]

    # init station
    station = Station(station_ports, STATION_TOTAL_POWER, time)

    # ----------------------------------------------------------------------- #

    # run the algorithm
    stationAlg(station, time, pause_time)

    # print out if vehicles were satisfied
    y=0
    for port in station.ports:
        print("At Port %d:" % y)
        x=0
        y+=1
        for vehicle in port.vehicles:
            if (vehicle != None):
                if (vehicle.finalCharge >= vehicle.requestedCharge):
                    print("   Vehicle ", x, " - SATISFIED: %.2f" % vehicle.finalCharge, "/%.2f kWh" % vehicle.requestedCharge, sep="", end="\n")
                else:
                    print("   Vehicle ", x, " - UNSATISFIED: %.2f" % vehicle.finalCharge, "/%.2f kWh" % vehicle.requestedCharge, sep="", end="\n")
            x+=1

    # ---------------------- plot all simulation data ----------------------- #


    plt.figure(1)

    # subplot for port 0 delivered power
    plt.subplot(2, 2, 1)
    plt.plot(time, station.ports[0].delivered_power, 'bo-')
    plt.xlabel('Time of Day (6 am - 8 pm)')
    plt.ylabel('Plug Power (kW)')
    plt.title('Port 0 Delivered Power')
    plt.grid(True)

    # subplot for port 1 delivered power
    plt.subplot(2, 2, 2)
    plt.plot(time, station.ports[1].delivered_power, 'bo-')
    plt.xlabel('Time of Day (6 am - 8 pm)')
    plt.ylabel('Plug Power (kW)')
    plt.title('Port 1 Delivered Power')
    plt.grid(True)

    # subplot for port 2 delivered power
    plt.subplot(2, 2, 3)
    plt.plot(time, station.ports[2].delivered_power, 'bo-')
    plt.xlabel('Time of Day (6 am - 8 pm)')
    plt.ylabel('Plug Power (kW)')
    plt.title('Port 2 Delivered Power')
    plt.grid(True)

    # subplot for port 3 delivered power
    plt.subplot(2, 2, 4)
    plt.plot(time, station.ports[3].delivered_power, 'bo-')
    plt.xlabel('Time of Day (6 am - 8 pm)')
    plt.ylabel('Plug Power (kW)')
    plt.title('Port 3 Delivered Power')
    plt.grid(True)

    # plot of station total delivered power
    plt.figure(2)
    plt.plot(time, station.delivered_power, 'bo-', time, total_power_line, 'r-')
    plt.ylim(0,station.total_power+10)
    plt.annotate('Total Station Power Available', xy=(10, station.total_power), xytext=(10.5, station.total_power+5),
            arrowprops=dict(facecolor='black', width=1, headwidth=5, headlength=5),
            )
    plt.xlabel('Time of Day (6 am - 8 pm)')
    plt.ylabel('Station Power (kW)')
    plt.title('Station Delivered Power')
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    main()