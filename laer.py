

import json

import numpy as np
import sim
import time
import tkinter as tk

# Connect to V-REP
clientID = sim.simxStart('127.0.0.1', 19999 , True, True, 5000, 5)

import sim
import time

# Assuming 'clientID' is the client connection ID

# Start streaming the signal
import sim
import struct
import time

# Assuming 'clientID' is the client connection ID

# Start streaming the signal 
result,data = sim.simxGetStringSignal(clientID, 'points', sim.simx_opmode_streaming)
time.sleep(0.1)
    # Receive the streamed signal
result, data = sim.simxGetStringSignal(clientID, 'points', sim.simx_opmode_buffer)
import cbor2
unpacked_data = cbor2.loads(data)

# Print the unpacked data (assuming it's a dictionary)
print(unpacked_data)
x_values = [coord[0] for coord in unpacked_data]
y_values = [coord[1] for coord in unpacked_data]
def round_to_nearest_half(number):
    return round(number * 2) / 2
x_values=[round_to_nearest_half(xvals) for xvals in x_values]
y_values=[round_to_nearest_half(yvals) for yvals in y_values]
print("xvalues:")
print(x_values)
print("yvalues")
print(y_values)
points=[[x_values[i],y_values[i]]for i in range(len(x_values))]


# Remove duplicates
unique_points = list(set(map(tuple, points)))

# Convert back to list of lists
unique_points = [list(point) for point in unique_points]

print("Original points:", points)
print("Points without duplicates:", unique_points)

print(unique_points)
filtered_points=[[int(point[0]),int(point[1])] for point in unique_points if ((point[0]!=point[0]//1) or (point[1]!=point[1]//1))]

print("Unique points:", unique_points)
print("Filtered points:", filtered_points)
import matplotlib.pyplot as plt
plt.scatter(x_values,y_values)
grid_resolution = 1.0  # Assuming obstacles are 1x1

# Initialize occupancy grid map
grid=np.zeros([5,5],dtype = int)
gridx=[point[0] for point in filtered_points]
gridy=[point[1] for point in filtered_points]
for i in range(len(gridx)):
    grid[gridy[i]][gridx[i]]=1
grid_size = 5
plt.imshow(1 - grid, cmap='gray', origin='lower', extent=[0, grid_size, 0, grid_size], vmin=0, vmax=1)

# Add grid lines
plt.grid(color='black', linestyle='-', linewidth=1)

# Set axis ticks to go up by 1s
plt.xticks(np.arange(0, 5, step=1))
plt.yticks(np.arange(0, 5, step=1))

plt.title('Occupancy Grid Map')
plt.xlabel('Grid X')
plt.ylabel('Grid Y')

plt.show()
print(filtered_points)