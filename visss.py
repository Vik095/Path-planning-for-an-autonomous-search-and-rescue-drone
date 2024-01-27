import numpy as np
import matplotlib.pyplot as plt

# Your matrix
matrix = np.array([[2, 2, 2, 2, 2, 2],
                   [2, 2, 0, 2, 2, 2],
                   [2, 2, 0, 2, 1, 1],
                   [1, 1, 0, 1, 1, 1],
                   [1, 1, 1, 1, 0, 1],
                   [1, 1, 1, 1, 1, 1]])

# Define colors for each number
colors = {0: 'black', 1: 'blue', 2: 'red'}

# Create a plot
fig, ax = plt.subplots()

# Plot the matrix with colors
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        color = colors.get(matrix[, j], 'white')  # Default to white if color not defined
        ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1, fill=True, color=color))

# Set axis labels
ax.set_xticks(np.arange(0.5, matrix.shape[1] + 0.5, 1))
ax.set_yticks(np.arange(-0.5, -matrix.shape[0] - 0.5, -1))
ax.set_xticklabels([])
ax.set_yticklabels([])

# Display the plot
plt.show()
