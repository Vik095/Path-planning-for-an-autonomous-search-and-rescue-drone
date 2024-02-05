# INIT----------------------------------------------
import math
import time
from turtle import pos
from AreaDivision import DARP
import sim
import numpy as np
from PIL import Image
from mstmodified import DARPVisualizer
import matplotlib.pyplot as plt
ip = '127.0.0.05'
port = 19999
client_id = sim.simxStart(ip, port, True, True, 5000, 5)
if client_id != -1:
    print('Connected to CoppeliaSim remote API')
# ------------------------------------------------------------

# TARGET handlee
_, ball_handleee = sim.simxGetObjectHandle(client_id, './targete', sim.simx_opmode_blocking)
_, Floor = sim.simxGetObjectHandle(
    client_id, 'Floor', sim.simx_opmode_blocking)
_, dronee = sim.simxGetObjectHandle(
    client_id, 'Quadcoptere', sim.simx_opmode_blocking)

# SENSOR handleeS--------------------------------------------------------------------------------------
_, frontSensore = sim.simxGetObjectHandle(
    client_id, './frontSensore', sim.simx_opmode_blocking)
_, backSensore = sim.simxGetObjectHandle(
    client_id, './backSensore', sim.simx_opmode_blocking)
_, leftSensore = sim.simxGetObjectHandle(
    client_id, './leftSensore', sim.simx_opmode_blocking)
_, rightSensore = sim.simxGetObjectHandle(
    client_id, './rightSensore', sim.simx_opmode_blocking)
_, backRighteSensore = sim.simxGetObjectHandle(
    client_id, './backRighteSensore', sim.simx_opmode_blocking)
_, frontRighteSensore = sim.simxGetObjectHandle(
    client_id, './frontRighteSensore', sim.simx_opmode_blocking)
_, frontLefteSensore = sim.simxGetObjectHandle(
    client_id, './frontLefteSensore', sim.simx_opmode_blocking)
_, backLefteSensore = sim.simxGetObjectHandle(
    client_id, './backLefteSensore', sim.simx_opmode_blocking)
# --------------------------------------------------------------------------------------------------------
# _, bottomCamera = sim.simxGetObjectHandle(
#     client_id, './Vision_sensor', sim.simx_opmode_blocking)
# _, _, image = sim.simxGetVisionSensorImage(
#     client_id, bottomCamera, 0, sim.simx_opmode_streaming)
# time.sleep(0.1)
# _, _, image = sim.simxGetVisionSensorImage(
#     client_id, bottomCamera, 0, sim.simx_opmode_buffer)

# # Streaming mode for proximity sensors
# _, detectionStatee, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, backSensore, sim.simx_opmode_streaming)
# time.sleep(5)
# print("Back Sensor Data:")
# _, detectionStatee, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, backSensore, sim.simx_opmode_buffer)
# print(detectionStatee)
# print(detectedPoint)
# print(norm)

# # Front sensor streaming mode
# _, detectionStatee, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, frontSensore, sim.simx_opmode_streaming)
# time.sleep(5)
# print("Front Sensor Data:")
# _, detectionStatee, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, frontSensore, sim.simx_opmode_buffer)
# print(detectionStatee)
# print(detectedPoint)
# print(norm)


# _, detectionStatee, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, rightSensore, sim.simx_opmode_streaming)
# time.sleep(5)
# print("Right Sensor Data:")
# _, detectionStatee, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, rightSensore, sim.simx_opmode_buffer)
# print(detectionStatee)
# print(detectedPoint)
# print(norm)
# def oneUp(handlee):
#     _,position=sim.simxGetObjectPosition(client_id, handlee,-1, sim.simx_opmode_streaming)
#     time.sleep(2)
#     for i in range(100):
#         _,position=sim.simxGetObjectPosition(client_id, handlee,-1, sim.simx_opmode_buffer)
#         sim.simxSetObjectPosition(client_id, handlee,-1,[positione[0],positione[1],positione[2]+0.01],sim.simx_opmode_blocking)
#         _,position=sim.simxGetObjectPosition(client_id, handlee,-1, sim.simx_opmode_buffer)
# handlee = ball_handleee  # Assuming ball_handleee is defined elsewhere in your code

# handlee = ball_handleee  # Assuming ball_handleee is defined elsewhere in your code
# _, positione = sim.simxGetObjectPosition(client_id, ball_handleee, -1, sim.simx_opmode_blocking)
# init = positione[2]

# while positione[2] < 7:
#     _, positione = sim.simxGetObjectPosition(client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#     # positione[2] += 0.01  # Increment the Z coordinate
#     sim.simxSetObjectPosition(client_id, ball_handleee, -1, [positione[0],positione[1],positione[2]+0.05], sim.simx_opmode_blocking)

#     _, positione = sim.simxGetObjectPosition(client_id, ball_handleee, -1, sim.simx_opmode_buffer)

# _,position=sim.simxGetObjectPosition(client_id, ball_handleee,-1, sim.simx_opmode_streaming)
# time.sleep(3)
# sim.simxSetObjectPosition(client_id,ball_handleee,-1,[1,1,positione[2]],sim.simx_opmode_blocking)
# time.sleep(3)
# sim.simxSetObjectPosition(client_id,ball_handleee,-1,[1,2,positione[2]],sim.simx_opmode_blocking)


# print(collisione(frontSensore))
time.sleep(2)


def collisione(handlee):
    _, detectionStatee, _, _, _ = sim.simxReadProximitySensor(
        client_id, handlee, sim.simx_opmode_streaming)
    time.sleep(0.2)
    _, detectionStatee, _, _, _ = sim.simxReadProximitySensor(
        client_id, handlee, sim.simx_opmode_buffer)
    return detectionStatee


sensor_handlees = {
    0: frontSensore,
    1: frontRighteSensore,
    2: rightSensore,
    3: backRighteSensore,
    4: backSensore,
    5: backLefteSensore,
    6: leftSensore,
    7: frontLefteSensore
}


def distance(positione, target):
    dx = positione[0]-target[0]
    dy = positione[1]-target[1]
    dz = positione[2]-target[2]
    dist = np.sqrt((dx**2)+(dy**2))
    return dist


target_positione = [20, +25, 5]
# def oneUp():
#     _,position=sim.simxGetObjectPosition(client_id, ball_handleee,-1, sim.simx_opmode_streaming)
#     time.sleep(0.1)
#     _,position=sim.simxGetObjectPosition(client_id, ball_handleee,-1, sim.simx_opmode_buffer)
#     time.sleep(0.1)
#     init = positione[2]+1

#     while positione[2]<init:
#         _,position=sim.simxGetObjectPosition(client_id, ball_handleee,-1, sim.simx_opmode_buffer)
#         sim.simxSetObjectPosition(client_id,ball_handleee,-1,[positione[0],positione[1],positione[2]+0.05],sim.simx_opmode_oneshot)
#         _,position=sim.simxGetObjectPosition(client_id, ball_handleee,-1, sim.simx_opmode_buffer)
#         time.sleep(0.1)


# def collisione_distance(i):
#     _, positione = sim.simxGetObjectPosition(
#         client_id, ball_handleee, -1, sim.simx_opmode_streaming)
#     time.sleep(0.1)
#     _, positione = sim.simxGetObjectPosition(
#         client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#     time.sleep(0.1)
#     _, _, detectDist, _, _ = sim.simxReadProximitySensor(
#         client_id, sensor_handlees[i], sim.simx_opmode_streaming)
#     time.sleep(1)
#     _, _, detectDist, _, _ = sim.simxReadProximitySensor(
#         client_id, sensor_handlees[i], sim.simx_opmode_buffer)
#     if (distance(detectDist, position) < 0.05):
#         return False
#     else:
#         return True


def oneBacke():
    # ID=1
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = positione[1]-1

    while (positione[1] >= init and not collisione(sensor_handlees[4])):
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(
            client_id, ball_handleee, -1, [positione[0], positione[1]-0.05, positione[2]], sim.simx_opmode_oneshot)
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


def oneFronte():
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = positione[1]+1

    while (positione[1] <= init):
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(
            client_id, ball_handleee, -1, [positione[0], positione[1]+0.05, positione[2]], sim.simx_opmode_oneshot)
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


def oneRighte():

    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = positione[0]+1

    while positione[0] <= init:
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(
            client_id, ball_handleee, -1, [positione[0]+0.05, positione[1], positione[2]], sim.simx_opmode_oneshot)
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


def oneLefte():
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = positione[0]-1

    while positione[0] >= init:
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(
            client_id, ball_handleee, -1, [positione[0]-0.05, positione[1], positione[2]], sim.simx_opmode_oneshot)
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


# def backRighte():

#     _, positione = sim.simxGetObjectPosition(
#         client_id, ball_handleee, -1, sim.simx_opmode_streaming)
#     time.sleep(0.1)
#     _, positione = sim.simxGetObjectPosition(
#         client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#     time.sleep(0.1)
#     init = position.copy()
#     if(target_positione[0]-positione[0]==0):
#         theta=np.pi/2
#     else:
#         theta = np.arctan(
#         abs((target_positione[1]-positione[1])/(target_positione[0]-positione[0])))

#     while distance(position, init) < 1:
#         _, positione = sim.simxGetObjectPosition(
#             client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#         sim.simxSetObjectPosition(client_id, ball_handleee, -1, [positione[0]+abs(np.cos(
#             theta))/20, positione[1]-1/20, positione[2]], sim.simx_opmode_oneshot)
#         _, positione = sim.simxGetObjectPosition(
#             client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#         time.sleep(0.1)

def backRighte():

    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = positione[0]+1
    if (target_positione[0]-positione[0] == 0):
        theta = np.pi/2
    else:
        theta = np.arctan(
            abs((target_positione[1]-positione[1])/(target_positione[0]-positione[0])))

    while positione[0] <= init:
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handleee, -1, [
                                  positione[0]+0.05, positione[1]-0.05, positione[2]], sim.simx_opmode_oneshot)
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


# def backLefte():

#     _, positione = sim.simxGetObjectPosition(
#         client_id, ball_handleee, -1, sim.simx_opmode_streaming)
#     time.sleep(0.1)
#     _, positione = sim.simxGetObjectPosition(
#         client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#     time.sleep(0.1)
#     init = position.copy()
#     if(target_positione[0]-positione[0]==0):
#         theta=np.pi/2
#     else:
#         theta = np.arctan(
#         abs((target_positione[1]-positione[1])/(target_positione[0]-positione[0])))

#     while distance(position, init) < 1:
#         _, positione = sim.simxGetObjectPosition(
#             client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#         sim.simxSetObjectPosition(client_id, ball_handleee, -1, [positione[0]-abs(np.cos(
#             theta))/20, positione[1]-1/20, positione[2]], sim.simx_opmode_oneshot)
#         _, positione = sim.simxGetObjectPosition(
#             client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#         time.sleep(0.1)

def backLefte():

    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = positione[0]-1
    if (target_positione[0]-positione[0] == 0):
        theta = np.pi/2
    else:
        theta = np.arctan(
            abs((target_positione[1]-positione[1])/(target_positione[0]-positione[0])))

    while positione[0] >= init:
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handleee, -1, [
                                  positione[0]-0.05, positione[1]-0.05, positione[2]], sim.simx_opmode_oneshot)
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


# def frontRighte():

#     _, positione = sim.simxGetObjectPosition(
#         client_id, ball_handleee, -1, sim.simx_opmode_streaming)
#     time.sleep(0.1)
#     _, positione = sim.simxGetObjectPosition(
#         client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#     time.sleep(0.1)
#     init = position.copy()
#     if(target_positione[0]-positione[0]==0):
#         theta=np.pi/2
#     else:
#         theta = np.arctan(
#         abs((target_positione[1]-positione[1])/(target_positione[0]-positione[0])))
#     while distance(position, init) < 1:
#         _, positione = sim.simxGetObjectPosition(
#             client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#         sim.simxSetObjectPosition(client_id, ball_handleee, -1, [positione[0]+abs(np.cos(
#             theta))/20, positione[1]+1/20, positione[2]], sim.simx_opmode_oneshot)
#         _, positione = sim.simxGetObjectPosition(
#             client_id, ball_handleee, -1, sim.simx_opmode_buffer)
#         time.sleep(0.1)

def frontRighte():

    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = positione[0]+1
    if (target_positione[0]-positione[0] == 0):
        theta = np.pi/2
    else:
        theta = np.arctan(
            abs((target_positione[1]-positione[1])/(target_positione[0]-positione[0])))
    while positione[0] <= init:
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handleee, -1, [
                                  positione[0]+0.05, positione[1]+0.05, positione[2]], sim.simx_opmode_oneshot)
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


def frontLefte():

    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = positione[0]-1
    if (target_positione[0]-positione[0] == 0):
        theta = np.pi/2
    else:
        theta = np.arctan(
            abs((target_positione[1]-positione[1])/(target_positione[0]-positione[0])))
    while positione[0] >= init:
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handleee, -1, [
                                  positione[0]-0.05, positione[1]+0.05, positione[2]], sim.simx_opmode_oneshot)
        _, positione = sim.simxGetObjectPosition(
            client_id, ball_handleee, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)
def cost(index, position):

    new_positione = position.copy()
    if (target_positione[0]-positione[0] == 0):
        theta = np.pi/2
    else:
        theta = np.arctan(
            abs((target_positione[1]-positione[1])/(target_positione[0]-positione[0])))
    if index == 0:
        new_positione[1] += 1
    elif index == 1:
        new_positione[0] += 1
        new_positione[1] += 1
    elif index == 2:
        new_positione[0] += 1
    elif index == 3:
        new_positione[0] += 1
        new_positione[1] -= 1
    elif index == 4:
        new_positione[1] -= 1
    elif index == 5:
        new_positione[0] -= 1
        new_positione[1] -= 1
    elif index == 6:
        new_positione[0] -= 1
    elif index == 7:
        new_positione[0] -= 1
        new_positione[1] += 1

    new_distance = distance(new_positione, target_positione)

    return new_distance


def trackereUpdate(index, new_position):
    x, y = np.copy(new_position)  

    if index == 0:
        y += 1
    elif index == 1:
        x += 1
        y += 1
    elif index == 2:
        x += 1
    elif index == 3:
        x += 1
        y -= 1
    elif index == 4:
        y -= 1
    elif index == 5:
        x -= 1
        y -= 1
    elif index == 6:
        x -= 1
    elif index == 7:
        x -= 1
        y += 1

    return x, y  # Return the updated position


# DICTIONARIES----------------------
movement_functions = {
    0: oneFronte,  # Complement of 4
    1: frontRighte,  # Compliment of 5
    2: oneRighte,  # complement of 6
    3: backRighte,  # complement of
    4: oneBacke,
    5: backLefte,
    6: oneLefte,
    7: frontLefte
}


# --------------------------------------
grid_size = 25  # Set the size of each grid cell
map_size = 50  # Set the size of the map
occupancy_map = np.zeros((map_size, map_size), dtype=int)

# ... (your existing code)


def nth_minimum_index(arr, n):
    """
    Calculate the index of the nth minimum value in an array.

    Parameters:
    - arr (list): The input array.
    - n (int): The desired rank of the minimum value (0-based index).

    Returns:
    - int: The index of the nth minimum value.
    """
    if n < 0 or n >= len(arr):
        raise ValueError("Invalid value for 'n'")

    # Use sorted function to get the sorted version of the array
    sorted_arr = sorted(enumerate(arr), key=lambda x: x[1])

    # Extract the index of the nth minimum value
    nth_min_index = sorted_arr[n][0]

    return nth_min_index

# Example usage:


# Example usage:


_, positione = sim.simxGetObjectPosition(
    client_id, ball_handleee, -1, sim.simx_opmode_streaming)
time.sleep(0.1)
_, positione = sim.simxGetObjectPosition(
    client_id, ball_handleee, -1, sim.simx_opmode_buffer)
print(positione)
visitse = []
trackere = [0, 0]
temptrackere = []
estimatedcoste = [0, 0, 0, 0, 0, 0, 0, 0]
sofarvisitse=[]
sofarintegervisitse=[]
o=0
target_positione = [9, 9, 0]
grid = np.zeros([25, 25], dtype=int)

_, positione = sim.simxGetObjectPosition(
    client_id, ball_handleee, -1, sim.simx_opmode_streaming)
time.sleep(0.1)
_, positione = sim.simxGetObjectPosition(
    client_id, ball_handleee, -1, sim.simx_opmode_buffer)
rows = 10
cols = 10
start=()
start=(10,0)
robotse = [start, (9, 9)]
valid_pointse=[]
trackereVal=(0,1)
oe=0
positione=[10,10,5.5]
# while (abs(positione[0] - target_positione[0]) > 0.4 or abs(positione[1] - target_positione[1]) > 0.4):
while True:
    # print("visitse: " + str(visitse))
    # print("trackere" + str(trackere))
    sofarvisitse.append((round(positione[1]), round(positione[0])))
    sofarintegervisitse.append((int(positione[1]), int(positione[0])))
    estimatedcoste = [0, 0, 0, 0, 0, 0, 0, 0]
    # _, positione = sim.simxGetObjectPosition(
    #     client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    # time.sleep(0.1)
    # _, positione = sim.simxGetObjectPosition(
    #     client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    print("position:", positione)
    sensorState = []
    for i in range(8):
        estimatedcoste[i] += cost(i, positione)
        sensorState.append(collisione(sensor_handlees.get(i)))

    print("sensors" + str(sensorState))

    min_coste = float('inf')
    optimal_indexe = 0  # Assume no optimal index initially

    for i in range(len(sensorState)):
        if (sensorState[i]):
            estimatedcoste[i] += 1000

    n = 1
    min_coste = 0
    min_coste = float('inf')
    optimal_indexe = -1

    for i in range(len(estimatedcoste)):
        if estimatedcoste[i] <= min_coste:
            # Update min_coste and optimal_indexe when a smaller cost is found
            min_coste = estimatedcoste[i]
            optimal_indexe = i
        # Update visitse_count based on the selected optimal_indexe
    print("cost" + str(estimatedcoste))

    movement_functions[optimal_indexe]()
    trackere = trackereUpdate(optimal_indexe, trackere)

    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    print(positione)

    time.sleep(0.1)

    
    # Start streaming the signal
    resulte, datae = sim.simxGetStringSignal(
        client_id, 'pointse', sim.simx_opmode_streaming)
    time.sleep(3)
    # Receive the streamed signal
    resulte, datae = sim.simxGetStringSignal(
        client_id, 'pointse', sim.simx_opmode_buffer)
    import cbor2
    unpacked_datae = cbor2.loads(datae)

    # Print the unpacked data (assuming it's a dictionary)
    print(unpacked_datae)
    x_valuese = [coord[0] for coord in unpacked_datae]
    y_valuese = [coord[1] for coord in unpacked_datae]
    

    def round_to_nearest_half(number):
        return round(number * 2) / 2
    x_valuese = [round_to_nearest_half(xvals) for xvals in x_valuese]
    y_valuese = [round_to_nearest_half(yvals) for yvals in y_valuese]
    print("xvaluese:")
    print(x_valuese)
    print("yvaluese")
    print(y_valuese)

    pointse = [[x_valuese[i], y_valuese[i]]for i in range(len(x_valuese))]

    # Remove duplicates
    unique_pointsee = list(set(map(tuple, pointse)))

    # Convert back to list of lists
    unique_pointsee = [list(point) for point in unique_pointsee]

    print("Original pointse:", pointse)
    print("pointse without duplicates:", unique_pointsee)

    print(unique_pointsee)
    filtered_pointse = [[point[0], point[1]] for point in unique_pointsee if (
        (point[0] != point[0]//1) or (point[1] != point[1]//1))]

    
    
    print("Position:", positione)
    for i in range(len(filtered_pointse)):
        subject = filtered_pointse[i]
        if (subject[0] % 1 == 0):
            if (positione[0] < subject[0]):
                filtered_pointse[i][0] += 0.5
            else:
                filtered_pointse[i][0] -= 0.5
        if (subject[1] % 1 == 0):
            if (positione[1] < subject[1]):
                filtered_pointse[i][1] += 0.5
            else:
                filtered_pointse[i][1] -= 0.5

    # Remove duplicates
    unique_pointsee = list(set(map(tuple, filtered_pointse)))

    # Convert back to list of lists
    filtered_pointse = [list(point) for point in unique_pointsee]

    print("Filtered pointse:", filtered_pointse)
    print("position:", positione)

    grid_resolution = 1.0  # Assuming obstacles are 1x1
    valid_pointse.extend([(int(point[1]), int(point[0])) for point in filtered_pointse])
    valid_pointse.extend([(round(positione[1]),round(positione[0]))])
    valid_pointse.extend([(10,10)])
    m = 0.1

    darp_visualizer = DARPVisualizer(rows, cols, robotse, valid_pointse, m)
    robot_indexe = 2  # Replace with the desired robot index
    robot_pointse = darp_visualizer.get_points_for_robot(robot_indexe)
    darp_visualizer.visualize_darp()

    # Choose target position such that the distance between robots and target is minimized
    min_distance = float('inf')
    for i in range(len(robot_pointse)):
        distance_to_robot = ((robot_pointse[i][0] - positione[0])**2 + (robot_pointse[i][1] - positione[1])**2)**0.5
        print("min distances:", min_distance)
        print("distanceto:", distance_to_robot)
        print("robots",robotse)
        print("tobe bisited:", robot_pointse)
        if distance_to_robot < min_distance:
            if min_distance!=0:
                min_distance = distance_to_robot
            
            target_positione = robot_pointse[i]

    print("tovisit", robot_pointse)
    print("taget",target_positione)
    sofarvisitse.append((round(positione[1]), round(positione[0])))
    sofarintegervisitse.append((int(positione[1]), int(positione[0])))
    robots=[start,(int(positione[1]),int(positione[0]))]
    print("position:", positione)
    oe+=1
    plt.show()

    

# import matplotlib.pyplot as plt
# import numpy as np

# Assuming 'grid' and 'grid_size' are defined earlier in your code
# for point in valid_pointse:
#         x, y = point
#         grid[x][y] = 1
# plt.imshow(1 - grid, cmap='gray', origin='lower', extent=[0, grid_size, 0, grid_size], vmin=0, vmax=1)

# Add grid lines
# plt.grid(color='black', linestyle='-', linewidth=1)

# Set axis ticks to go up by 1s
# plt.xticks(np.arange(0, grid_size + 1, step=1))
# plt.yticks(np.arange(0, grid_size + 1, step=1))

# plt.title('Occupancy Grid Map')
# plt.xlabel('Grid X')
# plt.ylabel('Grid Y')

# Save the image
# plt.savefig('occupancy_grid_map.png')

# Show the plot
# plt.show()

# frontRighte()
# _,position=sim.simxGetObjectPosition(client_id, ball_handleee,-1, sim.simx_opmode_streaming)
# time.sleep(0.1)
# _,position=sim.simxGetObjectPosition(client_id, ball_handleee,-1, sim.simx_opmode_buffer)
# print(np.sqrt(positione[0]**2+positione[1]**2))
plt.close()
x_sofarvisitse = [point[0] for point in sofarvisitse]
y_sofarvisitse = [point[1] for point in sofarvisitse]

x_sofarintegervisitse = [point[0] for point in sofarintegervisitse]
y_sofarintegervisitse = [point[1] for point in sofarintegervisitse]
# Create a scatter plot
plt.scatter(x_sofarvisitse, y_sofarvisitse, color='blue', label='sofarvisitse')
plt.scatter(x_sofarintegervisitse, y_sofarintegervisitse, color='red', label='sofarintegervisitse')

# Connect the pointse with lines
plt.plot(x_sofarvisitse, y_sofarvisitse, linestyle='-', color='blue')
plt.plot(x_sofarintegervisitse, y_sofarintegervisitse, linestyle='-', color='red')

# Add labels and legend
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()

# Show the plot
plt.show()
# END-----------------------------------