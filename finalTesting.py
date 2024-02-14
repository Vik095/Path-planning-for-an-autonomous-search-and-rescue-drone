# from matplotlib import pyplot as plt
# from mstmodified import DARPVisualizer
# import csv

# rows = 5
# cols = 5
# robots = [(0, 0), (4, 4)]
# obstacles_sets = [
#     [[(2, 3)]],  # 1 point
#     [[(4, 0), (0, 2), (3, 1), (2, 3), (1, 4)]],  # 5 points
#     [[(2, 1), (4, 3), (1, 0), (0, 4), (3, 2), (1, 3), (4, 2), (0, 1), (3, 4)]]
#  # 10 points
# ]

# with open('obstacle_lengths.csv', 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerow(['Obstacle Points', 'Robot 1 Length', 'Robot 2 Length'])

#     for obstacles_set in obstacles_sets:
#         obstacles = obstacles_set[0]  # Extracting the obstacle set
#         m = 0.1
#         print(obstacles_set)
#         darp_visualizer = DARPVisualizer(rows, cols, robots, obstacles_set[0], m)

#         robot1_length = len(darp_visualizer.get_points_for_robot(1))
#         robot2_length = len(darp_visualizer.get_points_for_robot(2))

#         csv_writer.writerow([len(obstacles), robot1_length, robot2_length])

# # xvalues=[point[0] for point in robot_points]
# # yvavlues=[point[1] for point in robot_points]
# # plt.show()
# # plt.plot(xvalues,yvavlues,color='red',linestyle='-', linewidth=1)
# # plt.show()
from matplotlib import pyplot as plt


integer_positions=[(0, 0), (1, 0), (2, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (6, 0), (6, 0), (7, 0), (8, 0), (9, 0), (9, 0), (9, 1), (8, 0), (8, 1), (7, 1), (5, 0), (5, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 0), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 2), (0, 1), (0, 2), (1, 2), (1, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2)]
x_coords = [pos[0] for pos in integer_positions]
y_coords = [pos[1] for pos in integer_positions]

# Plot the integer positions
plt.plot(x_coords, y_coords, color='blue', linewidth=2, label='Integer Positions')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Plot of Integer Positions')
plt.show()