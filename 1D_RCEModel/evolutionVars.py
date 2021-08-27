import numpy as np
import csv
from matplotlib import pyplot as plt

def evolvingProfs(state):
	# Compiling csv input into individual variables
	dataArr = []
	with open('output_runModel/weekly_results.csv', 'r') as weeklyFile:
		csvRead = csv.reader(weeklyFile)
		for row in csvRead:
			dataArr.append(row)
	dataArr =  [ele for ele in dataArr if ele != []] 
	olrs, bdry_tempDiff, surfT, netEn = dataArr[0], dataArr[1], dataArr[2], dataArr[3]

	# OLR
	fig = plt.figure()
	olr = [float(i) for i in olrs]
	plt.plot(olr)
	plt.xlabel("Weeks")
	plt.ylabel("Outgoing Longwave Radiation (W m^-2)")
	plt.savefig("graphs/weeklyOLR.png")
	
	# Plotting bdry_tempDiff
	fig = plt.figure()
	bdry_tempDiff = [float(i) for i in bdry_tempDiff]
	plt.plot(bdry_tempDiff)
	plt.xlabel("Weeks")
	plt.ylabel("Surface-Air Temperature Gradient (K)")
	plt.savefig("graphs/weeklybdry_tempDiff.png")
	
	# Plotting surfT
	fig = plt.figure()
	surfT = [float(i) for i in surfT]
	plt.plot(surfT)
	plt.xlabel("Weeks")
	plt.ylabel("Surface Temperature (K)")
	plt.savefig("graphs/weekly_surfT.png")
	
	#Plotting netEn
	fig = plt.figure()
	netEn = [float(i) for i in netEn]
	plt.plot(netEn)
	plt.xlabel("Weeks")
	plt.ylabel("Net Energy Level in Atmospheric Column (W m^-2)")
	plt.savefig("graphs/weekly_netEn.png")
	
	return 0.
