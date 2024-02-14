from turtle import color
from cv2 import sort, sqrt
import matplotlib.pyplot as plt
import numpy as np
from AreaDivision import DARP


from sympy import true

import math


class DARPVisualizer:
    def __init__(self, rows, cols, robots, obstacles, m):
        self.rows = rows
        self.cols = cols
        self.robots = robots
        self.obstacles = obstacles
        self.m = m
        self.darp_solver = DARP(rows, cols, robots, obstacles, m)

    def visualize_assignment(self):
        self.darp_solver.assign_cells()
        graphi=self.darp_solver.visualize_assignment()
        plt.imshow(graphi, cmap='viridis', interpolation='nearest', origin='lower')  # Convert to float
        plt.title('Assignment Matrix')
        plt.colorbar()
        

        # for i in range(self.rows):
        #     for j in range(self.cols):
        #         # plt.text(j, i, str(graphi[i, j]), color='white', ha='center', va='center')

        # plt.show()
        return graphi

    def create_indices_dict(self, assignment_matrix):
        indices_dict = {}
        num_rows = len(assignment_matrix)
        num_columns = len(assignment_matrix[0])

        for i in range(num_rows):
            for j in range(num_columns):
                element = assignment_matrix[j][i]  # Corrected the index order
                if element != 0:
                    if element in indices_dict:
                        indices_dict[element].append((i, j))
                    else:
                        indices_dict[element] = [(i, j)]

        return indices_dict

    def euclidean_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        if math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) == 1:
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        else:
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def count_turns(self, spanning_tree):
        num_turns = sum(
            1 for edge in spanning_tree if edge[0][0] != edge[1][0] and edge[0][1] != edge[1][1])
        return num_turns

    def generate_spanning_tree(self, points):
        
        # Filter out obstacle points
        points = [point for point in points if point not in self.obstacles]

        shuffled_points = points
        edges = []

        for i in range(len(shuffled_points)):
            for j in range(i + 1, len(shuffled_points)):
                
                x1, y1 = shuffled_points[i]
                x2, y2 = shuffled_points[j]
                if (((abs(x2 - x1) == 1 and abs(y2 - y1) == 0)) ^ ((abs(x2 - x1) == 0 and abs(y2 - y1) == 1))):
                    
                    edges.append((shuffled_points[i], shuffled_points[j], 0.61))
                    

                # Check if the points are diagonally adjacent
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    edges.append((shuffled_points[i], shuffled_points[j], 0.61))

        edges.sort(key=lambda edge: edge[2], reverse=False)
        parent = {tuple(point): tuple(point) for point in shuffled_points}

        def find_set(point):
            point_tuple = tuple(point)
            if parent[point_tuple] != point_tuple:
                parent[point_tuple] = find_set(parent[point_tuple])
            return parent[point_tuple]

        def union(set1, set2):
            root1 = find_set(tuple(set1))
            root2 = find_set(tuple(set2))
            parent[root1] = root2

        spanning_tree = []
        for edge in edges:
            point1, point2, weight = edge
            if find_set(point1) != find_set(point2):
                spanning_tree.append((point1, point2, weight))
                union(point1, point2)

        return spanning_tree


    def plot_configuration(self, points, spanning_tree):
        
        x_values, y_values = zip(*points)
        plt.scatter(x_values, y_values, color='blue')
        # plt.show()
        
        color = np.random.rand(3,)
        for edge in spanning_tree:
            
            (x1, y1), (x2, y2), weight = edge


            # plt.plot([x1, x2], [y1, y2], color='red', linewidth=2)
       

        # plt.xlabel('X-axis')
        # plt.ylabel('Y-axis')
        # plt.title('Generated Energy Aware MST')
        # plt.legend()

    def get_points_for_robot(self, i):
        assignment_matrix = self.visualize_assignment()
        indices_dict = self.create_indices_dict(assignment_matrix)
        rrobot_points=[]
        index = 1
        

        if i in indices_dict:
            points = indices_dict[i]
            # points=sorted(points, key = lambda point: self.euclidean_distance(point,self.robots[i-1]))
            pointe=self.generate_spanning_tree(points)
            point=self.generate_and_visualize_dfs(points,pointe)

            formatted_points = [[x, y, 5.5] for x, y in point]

            # Convert the formatted points to a numpy robot_pointsay for easy manipulation
        else:
            return []
        index = 1
        robot_points=formatted_points
        filtered_robot_points=[]
        if(len(robot_points)!=0):
            filtered_robot_points.append(robot_points[0])
        while index < len(robot_points):
            # Check if the current element has already appeared before
            if (robot_points[index] not in robot_points[:index]) and not((np.abs(robot_points[index-1][0]-robot_points[index][0])==2) or (np.abs(robot_points[index-1][1]-robot_points[index][1])==2)):
                # If it hasn't or if the conditions are met, add it to the filtered points
                filtered_robot_points.append(robot_points[index])
            index += 1
        
        new_points = []  # Initialize a new list to store the modified points

        for i in range(len(filtered_robot_points) - 1):
            current_point = filtered_robot_points[i]
            next_point = filtered_robot_points[i + 1]
            
            new_points.append(current_point)
            
            delta_x = abs(next_point[0] - current_point[0])
            delta_y = abs(next_point[1] - current_point[1])
            
            # if delta_x > 1 and delta_y > 1:
            #     avg_x = (current_point[0] + next_point[0]) / 2
            #     avg_y = (current_point[1] + next_point[1]) / 2
            #     new_points.append((current_point[0], math.ceil(avg_y), 5.5))  # Retain the x-coordinate from the previous point
            # elif delta_x > 1 or delta_y > 1:
            #     avg_x = (current_point[0] + next_point[0]) / 2
            #     avg_y = (current_point[1] + next_point[1]) / 2
            #     new_points.append([avg_x, math.ceil(avg_y), 5.5])  # Add the new point with z-coordinate 5.5
        if(len(filtered_robot_points)!=0):
            new_points.append(filtered_robot_points[-1])  # Add the last point from the original list

        print(new_points)
        return new_points


        

    def visualize_darp(self):
       
        assignment_matrix = self.visualize_assignment()
        indices_dict = self.create_indices_dict(assignment_matrix)

        # for i in range(1, 3):
        #     if i in indices_dict:
        #         points = indices_dict[i]
                
        #         spanning_tree = self.generate_spanning_tree(points)

        #         self.plot_configuration(points, spanning_tree)
        #         for i in range(1, 3):
        #             if i in indices_dict:
        #                 points = indices_dict[i]

        #                 self.generate_and_visualize_dfs(points, spanning_tree)
                        


        # plt.show()
    def dfs_traversal(self, start_point, visited, dfs_points):
        visited.add(start_point)
        dfs_points.append(start_point)

        for neighbor in self.get_neighbors(start_point):
            if neighbor not in visited:
                self.dfs_traversal(neighbor, visited, dfs_points)

    def get_neighbors(self, point):
        x, y = point
        neighbors = [
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)
        ]
        return [(neighbor_x, neighbor_y) for neighbor_x, neighbor_y in neighbors if 0 <= neighbor_x<self.rows  and 0 <= neighbor_y <self.cols]


    def generate_and_visualize_dfs(self, points, spanning_tree):
        
        start_point = self.robots[0]  # Assuming starting from the first point in the list
        visited = set()
        dfs_points = []

        self.dfs_traversal(start_point, visited, dfs_points)
        rlist=[]

        # self.plot_configuration(points, spanning_tree)  # Change this to plot MST or other elements
        for i in range(len(dfs_points) - 1):
            current_point = dfs_points[i]
            next_point = self.get_neighbors(current_point)

            # Check if the edge exists in the spanning tree before plotting
            for point in next_point:
                if any(((current_point, point) == (edge[0], edge[1]) or ((current_point, point) == (edge[1], edge[0])) for edge in spanning_tree)):
                    plt.plot([current_point[0], point[0]], [current_point[1], point[1]], color='red', linewidth=2)
                    # print("curremt point", current_point, "point", point)
                    rlist.append(current_point)
                    rlist.append(point)
        plt.title("dfs")
        
        return rlist
    
import time   

starttime=time.time()

rows = 8
cols = 8
robots = [(0, 0),(7,7)]
m = 0.1
obstacles=[(2,2),(3,2),(2,3),(3,3)]


darp_visualizer = DARPVisualizer(rows, cols, robots, obstacles, m)

robot_index = 1  # Replace with the desired robot index
robot_points = darp_visualizer.get_points_for_robot(robot_index)
darp_visualizer.visualize_darp()

print(robot_points)
plt.show()
# # grid=np.zeros((5,5), dtype=int)
# # for point in obstacles:
# #         y, x = point
# #         grid[x][y] = 1
# # plt.imshow(1 - grid, cmap='gray', origin='lower', extent=[0, 5, 0, 5], vmin=0, vmax=1)

# # # Add grid lines
# # plt.grid(color='black', linestyle='-', linewidth=1)

# # # Set axis ticks to go up by 1s
# # plt.xticks(np.arange(0, 5 + 1, step=1))
# # plt.yticks(np.arange(0, 5 + 1, step=1))

# # plt.title('Occupancy Grid Map')
# # plt.xlabel('X')
# # plt.ylabel('Y')
# # plt.show()
tbp=[]
def plot(robot_points):
    plt.close()
    x = [coord[0] for coord in robot_points]
    y = [coord[1] for coord in robot_points]

    # # # Plotting
    plt.plot(x, y, marker='o', linestyle='-', color='royalblue')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graph of 3D Coordinates (X,Y)')

    plt.show()
for point in robot_points:
    robots=[(point[0],point[1])]
    obstacles.append((point[0],point[1]))
    darp_visualizer = DARPVisualizer(rows, cols, robots, obstacles, m)
    tbp.append([point[0],point[1]])


    robot_index = 1  # Replace with the desired robot index
    new_points_points = darp_visualizer.get_points_for_robot(robot_index)
    darp_visualizer.visualize_darp()
plot(tbp)

print(robot_points)


# def overlap_area(x1, y1, x2, y2):
#     dx = min(x1 + 0.5, x2 + 0.5) - max(x1 - 0.5, x2 - 0.5)
#     dy = min(y1 + 0.5, y2 + 0.5) - max(y1 - 0.5, y2 - 0.5)
#     if dx < 0 or dy < 0:
#         return 0
#     return dx * dy

# # Initialize the total area
# total_area = 0

# # Plot each square and calculate the total area
# for point in new_points:
#     x, y,z = point
#     plt.plot([x - 0.5, x + 0.5, x + 0.5, x - 0.5, x - 0.5], [y - 0.5, y - 0.5, y + 0.5, y + 0.5, y - 0.5], color='blue')
#     total_area += 1  # Area of each square is 1

# Calculate the overlap area
# overlap_areas = []
# for i in range(len(new_points)):
#     for j in range(i + 1, len(new_points)):
#         x1, y1, z1 = new_points[i]
#         x2, y2, z2 = new_points[j]
#         overlap = overlap_area(x1, y1, x2, y2)
#         overlap_areas.append(overlap)

# # Total area of overlap
# total_overlap_area = sum(overlap_areas)

# Display the plot
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Unit Squares Centered at Points')
# plt.grid(True)
# plt.axis('equal')
# plt.show()

# print("Total area of squares:", len(new_points))
# print("Total overlap area:", total_overlap_area)
# import math

def calculate_angle(p1, p2, p3):
    """Calculate the angle between three points."""
    dx1 = p1[0] - p2[0]
    dy1 = p1[1] - p2[1]
    dx2 = p3[0] - p2[0]
    dy2 = p3[1] - p2[1]
    
    dot_product = dx1 * dx2 + dy1 * dy2
    cross_product = dx1 * dy2 - dy1 * dx2
    
    angle_rad = math.atan2(cross_product, dot_product)
    angle_deg = math.degrees(angle_rad)
    
    if angle_deg < 0:
        angle_deg += 360
    
    return angle_deg

def total_turn_angle(points):
    """Calculate the total turn angle for a list of points."""
    total_angle = 0
    length=0
    for i in range(len(points) - 2):
        angle = calculate_angle(points[i], points[i+1], points[i+2])
        
        if angle==45 or angle==315 or angle==135 or angle==225 :
            total_angle += 45
            
        elif angle==90 or angle==270:
            total_angle+=90
            
    return total_angle,length

# Example list of points
# points = [(1, 1), (2, 3), (4, 5), (6, 2)]

# # Calculate total turn angle
total_angle = total_turn_angle(tbp)
print("Total turn angle (45 or 90 degrees only):", total_angle[0], "degrees")
print("Total length:", total_angle[1], "degrees")
plt.show()