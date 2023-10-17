#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon July 24 10:30:12 2023

@author: James Klinman

to run: runfile('netCDF_Data_Extract.py', args='668.nc')
"""

# Note: This module import list is historical,
# possibly not all are required
import os
import sys
import netCDF4 


"""
Below contains the files being accessed and creates the data file to be made
"""

infile = sys.argv[1]
flight1 = netCDF4.Dataset(infile) #!!need to automate name


#uncomment below if you want to see the variable keys
#print(flight1.variables.keys())

"""  
Below reads in specific airplane data and preps empty lists to store the data in
"""
#This is pulling in the data and making empty lists
HH = flight1.variables['TIME_HOURS_20Hz']
MM = flight1.variables['TIME_MINUTES_20Hz']
SS = flight1.variables['TIME_SECONDS_20Hz']
lat1 = flight1.variables['LATITUDE_DECIMAL_DEG_20Hz']
long1 = flight1.variables['LONGITUDE_DECIMAL_DEG_20Hz']
alt = flight1.variables['GPS_ALTITUDE']
temp = flight1.variables['TEMPERATURE_ROSEMOUNT_SENSOR']
updraft = flight1.variables['UPDRAFT']
LWC_DMT = flight1.variables['LWC_DMT']
FSSP = flight1.variables['FSSP_LIQUID_WATER']
airspeed = flight1.variables['TRUE_AIRSPEED_CALCULATED']
airspeedNCAR = flight1.variables['TRUE_AIRSPEED_NCAR']
hailLWC = flight1.variables['HAIL_WATER']
hailCounts = flight1.variables['HAIL_TOTAL_COUNTS']

#HHx = HH.shape[1]
HHy = HH.shape[0]
#MMx = MM.shape[1]
MMy = MM.shape[0]
#SSx = SS.shape[1]
SSy = SS.shape[0]

#lat1x = lat1.shape[1]
lat1y = lat1.shape[0]

#long1x = long1.shape[1]
long1y = long1.shape[0]

#altx = alt.shape[1]
alty = alt.shape[0]

tempy = temp.shape[0]
updrafty = updraft.shape[0]
LWC_DMTy = LWC_DMT.shape[0]
FSSPy = FSSP.shape[0]
airspeedy = airspeed.shape[0]
hailLWCy = hailLWC.shape[0]
hailCountsy = hailCounts.shape[0]


HHFirstlist = []
MMlist = []
SSlist = []
lat1list = []
long1list = []
altlist = []
templist = []
updraftlist = []
LWClist = []
FSSPlist = []
airspeedlist = []
hailLWClist = []
hailCountslist = []

"""
Below is storing the data in the lists
"""

#These loops write out the data points for the whole data file and for each second
for x in range(0, lat1y): 
    lat1list.append(float(lat1[x,0])) #stores a data point for each sec of flight (1Hz instead of 20Hz) 
       
#The below chunk is a copy of the latitude but for longitude
for x in range(0, long1y):
    long1list.append(float(long1[x,0]))
    
#The below chunk is a copy of the latitude but for altitude
for x in range(0, alty):
    altlist.append(float(alt[x,0]))
    
#The below chunk is a copy of the latitude but for time
for x in range(0, HHy):
    HHFirstlist.append(float(HH[x,0]))
for x in range(0, MMy):
    MMlist.append(float(MM[x,0]))
for x in range(0, SSy):
    SSlist.append(float(SS[x,0]))
    
#For rest of variables
for x in range(0, tempy):
    templist.append(float(temp[x,0]))
    
for x in range(0, updrafty):
    updraftlist.append(float(updraft[x,0]))

for x in range(0, LWC_DMTy):
    LWClist.append(float(LWC_DMT[x,0]))
    
for x in range(0, FSSPy):
    FSSPlist.append(float(FSSP[x,0]))
    
for x in range(0, airspeedy):
    airspeedlist.append(float(airspeed[x,0]))
    
for x in range(0, hailLWCy):
    hailLWClist.append(float(hailLWC[x,0]))
    
for x in range(0, hailCountsy):
    hailCountslist.append(float(hailCounts[x,0]))
    

"""
Below is creating the file and formatting it
"""
    
HHlist = []
#correcting for colorado timezone NOW 0 BECAUSE I WANT UTC
for x in HHFirstlist:
    HHlist.append(x - 0)

#the abc's are just sepcific identifiers, they don't necesarilly have to be
#in order. Add and take them away depending on what you want to see in the
#file. Make sure you get the spacing specification correct so that the file
#prints cleanly
FlightNum = str(getattr(flight1, 'FlightNumber'))

TestFile = open('Sensor_Information/FlightInfo_' + str(FlightNum) + '.txt', "w+")
TestFile.write('{a:<3}{b:<3}{c:<3}{d:<10}{e:<12}{f:<10}{g:<13}{i:<15}{z:<18}'\
               '{k:<16}{l:<11}{h:<8}{j:<14}'.format\
               (a='HH', b='MM', c='SS', d='Lat', e='Long', f='Alt(m)',\
               g='Updraft(m/s)', i='LWC_DMT(g/m^3)', z='FSSP_LIQUID_WATER', k='Hail_LWC(g/m^3)',\
               l="HailCounts", h='Temp(C)', j='Calc_Airspeed'))
TestFile.write('\n')
#i did the range as HHy, but if there's ever a different y value in the data
#then that will have to be manually altered for the shortest array/list/etc
for x in range(HHy):    
    TestFile.write('{a:<3}{b:<3}{c:<3}{d:<10}{e:<12}{f:<10}{g:<13}{i:<15}{z:<18}{k:<16}{l:<11}{h:<8}{j:<14}'.format\
                   (a=int(HHlist[x]), b=int(MMlist[x]), c=int(SSlist[x]),\
                    d=round(lat1list[x], 5), e=round(long1list[x], 5),\
                    f=round(altlist[x], 3),  g=round(updraftlist[x], 4), \
                     i=round(LWClist[x], 7), z=round(FSSPlist[x], 7),\
                     k=round(hailLWClist[x], 7),\
                    l=hailCountslist[x], h=round(templist[x], 3), j=round(airspeedlist[x], 3)))
    TestFile.write('\n')

TestFile.close()
    
