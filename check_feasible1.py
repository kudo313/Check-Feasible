import numpy as np
import copy
import math
# read input
input_file = 'input1.txt'
f = open(input_file,'r')
f_name = f.readline()
f_name = f_name.split()[0]
ListMoveTech = []
RoutesDrone = []
Visited = []
first_line = f.readline()
second_line = f.readline()
tech_len = len(first_line)
tech_string = first_line[2:tech_len - 2]
tech_list = tech_string.split("],[")
for tech_route in tech_list:
    route = []
    elements = tech_route.split(" ")
    for element in elements:
        try:
            route.append(int(element))
        except:
            pass
    ListMoveTech.append(route)
print(ListMoveTech)
N_Technican = len(ListMoveTech)

drone_len = len(second_line)
drone_string = second_line[1:drone_len - 1]
drone_list = drone_string.split("],[")
for drone_route in drone_list:
    route = []
    elements = drone_route.split(" ")
    for element in elements:
        try:
            route.append(int(element))
        except:
            pass
    RoutesDrone.append(route)
print(RoutesDrone)
# ListMoveTech = [[0, 14, 11, 12, 42], [0, 37, 45, 47, 34, 26, 13, 27, 33, 17, 18, 29, 24, 8, 20, 22, 36, 28, 30, 9, 19, 10, 43, 15], [0, 50, 21, 4, 41, 16, 48, 40, 25, 49, 1, 23, 32, 31, 39, 5, 7, 46, 35, 44, 38], [0, 6, 3, 2]] 
# RoutesDrone =[[0, 41], [0, 47], [0, 40], [0, 13], [0, 1], [0, 33], [0, 18], [0, 31], [0, 20], [0, 30], [0, 46], [0, 19]]
# N_Technican = 5
print("Input: " )
print(ListMoveTech)
print(RoutesDrone)
f_name_file = f_name + ".txt"
# create variable
f = open("./data/" + f_name_file,"r")
numberOfDepot = 1
depot = 0
timeRateTech = 1/0.58
timeRateDrone = 1/0.83
edurance = 30
oneLine = f.readline()
oneLine = oneLine.split()
numberOfCus = int(oneLine[1])
Visited = np.zeros(numberOfCus + 1, int)
for i in RoutesDrone:
    for j in range(1, len(i)):
        Visited[i[j]] = 1
print(Visited)
print("Kết quả: ")
oneLine = f.readline()
coor_matrix = np.zeros((numberOfCus+numberOfDepot,2))
for i in range(1,numberOfCus+1):
    oneLine = f.readline()
    oneLine = oneLine.split()
    coor_matrix[i][0] = oneLine[0]
    coor_matrix[i][1] = oneLine[1]
totalPoint = numberOfCus + numberOfDepot
distanceMatrix =  np.zeros((numberOfCus+numberOfDepot,totalPoint))
timeTechMatrix =  np.zeros((numberOfCus+numberOfDepot,totalPoint))
timeDroneMatrix = np.zeros((numberOfCus+numberOfDepot,totalPoint))
unfeasible = False
for i in range(totalPoint):
    for j in range(totalPoint):
        if (i != j):
            distanceMatrix[i][j] = math.sqrt(pow(coor_matrix[i][0] - coor_matrix[j][0],2) + pow(coor_matrix[i][1] - coor_matrix[j][1],2))
            timeTechMatrix[i][j] = timeRateTech*distanceMatrix[i][j]
            timeDroneMatrix[i][j] = timeRateDrone*distanceMatrix[i][j]
        else:
            distanceMatrix[i][j]  = 0
            timeDroneMatrix[i][j] = 0
            timeTechMatrix[i][j] = 0
cusInDroneFlyRange = []
for i in range(1, totalPoint):
    if timeDroneMatrix[depot][i] + timeDroneMatrix[i][depot] <= edurance:
        cusInDroneFlyRange.append(i)
numCusInDroneRange = len(cusInDroneFlyRange)
if totalPoint < 14:
    D = 120
elif totalPoint < 22:
    D = 240
elif totalPoint < 52:
    D = 480
else: 
    D = 600
# create variable
TimeGuessOfTechIF = []
N_Technican = len(ListMoveTech)
for i in range(N_Technican):
    GuessTime = [0]
    TimeGuessOfTechIF.append(GuessTime)
TimeTechLeavePoint = np.zeros(totalPoint)
TimeTechArrivePoint = np.zeros(totalPoint)
TimeStartOfRoutesIF = np.zeros(len(RoutesDrone))
TimeDroneArrivePoint = copy.deepcopy(RoutesDrone)
TimeDroneLeavePoint = copy.deepcopy(RoutesDrone)
TimeDroneArriveDepot = np.zeros(len(RoutesDrone))
TimeTechArriveDepot = np.zeros(len(ListMoveTech))
AfterPointCarrySample = np.zeros(totalPoint, int)
for i in range(1, totalPoint):
    AfterPointCarrySample[i] = -1
TimeSampleInDepot = np.zeros(totalPoint)
totalSampleWaitTime = 0
totalDurationViolation = 0
totalWorkingTimeViolation = 0
# check feasible order in route
TheDroneRouteOfPoint1 = np.zeros(totalPoint, int)
OrderOfPointInDroneRoute1 = np.zeros(totalPoint, int)
# position of customer in drone trip
for i in range(totalPoint):
    TheDroneRouteOfPoint1[i] = (-1)*(i + 1)
    OrderOfPointInDroneRoute1[i] = (-1)*(i + 1)
for i in range(len(RoutesDrone)):
    for j in range(1, len(RoutesDrone[i])):
        thisPoint = RoutesDrone[i][j]
        TheDroneRouteOfPoint1[thisPoint] = i
        OrderOfPointInDroneRoute1[thisPoint] = j
for i in range(len(ListMoveTech)):
    maxRoute = 0
    for j in range(1, len(ListMoveTech[i])):
        findPoint = ListMoveTech[i][j]
        if Visited[findPoint] == 1:
            if TheDroneRouteOfPoint1[findPoint] >= 0 and TheDroneRouteOfPoint1[findPoint] < maxRoute:
                unfeasible = True
                print(findPoint)
                print(maxRoute)
                print("Sai thứ tự khách hàng trong hành trình drone hoặc nhân viên")
            else:
                maxRoute = TheDroneRouteOfPoint1[findPoint]
# print(ListMoveTech)
for i in range(N_Technican):
    N_PointOfTechRoute = len(ListMoveTech[i])
    timeOfTech = 0
    for j in range(1,N_PointOfTechRoute):
        thisPoint = ListMoveTech[i][j]
        prePoint = ListMoveTech[i][j - 1]
        timeArrivePoint = timeOfTech + timeRateTech*distanceMatrix[prePoint][thisPoint]
        TimeGuessOfTechIF[i].append(timeArrivePoint)
        TimeTechLeavePoint[thisPoint]  =  timeArrivePoint
        TimeTechArrivePoint[thisPoint]  =  timeArrivePoint
        timeOfTech = timeArrivePoint
        if Visited[thisPoint] == 0:
            if j != N_PointOfTechRoute -1 :
                AfterPointCarrySample[thisPoint] = ListMoveTech[i][j + 1]
            else:
                AfterPointCarrySample[thisPoint] = 0
    TimeTechArriveDepot[i] = TimeTechLeavePoint[thisPoint] + timeTechMatrix[thisPoint][0]
N_RoutesOfDrone = len(RoutesDrone)
timeDrone = 0
for i in range(N_RoutesOfDrone):
    N_PointOfDroneRoute = len(RoutesDrone[i])
    if N_PointOfDroneRoute > N_Technican + 1:
        unfeasible = True
        print("Hành trình drone bị lỗi, 1 hành trình có nhiều khách hàng hơn số nhân viên")
    durationOfDrone = 0
    timeStart = timeDrone
    for j in range(1, N_PointOfDroneRoute):
        thisPoint = RoutesDrone[i][j]
        prePoint = RoutesDrone[i][j - 1]
        timeToPickUp = timeRateDrone*distanceMatrix[prePoint][thisPoint]
        timeToBackDepot = timeRateDrone*distanceMatrix[thisPoint][depot]
        guessDroneTime = timeDrone + timeToPickUp
        if j == N_PointOfDroneRoute - 1:
            AfterPointCarrySample[thisPoint] = depot
        else:
            AfterPointCarrySample[thisPoint] = RoutesDrone[i][j + 1]
        if guessDroneTime < TimeTechLeavePoint[thisPoint]:
            if j != 1:
                durationOfDrone +=  TimeTechLeavePoint[thisPoint] - timeDrone
                TimeDroneArrivePoint[i][j] = timeDrone + timeToPickUp
                timeDrone = TimeTechLeavePoint[thisPoint]
                TimeDroneLeavePoint[i][j] = timeDrone
            else:
                # drone will wait at depot to arrive point (thisPoint) in the same with technican
                durationOfDrone +=  timeToPickUp
                timeStart = TimeTechLeavePoint[thisPoint] - timeToPickUp
                TimeDroneArrivePoint[i][j] = timeDrone + timeToPickUp
                timeDrone = TimeTechLeavePoint[thisPoint]
                TimeDroneLeavePoint[i][j] = timeDrone
        else:
            durationOfDrone += timeToPickUp
            timeDrone += timeToPickUp
            TimeDroneLeavePoint[i][j] = timeDrone
            TimeDroneArrivePoint[i][j] = timeDrone
            # bonus waiting time for guess time of tech
            checkBreak = False
            for u in range(N_Technican):
                for v in range(1, len(ListMoveTech[u])):
                    findPoint = ListMoveTech[u][v]
                    if findPoint == thisPoint:
                        if v != len(ListMoveTech[u]) - 1:
                            for k in range(v+1, len(ListMoveTech[u])):
                                pointAfterThisPoint = ListMoveTech[u][k]
                                TimeTechLeavePoint[pointAfterThisPoint] += timeDrone - TimeTechLeavePoint[thisPoint]
                                TimeTechArrivePoint[pointAfterThisPoint] += timeDrone - TimeTechArrivePoint[thisPoint]
                        checkBreak = True
                        break
                if checkBreak == True:
                    lastPointInTechRoute = ListMoveTech[u][-1]
                    TimeTechArriveDepot[u] = TimeTechLeavePoint[lastPointInTechRoute] + timeTechMatrix[lastPointInTechRoute][0]
                    break
            TimeTechLeavePoint[thisPoint] = timeDrone
    timeDrone += timeDroneMatrix[RoutesDrone[i][N_PointOfDroneRoute - 1]][0]
    TimeDroneArriveDepot[i] = timeDrone
    totalDurationViolation += max(timeDrone - timeStart - edurance, 0)
# caculate time back to depot of sample
for i in range(1, totalPoint):
    if AfterPointCarrySample[i] == 0 :
        if Visited[i] == 1:
            TimeSampleInDepot[i] = TimeTechLeavePoint[i] + timeDroneMatrix[i][0]
        else:
            TimeSampleInDepot[i] = TimeTechLeavePoint[i] + timeTechMatrix[i][0]
for i in range(1, totalPoint):
    if AfterPointCarrySample[i] != 0:
        afterPoint = AfterPointCarrySample[i]
        while AfterPointCarrySample[afterPoint] != 0:
            afterPoint = AfterPointCarrySample[afterPoint] 
        TimeSampleInDepot[i] = TimeSampleInDepot[afterPoint]
# caculate waiting time of sample
for i in range(1, totalPoint):
    totalSampleWaitTime += TimeSampleInDepot[i] - TimeTechArrivePoint[i]
# caculate working time violation
for i in range(N_Technican):
    totalWorkingTimeViolation += max(TimeTechArriveDepot[i] - D, 0)
if N_RoutesOfDrone != 0:
    totalWorkingTimeViolation += max(TimeDroneArriveDepot[-1] - D, 0)
fitness = 0
fitness += totalSampleWaitTime
print(fitness)
# update alpha beta
dz = totalDurationViolation
wz = totalWorkingTimeViolation
fz = totalSampleWaitTime
if totalDurationViolation == 0 :
    feasibleWithDroneEdurance = True
else:
    feasibleWithDroneEdurance = False
    print("Vi pham thoi gian giới hạn của drone: " + str(totalDurationViolation))
if totalWorkingTimeViolation == 0:
    feasibleWithMaximumWorking = True

else:
    feasibleWithMaximumWorking = False
    print("Vi pham thoi gian làm việc của nhân viên: " + str(totalWorkingTimeViolation))
if totalDurationViolation == 0 and totalWorkingTimeViolation == 0 and unfeasible == False:
    feasible = True
    print("lời giải hợp lệ")
    print("fitness: " + str(22))
else:
    feasible = False

