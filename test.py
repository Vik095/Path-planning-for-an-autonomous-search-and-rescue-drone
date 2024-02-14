# INIT----------------------------------------------
import math
import time
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

# TARGET HANDLE
_, ball_handle = sim.simxGetObjectHandle(
    client_id, './target', sim.simx_opmode_blocking)
_, Floor = sim.simxGetObjectHandle(
    client_id, 'Floor', sim.simx_opmode_blocking)
_, drone = sim.simxGetObjectHandle(
    client_id, 'Quadcopter', sim.simx_opmode_blocking)

# SENSOR HANDLES--------------------------------------------------------------------------------------
_, frontSensor = sim.simxGetObjectHandle(
    client_id, './frontSensor', sim.simx_opmode_blocking)
_, backSensor = sim.simxGetObjectHandle(
    client_id, './backSensor', sim.simx_opmode_blocking)
_, leftSensor = sim.simxGetObjectHandle(
    client_id, './leftSensor', sim.simx_opmode_blocking)
_, rightSensor = sim.simxGetObjectHandle(
    client_id, './rightSensor', sim.simx_opmode_blocking)
_, backRightSensor = sim.simxGetObjectHandle(
    client_id, './backRightSensor', sim.simx_opmode_blocking)
_, frontRightSensor = sim.simxGetObjectHandle(
    client_id, './frontRightSensor', sim.simx_opmode_blocking)
_, frontLeftSensor = sim.simxGetObjectHandle(
    client_id, './frontLeftSensor', sim.simx_opmode_blocking)
_, backLeftSensor = sim.simxGetObjectHandle(
    client_id, './backLeftSensor', sim.simx_opmode_blocking)
# --------------------------------------------------------------------------------------------------------
_, bottomCamera = sim.simxGetObjectHandle(
    client_id, './Vision_sensor', sim.simx_opmode_blocking)
_, _, image = sim.simxGetVisionSensorImage(
    client_id, bottomCamera, 0, sim.simx_opmode_streaming)
time.sleep(0.1)
_, _, image = sim.simxGetVisionSensorImage(
    client_id, bottomCamera, 0, sim.simx_opmode_buffer)

# # Streaming mode for proximity sensors
# _, detectionState, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, backSensor, sim.simx_opmode_streaming)
# time.sleep(5)
# print("Back Sensor Data:")
# _, detectionState, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, backSensor, sim.simx_opmode_buffer)
# print(detectionState)
# print(detectedPoint)
# print(norm)

# # Front sensor streaming mode
# _, detectionState, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, frontSensor, sim.simx_opmode_streaming)
# time.sleep(5)
# print("Front Sensor Data:")
# _, detectionState, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, frontSensor, sim.simx_opmode_buffer)
# print(detectionState)
# print(detectedPoint)
# print(norm)


# _, detectionState, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, rightSensor, sim.simx_opmode_streaming)
# time.sleep(5)
# print("Right Sensor Data:")
# _, detectionState, detectedPoint, _, norm = sim.simxReadProximitySensor(client_id, rightSensor, sim.simx_opmode_buffer)
# print(detectionState)
# print(detectedPoint)
# print(norm)
# def oneUp(handle):
#     _,position=sim.simxGetObjectPosition(client_id, handle,-1, sim.simx_opmode_streaming)
#     time.sleep(2)
#     for i in range(100):
#         _,position=sim.simxGetObjectPosition(client_id, handle,-1, sim.simx_opmode_buffer)
#         sim.simxSetObjectPosition(client_id, handle,-1,[position[0],position[1],position[2]+0.01],sim.simx_opmode_blocking)
#         _,position=sim.simxGetObjectPosition(client_id, handle,-1, sim.simx_opmode_buffer)
# handle = ball_handle  # Assuming ball_handle is defined elsewhere in your code

# handle = ball_handle  # Assuming ball_handle is defined elsewhere in your code
# _, position = sim.simxGetObjectPosition(client_id, ball_handle, -1, sim.simx_opmode_blocking)
# init = position[2]

# while position[2] < 7:
#     _, position = sim.simxGetObjectPosition(client_id, ball_handle, -1, sim.simx_opmode_buffer)
#     # position[2] += 0.01  # Increment the Z coordinate
#     sim.simxSetObjectPosition(client_id, ball_handle, -1, [position[0],position[1],position[2]+0.05], sim.simx_opmode_blocking)

#     _, position = sim.simxGetObjectPosition(client_id, ball_handle, -1, sim.simx_opmode_buffer)

# _,position=sim.simxGetObjectPosition(client_id, ball_handle,-1, sim.simx_opmode_streaming)
# time.sleep(3)
# sim.simxSetObjectPosition(client_id,ball_handle,-1,[1,1,position[2]],sim.simx_opmode_blocking)
# time.sleep(3)
# sim.simxSetObjectPosition(client_id,ball_handle,-1,[1,2,position[2]],sim.simx_opmode_blocking)


# print(collision(frontSensor))
time.sleep(2)


def collision(handle):
    _, detectionState, _, _, _ = sim.simxReadProximitySensor(
        client_id, handle, sim.simx_opmode_streaming)
    time.sleep(0.2)
    _, detectionState, _, _, _ = sim.simxReadProximitySensor(
        client_id, handle, sim.simx_opmode_buffer)
    return detectionState


sensor_handles = {
    0: frontSensor,
    1: frontRightSensor,
    2: rightSensor,
    3: backRightSensor,
    4: backSensor,
    5: backLeftSensor,
    6: leftSensor,
    7: frontLeftSensor
}


def distance(position, target):
    dx = position[0]-target[0]
    dy = position[1]-target[1]
    dz = position[2]-target[2]
    dist = np.sqrt((dx**2)+(dy**2))
    return dist


target_position = [20, +25, 5]
# def oneUp():
#     _,position=sim.simxGetObjectPosition(client_id, ball_handle,-1, sim.simx_opmode_streaming)
#     time.sleep(0.1)
#     _,position=sim.simxGetObjectPosition(client_id, ball_handle,-1, sim.simx_opmode_buffer)
#     time.sleep(0.1)
#     init = position[2]+1

#     while position[2]<init:
#         _,position=sim.simxGetObjectPosition(client_id, ball_handle,-1, sim.simx_opmode_buffer)
#         sim.simxSetObjectPosition(client_id,ball_handle,-1,[position[0],position[1],position[2]+0.05],sim.simx_opmode_oneshot)
#         _,position=sim.simxGetObjectPosition(client_id, ball_handle,-1, sim.simx_opmode_buffer)
#         time.sleep(0.1)


def collision_distance(i):
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    _, _, detectDist, _, _ = sim.simxReadProximitySensor(
        client_id, sensor_handles[i], sim.simx_opmode_streaming)
    time.sleep(1)
    _, _, detectDist, _, _ = sim.simxReadProximitySensor(
        client_id, sensor_handles[i], sim.simx_opmode_buffer)
    if (distance(detectDist, position) < 0.05):
        return False
    else:
        return True


def oneBack():
    # ID=1
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = position[1]-1

    while (position[1] > init):
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(
            client_id, ball_handle, -1, [position[0], position[1]-0.05, position[2]], sim.simx_opmode_oneshot)
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


def oneFront():
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = position[1]+1

    while (position[1] < init):
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(
            client_id, ball_handle, -1, [position[0], position[1]+0.05, position[2]], sim.simx_opmode_oneshot)
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


def oneRight():

    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = position[0]+1

    while position[0] <= init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(
            client_id, ball_handle, -1, [position[0]+0.05, position[1], position[2]], sim.simx_opmode_oneshot)
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


def oneLeft():
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = position[0]-1

    while position[0] > init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(
            client_id, ball_handle, -1, [position[0]-0.05, position[1], position[2]], sim.simx_opmode_oneshot)
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


# def backRight():

#     _, position = sim.simxGetObjectPosition(
#         client_id, ball_handle, -1, sim.simx_opmode_streaming)
#     time.sleep(0.1)
#     _, position = sim.simxGetObjectPosition(
#         client_id, ball_handle, -1, sim.simx_opmode_buffer)
#     time.sleep(0.1)
#     init = position.copy()
#     if(target_position[0]-position[0]==0):
#         theta=np.pi/2
#     else:
#         theta = np.arctan(
#         abs((target_position[1]-position[1])/(target_position[0]-position[0])))

#     while distance(position, init) < 1:
#         _, position = sim.simxGetObjectPosition(
#             client_id, ball_handle, -1, sim.simx_opmode_buffer)
#         sim.simxSetObjectPosition(client_id, ball_handle, -1, [position[0]+abs(np.cos(
#             theta))/20, position[1]-1/20, position[2]], sim.simx_opmode_oneshot)
#         _, position = sim.simxGetObjectPosition(
#             client_id, ball_handle, -1, sim.simx_opmode_buffer)
#         time.sleep(0.1)

def backRight():

    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = position[0]+1
    if (target_position[0]-position[0] == 0):
        theta = np.pi/2
    else:
        theta = np.arctan(
            abs((target_position[1]-position[1])/(target_position[0]-position[0])))

    while position[0] < init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handle, -1, [
                                  position[0]+0.05, position[1]-0.05, position[2]], sim.simx_opmode_oneshot)
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


# def backLeft():

#     _, position = sim.simxGetObjectPosition(
#         client_id, ball_handle, -1, sim.simx_opmode_streaming)
#     time.sleep(0.1)
#     _, position = sim.simxGetObjectPosition(
#         client_id, ball_handle, -1, sim.simx_opmode_buffer)
#     time.sleep(0.1)
#     init = position.copy()
#     if(target_position[0]-position[0]==0):
#         theta=np.pi/2
#     else:
#         theta = np.arctan(
#         abs((target_position[1]-position[1])/(target_position[0]-position[0])))

#     while distance(position, init) < 1:
#         _, position = sim.simxGetObjectPosition(
#             client_id, ball_handle, -1, sim.simx_opmode_buffer)
#         sim.simxSetObjectPosition(client_id, ball_handle, -1, [position[0]-abs(np.cos(
#             theta))/20, position[1]-1/20, position[2]], sim.simx_opmode_oneshot)
#         _, position = sim.simxGetObjectPosition(
#             client_id, ball_handle, -1, sim.simx_opmode_buffer)
#         time.sleep(0.1)

def backLeft():

    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = position[0]-1
    if (target_position[0]-position[0] == 0):
        theta = np.pi/2
    else:
        theta = np.arctan(
            abs((target_position[1]-position[1])/(target_position[0]-position[0])))

    while position[0] > init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handle, -1, [
                                  position[0]-0.05, position[1]-0.05, position[2]], sim.simx_opmode_oneshot)
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


# def frontRight():

#     _, position = sim.simxGetObjectPosition(
#         client_id, ball_handle, -1, sim.simx_opmode_streaming)
#     time.sleep(0.1)
#     _, position = sim.simxGetObjectPosition(
#         client_id, ball_handle, -1, sim.simx_opmode_buffer)
#     time.sleep(0.1)
#     init = position.copy()
#     if(target_position[0]-position[0]==0):
#         theta=np.pi/2
#     else:
#         theta = np.arctan(
#         abs((target_position[1]-position[1])/(target_position[0]-position[0])))
#     while distance(position, init) < 1:
#         _, position = sim.simxGetObjectPosition(
#             client_id, ball_handle, -1, sim.simx_opmode_buffer)
#         sim.simxSetObjectPosition(client_id, ball_handle, -1, [position[0]+abs(np.cos(
#             theta))/20, position[1]+1/20, position[2]], sim.simx_opmode_oneshot)
#         _, position = sim.simxGetObjectPosition(
#             client_id, ball_handle, -1, sim.simx_opmode_buffer)
#         time.sleep(0.1)

def frontRight():

    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = position[0]+1
    if (target_position[0]-position[0] == 0):
        theta = np.pi/2
    else:
        theta = np.arctan(
            abs((target_position[1]-position[1])/(target_position[0]-position[0])))
    while position[0] < init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handle, -1, [
                                  position[0]+0.05, position[1]+0.05, position[2]], sim.simx_opmode_oneshot)
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


def frontLeft():

    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    init = position[0]-1
    if (target_position[0]-position[0] == 0):
        theta = np.pi/2
    else:
        theta = np.arctan(
            abs((target_position[1]-position[1])/(target_position[0]-position[0])))
    while position[0] > init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handle, -1, [
                                  position[0]-0.05, position[1]+0.05, position[2]], sim.simx_opmode_oneshot)
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


# def velocity():
#     _, linearVelocity,_=sim.simxGetObjectVelocity(client_id,drone,sim.simx_opmode_streaming)
#     time.sleep(0.1)
#     _, linearVelocity,_=sim.simxGetObjectVelocity(client_id,drone,sim.simx_opmode_buffer)
#     print(linearVelocity)
#     return linearVelocity


def cost(index, position):
    # Update the position based on the movement index
    # Create a copy to avoid modifying the input directly
    new_position = position.copy()
    if (target_position[0]-position[0] == 0):
        theta = np.pi/2
    else:
        theta = np.arctan(
            abs((target_position[1]-position[1])/(target_position[0]-position[0])))
    if index == 0:
        new_position[1] += 1
    elif index == 1:
        new_position[0] += 1
        new_position[1] += 1
    elif index == 2:
        new_position[0] += 1
    elif index == 3:
        new_position[0] += 1
        new_position[1] -= 1
    elif index == 4:
        new_position[1] -= 1
    elif index == 5:
        new_position[0] -= 1
        new_position[1] -= 1
    elif index == 6:
        new_position[0] -= 1
    elif index == 7:
        new_position[0] -= 1
        new_position[1] += 1

    new_distance = distance(new_position, target_position)

    return new_distance


def trackerUpdate(index, new_position):
    # Update the position based on the movement index
    # Create a copy to avoid modifying the input directly

    x, y = np.copy(new_position)  # Unpack the coordinates

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
    0: oneFront,  # Complement of 4
    1: frontRight,  # Compliment of 5
    2: oneRight,  # complement of 6
    3: backRight,  # complement of
    4: oneBack,
    5: backLeft,
    6: oneLeft,
    7: frontLeft
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
# TARGET handlee
_, ball_handleee = sim.simxGetObjectHandle(
    client_id, './targete', sim.simx_opmode_blocking)
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

    while (positione[1] >= init):
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


def coste(index, position):

    new_positione = positione.copy()
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
movement_functionse = {
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


_, position = sim.simxGetObjectPosition(
    client_id, ball_handle, -1, sim.simx_opmode_streaming)
time.sleep(0.1)
_, position = sim.simxGetObjectPosition(
    client_id, ball_handle, -1, sim.simx_opmode_buffer)
print("Position of drone 1: ",position)
visits = []
tracker = [0, 0]
tempTracker = []
estimatedcost = [0, 0, 0, 0, 0, 0, 0, 0]

target_position = [1, 0, 0]
grid = np.zeros([25, 25], dtype=int)

_, position = sim.simxGetObjectPosition(
    client_id, ball_handle, -1, sim.simx_opmode_streaming)
time.sleep(0.1)
_, position = sim.simxGetObjectPosition(
    client_id, ball_handle, -1, sim.simx_opmode_buffer)
rows = 10
cols = 10
start = ()
start = (0, 0)
robots = [start, (9, 9)]
valid_points = []
trackerVal = (0, 1)
o = 0
_, positione = sim.simxGetObjectPosition(
    client_id, ball_handleee, -1, sim.simx_opmode_streaming)
time.sleep(0.1)
_, positione = sim.simxGetObjectPosition(
    client_id, ball_handleee, -1, sim.simx_opmode_buffer)
print("Position of drone 2: ", positione)
visitse = []
trackere = [0, 0]
temptrackere = []
estimatedcoste = [0, 0, 0, 0, 0, 0, 0, 0]
sofarvisitse = []
sofarintegervisitse = []
sofarvisits = []
sofarintegervisits = []
o = 0
target_positione = [4, 5, 0]
grid = np.zeros([25, 25], dtype=int)

_, positione = sim.simxGetObjectPosition(
    client_id, ball_handleee, -1, sim.simx_opmode_streaming)
time.sleep(0.1)
_, positione = sim.simxGetObjectPosition(
    client_id, ball_handleee, -1, sim.simx_opmode_buffer)
rows = 5
cols = 5
start = ()
start = (0, 0)
robotse = [start, (4, 4)]
valid_pointse = []
trackereVal = (0, 1)
oe = 0
positione = [5, 5, 5.5]
# while (abs(position[0] - target_position[0]) > 0.4 or abs(position[1] - target_position[1]) > 0.4):
while True:
    # print("visits: " + str(visits))
    # print("tracker" + str(tracker))

    estimatedcost = [0, 0, 0, 0, 0, 0, 0, 0]
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)

    sensorState = []
    for i in range(8):
        estimatedcost[i] += cost(i, position)
        sensorState.append(collision(sensor_handles.get(i)))

    # print("sensors" + str(sensorState))

    min_cost = float('inf')
    optimal_index = 0  # Assume no optimal index initially

    for i in range(len(sensorState)):
        if (sensorState[i]):
            estimatedcost[i] += 1000
    estimatedcoste = [0, 0, 0, 0, 0, 0, 0, 0]

    n = 1
    min_cost = 0
    min_cost = float('inf')
    optimal_index = -1

    for i in range(len(estimatedcost)):
        if estimatedcost[i] <= min_cost:
            # Update min_cost and optimal_index when a smaller cost is found
            min_cost = estimatedcost[i]
            optimal_index = i
        # Update visits_count based on the selected optimal_index
    # print("cost" + str(estimatedcost))

    movement_functions[optimal_index]()
    tracker = trackerUpdate(optimal_index, tracker)

    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)

    time.sleep(0.1)

    # Start streaming the signal
    result, data = sim.simxGetStringSignal(
        client_id, 'points', sim.simx_opmode_streaming)
    time.sleep(3)
    # Receive the streamed signal
    result, data = sim.simxGetStringSignal(
        client_id, 'points', sim.simx_opmode_buffer)
    import cbor2
    unpacked_data = cbor2.loads(data)

    # Print the unpacked data (assuming it's a dictionary)
    # print(unpacked_data)
    x_values = [coord[0] for coord in unpacked_data]
    y_values = [coord[1] for coord in unpacked_data]

    def round_to_nearest_half(number):
        return round(number * 2) / 2
    x_values = [round_to_nearest_half(xvals) for xvals in x_values]
    y_values = [round_to_nearest_half(yvals) for yvals in y_values]
    # print("xvalues:")
    # print(x_values)
    # print("yvalues")
    # print(y_values)

    points = [[x_values[i], y_values[i]]for i in range(len(x_values))]

    # Remove duplicates
    unique_points = list(set(map(tuple, points)))

    # Convert back to list of lists
    unique_points = [list(point) for point in unique_points]

    # print("Original points:", points)
    # print("Points without duplicates:", unique_points)

    # print(unique_points)
    filtered_points = [[point[0], point[1]] for point in unique_points if (
        (point[0] != point[0]//1) or (point[1] != point[1]//1))]

    print("Position of drone 1:", position)
    for i in range(len(filtered_points)):
        subject = filtered_points[i]
        if (subject[0] % 1 == 0):
            if (position[0] < subject[0]):
                filtered_points[i][0] += 0.5
            else:
                filtered_points[i][0] -= 0.5
        if (subject[1] % 1 == 0):
            if (position[1] < subject[1]):
                filtered_points[i][1] += 0.5
            else:
                filtered_points[i][1] -= 0.5

    # Remove duplicates
    unique_points = list(set(map(tuple, filtered_points)))

    # Convert back to list of lists
    filtered_points = [list(point) for point in unique_points]

    # print("Filtered points:", filtered_points)
    # print(position)

    grid_resolution = 1.0  # Assuming obstacles are 1x1
    valid_points.extend((int(point[0]), int(point[1]))
                        for point in filtered_points)
    valid_points.extend([(int(position[0]), int(position[1]))])
    # valid_points.extend([(round(position[0]),round(position[1]))])
    valid_points.extend([(0, 0)])
    m = 0.1

    darp_visualizer = DARPVisualizer(rows, cols, robots, valid_points, m)
    robot_index = 1
    robot_points = darp_visualizer.get_points_for_robot(robot_index)
    darp_visualizer.visualize_darp()

    min_distance = float('inf')
    if len(robot_points)==0:
        print("lmao")
        
    for i in range(len(robot_points)):
        if tuple((robot_points[i][0],robot_points[i][1])) not in valid_points:
    
            target_position=robot_points[i]
            break


    # print("tovisit", robot_points)
    print("target of drone 1", target_position)
    robots = [(int(position[0]), int(position[1])), robots[1]]
    # print("visitse: " + str(visitse))
    # print("trackere" + str(trackere))
    sofarvisitse.append((round(positione[1]), round(positione[0])))
    sofarintegervisitse.append((int(positione[0]), int(positione[1])))
    estimatedcoste = [0, 0, 0, 0, 0, 0, 0, 0]
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    print("position of drone 2:", positione)
    sensorState = []
    print("target for drone 2:",target_positione)
    for i in range(8):
        estimatedcoste[i] += coste(i, positione)
        sensorState.append(collisione(sensor_handlees.get(i)))

    # print("sensors" + str(sensorState))

    min_coste = float('inf')
    optimal_indexe = 0  # Assume no optimal index initially

    for i in range(len(sensorState)):
        if (sensorState[i]):
            estimatedcoste[i] += 1000

    n = 1
    min_coste = 0
    min_coste = float('inf')
    optimal_indexe = -1

    for k in range(len(estimatedcoste)):
        if estimatedcoste[k] <= min_coste:
            # Update min_coste and optimal_indexe when a smaller cost is found
            min_coste = estimatedcoste[k]
            optimal_indexe = k
        # Update visitse_count based on the selected optimal_indexe
    # print("cost" + str(estimatedcoste))

    movement_functionse[optimal_indexe]()
    trackere = trackereUpdate(optimal_indexe, trackere)

    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    print("position of drone 2",positione)

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
    # print(unpacked_datae)
    x_valuese = [coord[0] for coord in unpacked_datae]
    y_valuese = [coord[1] for coord in unpacked_datae]

    def round_to_nearest_half(number):
        return round(number * 2) / 2
    x_valuese = [round_to_nearest_half(xvals) for xvals in x_valuese]
    y_valuese = [round_to_nearest_half(yvals) for yvals in y_valuese]
    # print("xvaluese:")
    # print(x_valuese)
    # print("yvaluese")
    # print(y_valuese)

    pointse = [[x_valuese[i], y_valuese[i]]for i in range(len(x_valuese))]

    # Remove duplicates
    unique_pointsee = list(set(map(tuple, pointse)))

    # Convert back to list of lists
    unique_pointsee = [list(point) for point in unique_pointsee]

    # print("Original pointse:", pointse)
    # print("pointse without duplicates:", unique_pointsee)

    # print(unique_pointsee)
    filtered_pointse = [[point[0], point[1]] for point in unique_pointsee if (
        (point[0] != point[0]//1) or (point[1] != point[1]//1))]

    
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

    # print("Filtered pointse:", filtered_pointse)
    # print("position:", positione)

    grid_resolution = 1.0  # Assuming obstacles are 1x1
    valid_points.extend([(int(point[0]), int(point[1]))
                        for point in filtered_pointse])
    valid_points.extend([(round(positione[0]), round(positione[1]))])
    valid_points.extend([(10, 10)])
    m = 0.1

    robot_index = 2  # Replace with the desired robot index
    robot_pointse = darp_visualizer.get_points_for_robot(robot_index)
    darp_visualizer.visualize_darp()
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, positione = sim.simxGetObjectPosition(
        client_id, ball_handleee, -1, sim.simx_opmode_buffer)
    print("position of drone 2",positione)

    
    robot_index = 2
    robot_points = darp_visualizer.get_points_for_robot(robot_index)
    

    min_distance = float('inf')
    if len(robot_points)==0:
        print("lmao")
    
    for i in range(len(robot_points)):
        if tuple((robot_points[i][0],robot_points[i][1])) not in valid_points:
    
            target_positione=robot_points[i]
            break

    # print("tovisit", robot_pointse)
    print("taget for drone 2;", target_positione)
    sofarvisitse.append((round(positione[1]), round(positione[0])))
    sofarintegervisits.append((int(positione[0]), int(positione[1])))
    robots = [robots[0], (round((positione[0])),round((positione[1])))]
    valid_points.extend((round((positione[0])),round((positione[1]))))
    print("position of drone 2:", positione)
    

# import matplotlib.pyplot as plt
# import numpy as np

# # Assuming 'grid' and 'grid_size' are defined earlier in your code
# for point in valid_points:
#         x, y = point
#         grid[x][y] = 1
# plt.imshow(1 - grid, cmap='gray', origin='lower', extent=[0, grid_size, 0, grid_size], vmin=0, vmax=1)

# # Add grid lines
# plt.grid(color='black', linestyle='-', linewidth=1)

# # Set axis ticks to go up by 1s
# plt.xticks(np.arange(0, grid_size + 1, step=1))
# plt.yticks(np.arange(0, grid_size + 1, step=1))

# plt.title('Occupancy Grid Map')
# plt.xlabel('Grid X')
# plt.ylabel('Grid Y')

# Save the image
# plt.savefig('occupancy_grid_map.png')

# Show the plot
x_sofarvisits = [point[0] for point in sofarvisits]
y_sofarvisits = [point[1] for point in sofarvisits]

x_sofarintegervisits = [point[0] for point in sofarintegervisits]
y_sofarintegervisits = [point[1] for point in sofarintegervisits]
print(x_sofarintegervisits)
print(y_sofarintegervisits)
plt.scatter(x_sofarintegervisits, y_sofarintegervisits)
plt.show()
# frontRight()
# _,position=sim.simxGetObjectPosition(client_id, ball_handle,-1, sim.simx_opmode_streaming)
# time.sleep(0.1)
# _,position=sim.simxGetObjectPosition(client_id, ball_handle,-1, sim.simx_opmode_buffer)
# print(np.sqrt(position[0]**2+position[1]**2))


# END-----------------------------------
