ev-smartcharge

Electric Vehicle Smart Charge
-----------------------------
This project is a collaboration between Michigan Technological University's Wireless Communication Enterprise and their sponsor, Ford Motor Company. The goal is to create a simulation of an electric vehicle charging station that supports a given number of ports (around 4-6) and intelligently prioritizes the rate of charge sent to each connected vehicle based on a variety of factors, such as arrival and departure time, amount of charge needed, etc.

An Android application also interfaces with this simulation, so that a driver may select the time they wish to depart the charging station, which the station then factors into its algorithm to decide on the most efficient way to charge the vehicle.

Files
-----
Android:
- Contains source code for Android application, developed in Android studio and currently being tested on Google Pixel XL

Simulation_1:
- Contains our first attempt at simulation, now deprecated

Simulation_2:
- Contains current simulation code, based off Excel demonsration created by Andy Drews at Ford
- To run, execute "python SmartChargeSimulation.py"
- Plot.py is deprecated

SocketDemo.py:
- Testing and playing around with socket communication in Python, will be removed

