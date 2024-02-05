# import matplotlib.pyplot as plt

# # Create a 5 by 5 grid
# grid_size = 5
# x = range(0, grid_size)
# y = range(0, grid_size)

# # Generate all points in the grid
# points = [(i, j) for i in x for j in y]

# # Separate x and y coordinates for plotting
# x_coords, y_coords = zip(*points)

# # Plot the points
# plt.scatter(x_coords, y_coords, marker='o', color='blue')

# # Add grid lines for better visualization


# # Set axis labels
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')

# # Set the title of the plot
# plt.title('Path followed by the 2 drones')

# # Show the plot
# plt.show()
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def construct_polygon(connected_edges):
    points_dict = {}
    
    # Create a dictionary to store points and their coordinates
    for edge in connected_edges:
        for point in edge[:2]:
            if point not in points_dict:
                points_dict[point] = Point(point[0], point[1])

    # Connect the points based on the connected edges
    connected_chain = []
    for edge in connected_edges:
        point1, point2, _ = edge
        connected_chain.append(points_dict[point1])
        connected_chain.append(points_dict[point2])

    # Print the connected chain
    for i in range(0, len(connected_chain), 2):
        print(f"Connecting ({connected_chain[i].x}, {connected_chain[i].y}) to ({connected_chain[i+1].x}, {connected_chain[i+1].y})")

# Example usage:
connected_edges = [((0, 0), (0, 1), 0.61), ((0, 0), (1, 0), 0.61), ((0, 0), (1, 1), 0.61), ((0, 1), (0, 2), 0.61), ((0, 1), (1, 2), 0.61), ((0, 2), (0, 3), 0.61), ((0, 2), (1, 3), 0.61), ((0, 3), (0, 4), 0.61), ((0, 3), (1, 4), 0.61), ((1, 0), (2, 0), 0.61), ((1, 0), (2, 1), 0.61), ((1, 2), (2, 3), 0.61), ((1, 3), (2, 4), 0.61), ((2, 0), (3, 0), 0.61), ((2, 0), (3, 1), 0.61), ((2, 3), (3, 3), 0.61), ((2, 3), (3, 4), 0.61), ((3, 0), (4, 0), 0.61), ((3, 0), (4, 1), 0.61), ((3, 1), (4, 2), 0.61), ((3, 3), (4, 3), 0.61), ((3, 3), (4, 4), 0.61)]

construct_polygon(connected_edges)
