import matplotlib.pyplot as plt
import math

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def kruskals_algorithm(points):
    edges = []
    
    # Generate edges for horizontal, vertical, and adjacent diagonal connections
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]

            if x1 == x2 or y1 == y2 or abs(x2 - x1) == abs(y2 - y1):
                edges.append((points[i], points[j], euclidean_distance(points[i], points[j])))

    edges.sort(key=lambda edge: edge[2])

    parent = {point: point for point in points}

    def find_set(point):
        if parent[point] != point:
            parent[point] = find_set(parent[point])
        return parent[point]

    def union(set1, set2):
        root1 = find_set(set1)
        root2 = find_set(set2)
        parent[root1] = root2

    minimum_spanning_tree = []
    for edge in edges:
        point1, point2, weight = edge
        if find_set(point1) != find_set(point2):
            minimum_spanning_tree.append((point1, point2, weight))
            union(point1, point2)

    return minimum_spanning_tree

# Given points in the grid
points = [(x,y) for x in range(6) for y in range(6)]

# Applying Kruskal's algorithm
minimum_spanning_tree = kruskals_algorithm(points)

# Plotting the points
x_values, y_values = zip(*points)
plt.scatter(x_values, y_values, color='blue', label='Points')

# Plotting the minimum spanning tree in red
for edge in minimum_spanning_tree:
    (x1, y1), (x2, y2), weight = edge
    plt.plot([x1, x2], [y1, y2], color='red', linewidth=2)

# Adding labels and legend
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Minimum Spanning Tree')
plt.legend()

# Show the plot
plt.show()
