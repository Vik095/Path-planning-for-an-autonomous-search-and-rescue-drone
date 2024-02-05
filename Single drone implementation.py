# INIT----------------------------------------------
import math
import time

import cbor2
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

    while (position[1] >= init and not collision(sensor_handles[4])):
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

    while (position[1] <= init):
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

    while position[0] >= init:
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

    while position[0] <= init:
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

    while position[0] >= init:
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
    while position[0] <= init:
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
    while position[0] >= init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handle, -1, [
                                  position[0]-0.05, position[1]+0.05, position[2]], sim.simx_opmode_oneshot)
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        time.sleep(0.1)


def cost(index, position):

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


_, position = sim.simxGetObjectPosition(
    client_id, ball_handle, -1, sim.simx_opmode_streaming)
time.sleep(0.1)
_, position = sim.simxGetObjectPosition(
    client_id, ball_handle, -1, sim.simx_opmode_buffer)
print(position)
visits = []
tracker = [0, 0]
tempTracker = []
estimatedcost = [0, 0, 0, 0, 0, 0, 0, 0]
sofarvisits = []
sofarintegervisits = []
o = 0
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
start = (10, 0)
robots = [start, (0, 10)]
valid_points = []
trackerVal = (0, 1)
o = 0
# while (abs(position[0] - target_position[0]) > 0.4 or abs(position[1] - target_position[1]) > 0.4):
while True:
    # print("visits: " + str(visits))
    # print("tracker" + str(tracker))
    sofarvisits.append((round(position[1]), round(position[0])))
    sofarintegervisits.append((int(position[1]), int(position[0])))
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
    print("sensors" + str(sensorState))

    min_cost = float('inf')
    optimal_index = 0  # Assume no optimal index initially

    for i in range(len(sensorState)):
        if (sensorState[i]):
            estimatedcost[i] += 1000

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
    print("cost" + str(estimatedcost))

    movement_functions[optimal_index]()
    tracker = trackerUpdate(optimal_index, tracker)

    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)

    time.sleep(0.1)

    result, data = sim.simxGetStringSignal(
        client_id, 'points', sim.simx_opmode_streaming)
    time.sleep(3)

    result, data = sim.simxGetStringSignal(
        client_id, 'points', sim.simx_opmode_buffer)

    unpacked_data = cbor2.loads(data)

    print(unpacked_data)
    x_values = [coord[0] for coord in unpacked_data]
    y_values = [coord[1] for coord in unpacked_data]

    def round_to_nearest_half(number):
        return round(number * 2) / 2
    x_values = [round_to_nearest_half(xvals) for xvals in x_values]
    y_values = [round_to_nearest_half(yvals) for yvals in y_values]
    print("xvalues:")
    print(x_values)
    print("yvalues")
    print(y_values)

    points = [[x_values[i], y_values[i]]for i in range(len(x_values))]

    unique_points = list(set(map(tuple, points)))

    unique_points = [list(point) for point in unique_points]

    print("Original points:", points)
    print("Points without duplicates:", unique_points)

    print(unique_points)
    filtered_points = [[point[0], point[1]] for point in unique_points if (
        (point[0] != point[0]//1) or (point[1] != point[1]//1))]

    print("Position:", position)
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

    unique_points = list(set(map(tuple, filtered_points)))

    filtered_points = [list(point) for point in unique_points]

    print("Filtered points:", filtered_points)
    print(position)

    grid_resolution = 1.0  # Assuming obstacles are 1x1
    valid_points.extend([(int(point[1]), int(point[0]))
                        for point in filtered_points])
    valid_points.extend([(round(position[1]), round(position[0]))])
    valid_points.extend([(0, 0)])
    m = 0.1

    darp_visualizer = DARPVisualizer(rows, cols, robots, valid_points, m)
    robot_index = 1
    robot_points = darp_visualizer.get_points_for_robot(robot_index)
    darp_visualizer.visualize_darp()

    min_distance = float('inf')
    for i in range(len(robot_points)):
        distance_to_robot = ((robot_points[i][0] - int(position[0]))
                             ** 2 + (robot_points[i][1] - int(position[1]))**2)**0.5
        print("min distances:", min_distance)
        print("distanceto:", distance_to_robot)
        print("robots", robots)
        print("tobe bisited:", robot_points)
        if distance_to_robot < min_distance:
            min_distance = distance_to_robot

            target_position = robot_points[i]

    print("tovisit", robot_points)
    print("taget", target_position)
    sofarvisits.append((round(position[1]), round(position[0])))
    sofarintegervisits.append((int(position[1]), int(position[0])))
    robots = [(int(position[1]), int(position[0])), (9, 0)]
    o += 1
    if o > 3:
        break


plt.close()
x_sofarvisits = [point[0] for point in sofarvisits]
y_sofarvisits = [point[1] for point in sofarvisits]

x_sofarintegervisits = [point[0] for point in sofarintegervisits]
y_sofarintegervisits = [point[1] for point in sofarintegervisits]
# Create a scatter plot
plt.scatter(x_sofarvisits, y_sofarvisits, color='blue', label='sofarvisits')
plt.scatter(x_sofarintegervisits, y_sofarintegervisits,
            color='red', label='sofarintegervisits')

plt.plot(x_sofarvisits, y_sofarvisits, linestyle='-', color='blue')
plt.plot(x_sofarintegervisits, y_sofarintegervisits,
         linestyle='-', color='red')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()


plt.show()
# END-----------------------------------
