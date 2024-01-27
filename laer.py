

# import json

# import numpy as np
# import sim
# import time
# import tkinter as tk
import matplotlib.pyplot as plt

# # Connect to V-REP
# clientID = sim.simxStart('127.0.0.1', 19999 , True, True, 5000, 5)
# _, ball_handle = sim.simxGetObjectHandle(
#     clientID, './target', sim.simx_opmode_blocking)
# import sim
# import time

# # Assuming 'clientID' is the client connection ID

# # Start streaming the signal
# import sim
# import struct
# import time

# # Assuming 'clientID' is the client connection ID
# _, position = sim.simxGetObjectPosition(
#     clientID, ball_handle, -1, sim.simx_opmode_streaming)
# time.sleep(0.1)
# _, position = sim.simxGetObjectPosition(
#     clientID, ball_handle, -1, sim.simx_opmode_buffer)

# # Start streaming the signal 
# result,data = sim.simxGetStringSignal(clientID, 'points', sim.simx_opmode_streaming)
# time.sleep(3)
#     # Receive the streamed signal
# result, data = sim.simxGetStringSignal(clientID, 'points', sim.simx_opmode_buffer)
# import cbor2
# unpacked_data = cbor2.loads(data)

# # Print the unpacked data (assuming it's a dictionary)
# print(unpacked_data)
# x_values = [coord[0] for coord in unpacked_data]
# y_values = [coord[1] for coord in unpacked_data]
# plt.scatter(x_values,y_values)
# def round_to_nearest_half(number):
#     return round(number * 2) / 2
# x_values=[round_to_nearest_half(xvals) for xvals in x_values]
# y_values=[round_to_nearest_half(yvals) for yvals in y_values]
# print("xvalues:")
# print(x_values)
# print("yvalues")
# print(y_values)

# points=[[x_values[i],y_values[i]]for i in range(len(x_values))]


# # Remove duplicates
# unique_points = list(set(map(tuple, points)))

# # Convert back to list of lists
# unique_points = [list(point) for point in unique_points]

# print("Original points:", points)
# print("Points without duplicates:", unique_points)

# print(unique_points)
# filtered_points=[[point[0],point[1]] for point in unique_points if ((point[0]!=point[0]//1) or (point[1]!=point[1]//1))]

# print("Unique points:", unique_points)
# print("Filtered points:", filtered_points)
# print("Position:", position)
# for i in range(len(filtered_points)):
#     subject=filtered_points[i]
#     if(subject[0]%1==0):
#         if(position[0]<subject[0]):
#             filtered_points[i][0]+=0.5
#         else:
#             filtered_points[i][0]-=0.5
#     if(subject[1]%1==0):
#         if(position[1]<subject[1]):
#             filtered_points[i][1]+=0.5
#         else:
#             filtered_points[i][1]-=0.5


# # Remove duplicates
# unique_points = list(set(map(tuple, filtered_points)))

# # Convert back to list of lists
# filtered_points = [list(point) for point in unique_points]

# print(filtered_points)


# grid_resolution = 1.0  # Assuming obstacles are 1x1
# valid_points=[[int(point[0]),int(point[1])] for point in filtered_points]
# grid=np.zeros([25,25],dtype = int)
# for i in range(len(valid_points)):
#     x=valid_points[i][0]
#     y=valid_points[i][1]
#     grid[y][x]=1
# print(grid)
import numpy as np
import matplotlib.pyplot as plt

# Initialize occupancy grid map with zeros
grid_size = 25
grid = np.zeros((grid_size, grid_size), dtype=int)

# Coordinates to set to 1
coordinates_to_set = [(3, 0), (4, 0), (6, 0)]

# Set specified coordinates to 1
for coord in coordinates_to_set:
    grid[coord[0], coord[1]] = 1

# Visualize the occupancy grid map
plt.imshow(1 - grid, cmap='gray', origin='lower', extent=[0, grid_size, 0, grid_size], vmin=0, vmax=1)

# Add grid lines
plt.grid(color='black', linestyle='-', linewidth=1)

# Set axis ticks to go up by 1s
plt.xticks(np.arange(0, grid_size + 1, step=1))
plt.yticks(np.arange(0, grid_size + 1, step=1))

plt.title('Occupancy Grid Map')
plt.xlabel('Grid X')
plt.ylabel('Grid Y')
plt.show()
