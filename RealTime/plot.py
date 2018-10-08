"""
This example showcases a live plotting animation.
"""

import numpy as np
import numpy.ma as ma
from random import *
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as dates
import os
from matplotlib import style
from datetime import datetime
import matplotlib.lines as mlines
from time import *
from threading import Thread
from socketserver import *
from socket import *
from sys import *
from Vehicle import *
from Station import *
from queue import Queue
import io
import re
import select
import threading
from firebase import firebase
from pyfcm import *

class Event(object):         
    def __init__(self, time, cmd):
        self.time = time
        self.cmd = cmd

global running
running = False

global t
t = 0

station = Station()

# - CREATE FIREBASE CONNECTIONS - #

# Main firebase
fire = firebase.FirebaseApplication('https://ev-charge-8133f.firebaseio.com/', None)

# Initialize Push service
FB_KEY = "AAAA7L2MSt0:APA91bEihBBAZZLVU8qOjsSZzAnMMSnZ64RjWTuXAnxY6IzaBDDLDD9u_Te7BQGawX6fD106DIKHuEQtXKra5Go0ksYIym2lu7zfo5mQV4TFOA3NaW01RvY_-S1-3HOrQbquLoM7MGwJ"
push_service = FCMNotification(api_key=FB_KEY)

# Empty database of residual commands
try:
    diction = fire.delete('/add', None)
except:
    """ nothing in database commands """


# - CREATION OF SOCKETS - #
HOME = ''

# - CREATE send.py TERMINAL SOCKET - #
PORT = 80
sim_s = socket(AF_INET, SOCK_STREAM)
print('Terminal socket created.')

# Bind socket to local host and port
try:
    sim_s.bind((HOME, PORT))
except error as msg:
    print ('Terminal bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    exit()

print ('Socket bind to terminal complete.')

# Start listening on socket
sim_s.listen(10)
print ('Terminal socket listening')

# Wait to accept a connection to send.py - blocking call
term_conn, addr = sim_s.accept()
print ('Connected with ' + addr[0] + ':' + str(addr[1]))
term_conn.setblocking(0)

# List of threads
threads = []

# - SET INDEX 0 - #
i = 0

# Get 8am variable to use on axes
str_8am = "8:00"
tim_8am = dates.date2num(datetime.strptime(str_8am, '%H:%M'))

# - BEGIN PLOT - #
style.use('fivethirtyeight')

fig = plt.figure()

ax1 = fig.add_subplot(2,2,1)
ax1.set_title('Port 0 Delivered Power')
ax2 = fig.add_subplot(2,2,2)
ax2.set_title('Port 1 Delivered Power')
ax3 = fig.add_subplot(2,2,3)
ax3.set_title('Port 2 Delivered Power')
ax4 = fig.add_subplot(2,2,4)
ax4.set_title('Port 3 Delivered Power')
fig.subplots_adjust(hspace=0.33)

fig2 = plt.figure()
ax5 = fig2.add_subplot(1,1,1)
ax5.set_title('Total Station Delivered Power')

hfmt = dates.DateFormatter('%H:%M')

ax1.set_xlabel("Time")
ax1.set_ylabel("Power (kW)")
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(hfmt)
ax1.xaxis.set_major_locator(dates.AutoDateLocator())


ax2.set_xlabel("Time")
ax2.set_ylabel("Power (kW)")
ax2.xaxis_date()
ax2.xaxis.set_major_formatter(hfmt)
ax2.xaxis.set_major_locator(dates.AutoDateLocator())


ax3.set_xlabel("Time")
ax3.set_ylabel("Power (kW)")
ax3.xaxis_date()
ax3.xaxis.set_major_formatter(hfmt)
ax3.xaxis.set_major_locator(dates.AutoDateLocator())

ax4.set_xlabel("Time")
ax4.set_ylabel("Power (kW)")
ax4.xaxis_date()
ax4.xaxis.set_major_formatter(hfmt)
ax4.xaxis.set_major_locator(dates.AutoDateLocator())


ax5.set_xlabel("Time")
ax5.set_ylabel("Power (kW)")
ax5.xaxis_date()
ax5.xaxis.set_major_formatter(hfmt)
ax5.xaxis.set_major_locator(dates.AutoDateLocator())



def endSim():
    print("The simulation has ended")

def processCmd(cmd):
    global t, running, xs, ys0, ys1, ys2, ys3, ys4, ysd0, ysd1, ysd2, ysd3, ysd4

    #Parse command into parts
    command = cmd.split()

    print(command[0])

    if command[0] == 'pause':
        #pause
        running = False
    if command[0] == 'play':
        #play
        running = True
    if command[0] == 'add':
        #add [port] [capacity] [maxcharge] [SOC] [deptime] [reqSOC] [userid]
        station.ports[int(command[1])] = Vehicle(command)
        print('Port [', command[1] ,'] Vehicle added', sep="")
    if command[0] == 'list':
        print("")
        for i,port in enumerate(station.ports):
            if port:
                list_mins = int(port.projDeparture*5)
                list_hours = int(list_mins/60)
                list_mins = int(list_mins-(60*list_hours))
                list_hours = list_hours+8 # simulation starts at 8 am, each sec is simulating 5 mins
                if(list_mins < 10):
                    list_format_zero = "0"
                else:
                    list_format_zero  = ""
                list_time_string = str(list_hours)+":"+list_format_zero+str(list_mins)
                print('Port [', i ,'] Vehicle:',
                    '\n  Pack Capacity: ', port.packCapacity, ' kWh'
                    '\n  Max Charge Rate: ', port.maxChargeRate, ' kW'
                    '\n  Departure Time: ', list_time_string,
                    '\n  Current SOC: %.2f' % port.SOC, '%'
                    '\n  Requested SOC: ', port.requestedCharge, '%', sep="")
            else:
                print('Port [', i ,'] EMPTY', sep="")
            print("")

    if command[0] == 'sub':
        #sub [port]
        station.ports[int(command[1])] = None
    if command[0] == 'modtime':
        #modtime [port] [deptime]
        mod_hours, mod_mins = command[2].split(":")
        mod_hours = int(mod_hours)
        mod_hours = (mod_hours-8)*12
        mod_mins = int(mod_mins)
        mod_mins = mod_mins/5

        mod_ret = mod_hours + mod_mins
        print(str(mod_ret))

        station.ports[int(command[1])].projDeparture = mod_ret
        print('Port [', command[1] ,'] Vehicle Departure time changed to ', command[2] , sep="")
    if command[0] == 'modcharge':
        #modcharge [port] [reqSOC]
        station.ports[int(command[1])].requestedCharge = int(command[2])
        print('Port [', command[1] ,'] Vehicle Requested SOC changed to ', command[2] , sep="")
    if command[0] == 'reset':
        xs = []
        ys0 = []
        ys1 = []
        ys2 = []
        ys3 = []
        ys4 = []
        ysd0 = []
        ysd1 = []
        ysd2 = []
        ysd3 = []
        ysd4 = []
        station.ports[0] = None
        station.ports[1] = None
        station.ports[2] = None
        station.ports[3] = None
        running = False
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax5.clear()
        ax1.set_title('Port 0 Delivered Power')
        ax2.set_title('Port 1 Delivered Power')
        ax3.set_title('Port 2 Delivered Power')
        ax4.set_title('Port 3 Delivered Power')
        fig.subplots_adjust(hspace=0.33)
        ax5.set_title('Total Station Delivered Power')
        hfmt = dates.DateFormatter('%H:%M')
        
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Power (kW)")
        ax1.xaxis_date()
        ax1.xaxis_date()
        ax1.xaxis.set_major_formatter(hfmt)
        ax1.xaxis.set_major_locator(dates.AutoDateLocator())

        ax2.set_xlabel("Time")
        ax2.set_ylabel("Power (kW)")
        ax2.xaxis_date()
        ax2.xaxis.set_major_formatter(hfmt)
        ax2.xaxis.set_major_locator(dates.AutoDateLocator())

        ax3.set_xlabel("Time")
        ax3.set_ylabel("Power (kW)")
        ax3.xaxis_date()
        ax3.xaxis.set_major_formatter(hfmt)
        ax3.xaxis.set_major_locator(dates.AutoDateLocator())

        ax4.set_xlabel("Time")
        ax4.set_ylabel("Power (kW)")
        ax4.xaxis_date()
        ax4.xaxis.set_major_formatter(hfmt)
        ax4.xaxis.set_major_locator(dates.AutoDateLocator())

        ax5.set_xlab2el("Time")
        ax5.set_ylabel("Power (kW)")
        ax5.xaxis_date()
        ax5.xaxis.set_major_formatter(hfmt)
        ax5.xaxis.set_major_locator(dates.AutoDateLocator())

    if command[0] == "runScript":
        # runScript [scriptFilePath]
        doScriptCalc(command[1])



def doScriptCalc(scriptFile):

    # Setup the Station Parameters (Currently using defaults)
    # Total Power
    # Max port power
    # Number of Ports
    avgNumCars = 1
    carsStd = 0.5 
    startAvg = 8 
    startStd = 0.5 
    depatureAvg = 8 
    departureStd = 0.5 
    avgTimeBtwnCars = 0.15 
    timeBtwnCarsStd = 0.5
    tempNumPorts = 4
    days = 100
    averageHourlySmartRate = [0] * 288
    dailyAverageHourlySmartRate = [0] * 288
    averageHourlyDumbRate = [0] * 288
    dailyAverageHourlyDumbRate = [0] * 288

    # Generate a seed that can be output for repeatability
    seed()
    initSeed = int(random()*maxsize)
    seed(initSeed)

    # Setup the cost of power
    costOfPower = []

    for index in np.arange(24):
        costOfPower.append(0.13)

    # Open the script file for parsing
    f = open(scriptFile, "r")

    for lines in f:
        print(lines)
        lineArray = lines.split(" ")

        if (lineArray[0] == "simDays"):
            days = int(lineArray[2])

        if (lineArray[0] == "seed"):
            initSeed = int(lineArray[2])
            seed(initSeed)

        if (lineArray[0] == "numPorts"):
            station.ports = [None] * int(lineArray[2])
            tempNumPorts = int(lineArray[2])

        if (lineArray[0] == "maxStationPower"):
            station.total_power = float(lineArray[2])

        if (lineArray[0] == "maxPortPower"):
            station.max_power = float(lineArray[2])

        if (lineArray[0] == "portParams"):

            avgNumCars = lineArray[1] 
            carsStd = lineArray[2] 
            startAvg = lineArray[3]
            startStd = lineArray[4] 
            depatureAvg = lineArray[5] 
            departureStd = lineArray[6] 
            avgTimeBtwnCars = lineArray[7] 
            timeBtwnCarsStd = lineArray[8]

        if (lineArray[0] == "costFile"):
            costFile = str(lineArray[2]).rstrip('\n')
            print(costFile)
            try:
                costFileStream = open(costFile)
                fileString = costFileStream.read()
                costFileVals = fileString.split(",")
                for val in range(24):
                    costOfPower[val] = float(costFileVals[val]) / 100.0
            except OSError as err:
                print(str(err))

        if (lineArray[0] == "chanceOfPHEV"):
                chanceOfPHEV = float(lineArray[2])


    f.close()

    # Setup the array to hold all of the total daily powers
    dailyPower = [0]*days
    dailyPowerD = [0]*days
    dailyCost = [0]*days
    dailyCostD = [0]*days  

    # For each day in the simulation
    for j in np.arange(days):

        # Initialize all daily variables to zero
        totalDailyCharge = 0
        totalDailyChargeD = 0
        totalDailyCost = 0
        totalDailyCostD = 0

        # Run the simulation for the day (Starts at Midnight)
        t_hours = 0
        t_mins = 0
        t = 0
        rate = []
        dumb_rate = []
        for k in range(tempNumPorts):
            rate.append(0)
            dumb_rate.append(0)
        sum_rates = 0
        sum_dumb_rates = 0
        station.sum_priorities = 0
        eventCounter = 0
        events = []*0
        numberOfCars = 0
        arrivalTime = 0
        duration = 9

        for i in range(tempNumPorts):
            
            # Get the number of cars during the day
            numberOfCars = int(round(gauss(float(avgNumCars), float(carsStd))))

            # Get the time first vehicle will arrive
            arrivalTime = gauss(float(startAvg), float(startStd))

            # Get the duration the port will be occupied throughout the day
            duration = gauss(float(depatureAvg), float(departureStd))

            # Create the add car events that happen throughout the day
            if (numberOfCars > 0):
                durationMaxDelta = 1.0

                for l in range(numberOfCars):
                    
                    durationRand = random()
                    tempRand = random()

                    # Get the duration the current vehicle will be there
                    actualDuration = 0
                    if (durationRand < 0.5):
                        actualDuration = (duration / float(numberOfCars)) - (durationMaxDelta * tempRand)
                    else:
                        actualDuration = (duration / float(numberOfCars)) + (durationMaxDelta * tempRand)

                    # Set the current state of charge of the vehicle
                    currSOC = int(100-(50*random()))

                    # Calculate the departure time and convert from decimal hours to a time string
                    depTime = actualDuration + arrivalTime
                    if (int(60 * (depTime - int(depTime))) < 10):
                        depTimeStr = str(int(depTime)) + ":0" + str(int(60*((depTime-int(depTime)))))

                    else:
                        depTimeStr = str(int(depTime)) + ":" + str(int(60*((depTime-int(depTime)))))
                    
                    # Convert arrival time from decimal hours to a time string
                    if (int(60 * (arrivalTime - int(arrivalTime))) < 10):
                        arrivalTimeStr = str(int(arrivalTime)) + ":0" + str(int(60 * (arrivalTime - int(arrivalTime))))
                    else:
                        arrivalTimeStr = str(int(arrivalTime)) + ":" + str(int(60 * (arrivalTime - int(arrivalTime))))

                    # Get a random battery capacity

                    if (chanceOfPHEV > random()):
                        currBatteryCap = uniform(10,20)
                    else:
                        currBatteryCap = uniform(30,70)

                    events.append(Event(arrivalTimeStr, "add " + str(i) + " " + str(currBatteryCap) + " 11.5 " + str(currSOC) + " " + depTimeStr + " 100" + " Script"))
                    
                    arrivalTime = depTime + gauss(float(avgTimeBtwnCars), float(timeBtwnCarsStd))

        for index in np.arange(1,len(events)):

            currentvalue = events[index]
            position = index

            while (position > 0 and ((int(events[position-1].time.split(":")[0]) > int(currentvalue.time.split(":")[0])) or (int(events[position-1].time.split(":")[0]) == int(currentvalue.time.split(":")[0]) and int(events[position-1].time.split(":")[1]) > int(currentvalue.time.split(":")[1])))):
                events[position]=events[position-1]
                position = position-1
            events[position] = currentvalue


        while (t_hours < 24):
            station.sum_priorities = 0

            # Calculate port priorities
            for i,port in enumerate(station.ports):
                
                # remove completed vehicles
                if(port and ((port.depHours*60 + port.depMins) / 5) <= t):
                    station.ports[i] = None
                else:
                    if (port):

                        # calculate expected remaining time
                        time_remaining = ((port.depHours + port.depMins/60)) - (t*5/60)

                        # calculate port's priority if not fully charged
                        if((port.requestedCharge-port.SOC) > 0):
                            port.priority = (port.requestedCharge - port.SOC) / (port.maxChargeRate * time_remaining)
                        else:
                            port.priority = 0

                        if (port.priority >= 1):
                            port.priority = 1

                        # untempered power rate decision
                        if((port.requestedCharge-port.SOCd) > 0):
                            dumb_rate[i] = min(port.maxChargeRate, station.total_power, station.max_power)
                        else:
                            dumb_rate[i] = 0

                        # add current vehicle priority to the current total priority
                        station.sum_priorities += port.priority
                        sum_dumb_rates += dumb_rate[i]
                        dailyAverageHourlyDumbRate[t] += (dumb_rate[i])

            # go through every vehicle in every port to get port's delivered power (kW)
            for i,port in enumerate(station.ports):

                if(port and ((port.depHours*60 + port.depMins) / 5) > t):

                    # calculate port's delivered power if priority isn't zero
                    if(port.priority > 0):

                        # if calculated rate is more than vehicle's max, charge at vehicle's max
                        if(((port.priority / station.sum_priorities) * station.total_power) > port.maxChargeRate):
                            rate[i] = port.maxChargeRate

                        # otherwise, use calculated rate
                        else:
                            rate[i] = (port.priority / station.sum_priorities) * station.total_power


                        # if calculated rate is more than port's max, charge at port's max
                        if (rate[i] > station.max_power):
                            rate[i] = station.max_power

                        # add current port's delivered power to the current station total power
                        sum_rates += rate[i]
                        dailyAverageHourlySmartRate[t] += (rate[i])

                    else:
                        rate[i] = 0

                    # update state of charge of vehicle
                    port.SOC = ((((port.SOC/100)*port.packCapacity) + (rate[i])/12)/port.packCapacity)*100
                    totalDailyCharge = totalDailyCharge + rate[i]/12.0
                    totalDailyCost = totalDailyCost + rate[i]/12.0 * costOfPower[int(t_hours)]

                    port.SOCd = ((((port.SOCd/100)*port.packCapacity) + (dumb_rate[i])/12)/port.packCapacity)*100
                    totalDailyChargeD = totalDailyChargeD + dumb_rate[i]/12.0
                    totalDailyCostD = totalDailyCostD + dumb_rate[i]/12.0 * costOfPower[int(t_hours)]

                    if port.SOC >= 100:
                        port.SOC = 100
                    if port.SOCd >= 100:
                        port.SOCd = 100
                    
            

            # Execute all events that would take place at this time
            while (eventCounter < len(events) and ((int(events[eventCounter].time.split(":")[0]) < t_hours) or ((int(events[eventCounter].time.split(":")[0]) == t_hours and int(events[eventCounter].time.split(":")[1]) >= t_mins)))):
                processCmd(events[eventCounter].cmd)
                eventCounter += 1

            # Go to the next value in the simulation
            if (t_mins == 55):
                t_hours += 1
                t_mins = 0
            else:
                t_mins += 5
            t+=1

        dailyPower[j] = totalDailyCharge
        dailyPowerD[j] = totalDailyChargeD
        dailyCost[j] = totalDailyCost
        dailyCostD[j] = totalDailyCostD
        for i in range(288):
            averageHourlySmartRate[i] += dailyAverageHourlySmartRate[i]
            averageHourlyDumbRate[i] += dailyAverageHourlyDumbRate[i]
            dailyAverageHourlySmartRate[i] = 0
            dailyAverageHourlyDumbRate[i] = 0

    
    for i in range(288):
        averageHourlySmartRate[i] = averageHourlySmartRate[i] / days
        averageHourlyDumbRate[i] = averageHourlyDumbRate[i] / days

    # Plot the average power
    fig3 = plt.figure()
    ax6 = fig3.add_subplot(3,1,1)
    ax7 = fig3.add_subplot(3,1,3, sharey=ax6)
    ax6.set_title('Amount of Energy Delivered Per Day (Smart Charge)')
    ax6.set_xlabel('Daily Energy (kWh)')
    ax6.set_ylabel('Frequency')
    location = np.mean(dailyPower) + 3 * np.std(dailyPower)
    avg_string = "Average: " + str(np.mean(dailyPower))

    ax7.set_title('Amount of Energy Delivered Per Day (Dumb Rate)')
    ax7.set_xlabel('Daily Energy (kWh)')
    ax7.set_ylabel('Frequency')
    avg_string = "Average: " + str(np.mean(dailyPower))
    location = np.mean(dailyPowerD) + 3 * np.std(dailyPowerD)

    print("Median Energy: " + str(np.median(dailyPower))) 
    print("Average Energy: " + str(np.mean(dailyPower)))
    print("Standard Dev: " + str(np.std(dailyPower)))

    print("Median Energy: " + str(np.median(dailyPowerD)))
    print("Average Energy: " + str(np.mean(dailyPowerD)))
    print("Standard Dev: " + str(np.std(dailyPowerD)))

    sortDailyPower = sorted(dailyPower)
    sortDailyPowerD = sorted(dailyPowerD)

    fit1 = stats.norm.pdf(sortDailyPower, np.mean(sortDailyPower), np.std(sortDailyPower))

    ax6.plot(sortDailyPower,fit1,'-o')
    ax6.hist(sortDailyPower,normed=True)      

    fit2 = stats.norm.pdf(sortDailyPowerD, np.mean(sortDailyPowerD), np.std(sortDailyPowerD))

    ax7.plot(sortDailyPowerD,fit2,'-o')
    ax7.hist(sortDailyPowerD,normed=True)

    # Plot the average daily cost
    fig4 = plt.figure()
    ax8 = fig4.add_subplot(3,1,1)
    ax9 = fig4.add_subplot(3,1,3,sharey=ax8)
    ax8.set_title('Cost per Day (Smart Charge)')
    ax8.set_xlabel('Daily Costs ($)')
    ax8.set_ylabel('Frequency')

    ax9.set_title('Cost Per Day (Dumb Rate)')
    ax9.set_xlabel('Daily Costs ($)')
    ax9.set_ylabel('Frequency')

    print("Median Cost ($): " + str(round(np.median(dailyCost),2)))
    print("Average Cost ($): " + str(round(np.mean(dailyCost),2)))
    print("Standard Dev ($): " + str(round(np.std(dailyCost),2)))

    print("Median Cost ($): " + str(round(np.median(dailyCostD),2)))
    print("Average Cost ($): " + str(round(np.mean(dailyCostD),2)))
    print("Standard Dev ($): " + str(round(np.std(dailyCostD),2)))

    sortDailyCost = sorted(dailyCost)
    sortDailyCostD = sorted(dailyCostD)

    fit3 = stats.norm.pdf(sortDailyCost, np.mean(sortDailyCost), np.std(sortDailyCost))

    ax8.plot(sortDailyCost,fit3,'-o')
    ax8.hist(sortDailyCost,normed=True)      

    fit4 = stats.norm.pdf(sortDailyCostD, np.mean(sortDailyCostD), np.std(sortDailyCostD))

    ax9.plot(sortDailyCostD,fit4,'-o')
    ax9.hist(sortDailyCostD,normed=True)

    newXaxis = np.arange(288)
    
    axisLabel = [""] * 288
    for i in range(288):
        if (i % 12 == 0):
            axisLabel[i] = str(int(i/12)) + ":00"

    fig6 = plt.figure()
    ax12 = fig6.add_subplot(1,1,1)

    mask1 = ma.where(np.asarray(averageHourlySmartRate)>=np.asarray(averageHourlyDumbRate))
    mask2 = ma.where(np.asarray(averageHourlyDumbRate)>=np.asarray(averageHourlySmartRate))
    averageHourlySmartRate = np.asarray(averageHourlySmartRate)
    averageHourlyDumbRate = np.asarray(averageHourlyDumbRate)

    try:
        ax12.bar(newXaxis[mask1], averageHourlySmartRate[mask1], color='b', alpha=1, edgecolor='none',linewidth=0,width=1, log=False, label='Smart Charge')
        ax12.bar(newXaxis, averageHourlyDumbRate, color='r', alpha=1, edgecolor='black', linewidth=0, width=1, log=False, label='Dumb Charge')
        ax12.bar(newXaxis[mask2], averageHourlySmartRate[mask2], color='b', alpha=1, edgecolor='none',linewidth=0,width=1, log=False)

    
        ax12.set_title('Comparison of charge rates throughout the day')
        ax12.set_xlabel('Time of Day')
        ax12.set_ylabel('Charging Rate (kW)')
        plt.xticks(newXaxis, axisLabel, rotation=45)

        ax12.legend()
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
    except Exception as error:
        print(str(error))
    # ax12.plot(newXaxis, averageHourlySmartRate, '-b', newXaxis, averageHourlyDumbRate, '--r',linewidth = 1.5, tick_label = axisLabel)
    plt.show(block=False)
    print("Seed used: " + str(int(initSeed)))

def animate(i):
    global running, xs, ys0, ys1, ys2, ys3, ys4, ysd0, ysd1, ysd2, ysd3, ysd4

    if running:
        # -- TIME CALC -- #
        t_mins = (t*5)
        t_hours = int(t_mins/60)
        t_mins = int(t_mins-(60*t_hours))
        t_hours = t_hours+8 # simulation starts at 8 am, each sec is simulating 5 mins
        if(t_hours >= 24):
            t_hours = t_hours-24
        if(t_mins < 10):
            format_zero = "0"
        else:
            format_zero  = ""
        time_string = str(t_hours)+":"+format_zero+str(t_mins)
        new_t = dates.date2num(datetime.strptime(time_string, '%H:%M'))
        # -- END TIME CALC -- #

        rate = [0]*4
        dumb_rate = [0]*4
        sum_rates = 0
        sum_dumb_rates = 0

        animate.counter += 1
        station.sum_priorities = 0

        print("\n")
        print(time_string)

        if(t >= 144):
            processCmd("pause")
            endSim()

        # go through every vehicle in every port to get priorities
        for i,port in enumerate(station.ports):
            # if port has a vehicle in it
            if(port):

                # remove completed vehicles
                if(port.projDeparture <= t):
                    # send notification
                    registration_id = port.username
                    message_title = "Time to Depart"
                    message_body = "Your departure time has been reached."
                    try:
                        push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
                    except:
                        """ server not connected to internet """
                    # remove
                    station.ports[i] = None
                    print('Port [', i ,'] Vehicle removed & was', sep="", end='')
                    if port.SOC >= port.requestedCharge:
                        print(' satisfied!')
                    else:
                        print(' not satisfied...')
                else:
                    # calculate expected remaining time
                    time_remaining = port.projDeparture - t

                    # calculate port's priority if not fully charged
                    if((port.requestedCharge-port.SOC) > 0):
                        port.priority = (port.requestedCharge - port.SOC) / (port.maxChargeRate * time_remaining)
                    else:
                        port.priority = 0

                    # if greater than 1, set priority to 1
                    if(port.priority > 1):
                        port.priority = 1 

                    # untempered power rate decision
                    if((port.requestedCharge-port.SOCd) > 0):
                        dumb_rate[i] = min(port.maxChargeRate, station.total_power, station.max_power)
                    else:
                        dumb_rate[i] = 0

                    # add current vehicle priority to the current total priority
                    station.sum_priorities += port.priority
                    sum_dumb_rates += dumb_rate[i]

        # go through every vehicle in every port to get port's delivered power (kW)
        for i,port in enumerate(station.ports):
            # if the vehicle is currently parked
            if(not port):
                print('Port [', i ,'] EMPTY', sep="")

            if(port and port.projDeparture > t):

                # calculate port's delivered power if priority isn't zero
                if(port.priority > 0):

                    # if calculated rate is more than vehicle's max, charge at vehicle's max
                    if((port.priority / station.sum_priorities) * station.total_power) > port.maxChargeRate:
                        rate[i] = port.maxChargeRate
                    # otherwise, use calculated rate
                    else:
                        rate[i] = (port.priority / station.sum_priorities) * station.total_power

                    # if calculated rate is more than port's max, charge at port's max
                    if (rate[i] > station.max_power):
                        rate[i] = station.max_power
                # add current port's delivered power to the current station total power
                sum_rates += rate[i]

                # update state of charge of vehicle
                port.SOC = ((((port.SOC/100)*port.packCapacity) + (rate[i])/12)/port.packCapacity)*100

                port.SOCd = ((((port.SOCd/100)*port.packCapacity) + (dumb_rate[i])/12)/port.packCapacity)*100

                if port.SOC >= 100:
                    port.SOC = 100
                    if port.fullnotified == 0:
                        # send notification
                        port.fullnotified = 1
                        registration_id = port.username
                        message_title = "Fully Charged"
                        message_body = "Your vehicle is fully charged."
                        try:
                            push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
                        except:
                            """ server not connected to internet """
                if port.SOCd >= 100:
                    port.SOCd = 100

                print('Port [', i ,'] Vehicle SOC: %.2f' % ((port.SOC/100)*port.packCapacity),
                    "/%.2f" % ((port.requestedCharge/100)*port.packCapacity), " kWh", sep="", end='')
                if port.SOC >= port.requestedCharge:
                    print(' - Satisfied!')
                    if port.chargenotified == 0:
                        # send notification
                        port.chargenotified = 1
                        registration_id = port.username
                        message_title = "EV Charging Complete"
                        message_body = "Your vehicle has been charged to the requested value."
                        try:
                            push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)      
                        except:
                            """ server not connected to internet """
                else:
                    print("")


        # END OF CALCULATIONS #

        xs.append(new_t)
        ys0.append(rate[0])
        ys1.append(rate[1])
        ys2.append(rate[2])
        ys3.append(rate[3])
        ys4.append(sum_rates)
        ysd0.append(dumb_rate[0])
        ysd1.append(dumb_rate[1])
        ysd2.append(dumb_rate[2])
        ysd3.append(dumb_rate[3])
        ysd4.append(sum_dumb_rates)

        ax1.plot(xs, ys0, 'go-', label="ys0")
        ax1.plot(xs, ysd0, 'r--', label="ysd0")

        ax2.plot(xs, ys1, 'go-', label="ys1")
        ax2.plot(xs, ysd1, 'r--', label="ysd1")

        ax3.plot(xs, ys2, 'go-', label="ys2")
        ax3.plot(xs, ysd2, 'r--', label="ysd2")

        ax4.plot(xs, ys3, 'go-', label="ys3")
        ax4.plot(xs, ysd3, 'r--', label="ysd3")

        ax5.plot(xs, ys4, 'go-', label="ys4")
        ax5.plot(xs, ysd4, 'r--', label="ysd4")

        axes = [ax1, ax2, ax3, ax4]
        for i,port in enumerate(station.ports):
            if(port):
                maxCharge = port.maxChargeRate
            else:
                maxCharge = 1000
            axes[i].set_ylim([-1,min(maxCharge+1, station.total_power+1, station.max_power+1)])

        # FIX AX5 MAX Y VAL

        t += 1

    # Get command from socket for send.py terminal
    try:
        cmd = term_conn.recv(1024).decode('UTF-8')
        processCmd(cmd)
    except:
        """ no command """

    # Connect and get command from mobile devices (via Firebase)
    try:
        diction = fire.get('/add', None) # Get dictionary from database
        datakeys = list(diction.keys())  # Get list of keys (userIDs)
        
        # Get all commands (some might have been simultaneous)
        for key in datakeys:
            # Get value from key
            datain = diction[key]
              
            # TODO need to add port number transfer
            userID, app_port, batCap, initialSOC, hours, mins, reqSOC = datain.split()
            
            # Delete from firebase (it's been read)
            fire.delete('/add', userID)
            
            # Create command string
            cmd = "add " + app_port + " " + batCap + " 11.5 " + initialSOC + " " + hours + ":" + mins + " " + reqSOC + " " + userID
            # FOR NOW: automatically add with 11.5 maxChargeRate (typical max of station)
        
            processCmd(cmd)
    except:
        """ no connection available yet """

animate.counter = 0

xs = []
ys0 = []
ys1 = []
ys2 = []
ys3 = []
ys4 = []

ysd0 = []
ysd1 = []
ysd2 = []
ysd3 = []
ysd4 = []


# Uncomment one of the below to select which type of plot
ani = animation.FuncAnimation(fig, animate, interval=1000)
#ani2 = animation.FuncAnimation(fig2, animate, interval=1000)
plt.show()

term_conn.close()