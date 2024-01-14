# INIT----------------------------------------------
import math
import time
import sim
import numpy as np
from PIL import Image

import matplotlib.pyplot as plt
ip = '127.0.0.1'
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
_, bottomCamera= sim.simxGetObjectHandle(client_id, './Vision_sensor', sim.simx_opmode_blocking)
_,_, image= sim.simxGetVisionSensorImage(client_id,bottomCamera,0,sim.simx_opmode_streaming)
time.sleep(0.1)
_,_, image= sim.simxGetVisionSensorImage(client_id,bottomCamera,0,sim.simx_opmode_buffer)

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
#     sim.simxSetObjectPosition(client_id, ball_handle, -1, [position[0],position[1],position[2]+0.1], sim.simx_opmode_blocking)

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
#         sim.simxSetObjectPosition(client_id,ball_handle,-1,[position[0],position[1],position[2]+0.1],sim.simx_opmode_oneshot)
#         _,position=sim.simxGetObjectPosition(client_id, ball_handle,-1, sim.simx_opmode_buffer)
#         time.sleep(0.1)

def collision_distance(i):
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    time.sleep(0.1)
    _,_,detectDist, _, _ = sim.simxReadProximitySensor(
        client_id, sensor_handles[i], sim.simx_opmode_streaming)
    time.sleep(1)
    _,_,detectDist, _, _ = sim.simxReadProximitySensor(
        client_id, sensor_handles[i], sim.simx_opmode_buffer)
    if(distance(detectDist,position)<0.1):
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

    while (position[1] > init and not collision(sensor_handles[4])):
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(
            client_id, ball_handle, -1, [position[0], position[1]-0.1, position[2]], sim.simx_opmode_oneshot)
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
            client_id, ball_handle, -1, [position[0], position[1]+0.1, position[2]], sim.simx_opmode_oneshot)
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
            client_id, ball_handle, -1, [position[0]+0.1, position[1], position[2]], sim.simx_opmode_oneshot)
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
            client_id, ball_handle, -1, [position[0]-0.1, position[1], position[2]], sim.simx_opmode_oneshot)
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
    if(target_position[0]-position[0]==0):
        theta=np.pi/2
    else:
        theta = np.arctan(
        abs((target_position[1]-position[1])/(target_position[0]-position[0])))

    while position[0]<init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handle, -1, [position[0]+0.1, position[1]-0.1, position[2]], sim.simx_opmode_oneshot)
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
    if(target_position[0]-position[0]==0):
        theta=np.pi/2
    else:
        theta = np.arctan(
        abs((target_position[1]-position[1])/(target_position[0]-position[0])))

    while position[0]>init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handle, -1, [position[0]-0.1, position[1]-0.1, position[2]], sim.simx_opmode_oneshot)
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
    if(target_position[0]-position[0]==0):
        theta=np.pi/2
    else:
        theta = np.arctan(
        abs((target_position[1]-position[1])/(target_position[0]-position[0])))
    while position[0]<init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handle, -1, [position[0]+0.1, position[1]+0.1, position[2]], sim.simx_opmode_oneshot)
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
    if(target_position[0]-position[0]==0):
        theta=np.pi/2
    else:
        theta = np.arctan(
        abs((target_position[1]-position[1])/(target_position[0]-position[0])))
    while position[0] > init:
        _, position = sim.simxGetObjectPosition(
            client_id, ball_handle, -1, sim.simx_opmode_buffer)
        sim.simxSetObjectPosition(client_id, ball_handle, -1, [position[0]-0.1, position[1]+0.1, position[2]], sim.simx_opmode_oneshot)
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
    if(target_position[0]-position[0]==0):
        theta=np.pi/2
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


def trackerUpdate(index, position):
    # Update the position based on the movement index
    # Create a copy to avoid modifying the input directly
    new_position = position.copy()

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

    return new_position


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
grid_size = 0.5  # Set the size of each grid cell
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
plt.ion()
target_position=[4,4,0]

_, position = sim.simxGetObjectPosition(
    client_id, ball_handle, -1, sim.simx_opmode_streaming)
time.sleep(0.1)
_, position = sim.simxGetObjectPosition(
    client_id, ball_handle, -1, sim.simx_opmode_buffer)
while (abs(position[0] - target_position[0]) > 1 or abs(position[1] - target_position[1]) > 1):
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

    
    print("sensors" + str(sensorState))

    min_cost = float('inf')
    optimal_index = 0  # Assume no optimal index initially

    for i in range(len(sensorState)):
        if (sensorState[i]):
            estimatedcost[i]+=1000
        
            
    n = 1
    min_cost=0
    min_cost = float('inf')
    optimal_index = -1

    for i in range(len(estimatedcost)):
        if estimatedcost[i] <= min_cost:
            # Update min_cost and optimal_index when a smaller cost is found
            min_cost = estimatedcost[i]
            optimal_index = i
        # Update visits_count based on the selected optimal_index
    print("cost" + str(estimatedcost))
    

    # print("opt index" + str(optimal_index))

    # print(visits.count(round(estimatedcost[i], 1)))
    # print(round(estimatedcost[i], 1))

    # if abs(position[0] - target_position[0]) < 1 and abs(position[1] - target_position[1]) < 1:
    #     break

    movement_functions[optimal_index]()
    tracker = trackerUpdate(optimal_index, tracker)

    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_streaming)
    time.sleep(0.1)
    _, position = sim.simxGetObjectPosition(
        client_id, ball_handle, -1, sim.simx_opmode_buffer)
    
    time.sleep(0.1)
    

    time.sleep(1)
    
    # grid_size_x = 100
    # grid_size_y = 100
    # cell_size = 0.1  # Adjust based on your requirements
    # occupancy_grid = [[0 for _ in range(grid_size_y)] for _ in range(grid_size_x)]



    # Read sensor data and update occupancy grid
    # for sensor_handle in sensor_handles:
    #     _, detection_state, _, _, detected_point = sim.simxReadProximitySensor(client_id, sensor_handle, sim.simx_opmode_blocking)

    #     if detection_state and detected_point[2] < 0.5:  # Adjust threshold based on your sensor's specifications
    #         # Detected an obstacle, update the occupancy grid
    #         grid_x = math.floor(detected_point[0] / cell_size) + grid_size_x // 2
    #         grid_y = math.floor(detected_point[1] / cell_size) + grid_size_y // 2

    #         # Check if the calculated indices are within the grid bounds
    #         if 0 <= grid_x < grid_size_x and 0 <= grid_y < grid_size_y:
    #             occupancy_grid[grid_x][grid_y] = 1

# frontRight()
# _,position=sim.simxGetObjectPosition(client_id, ball_handle,-1, sim.simx_opmode_streaming)
# time.sleep(0.1)
# _,position=sim.simxGetObjectPosition(client_id, ball_handle,-1, sim.simx_opmode_buffer)
# print(np.sqrt(position[0]**2+position[1]**2))


# END-----------------------------------
sim.simxFinish(client_id)
print("Connection Closed")


