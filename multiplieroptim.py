from drppp import DARP

def Jcost(arr):
    total_sum = sum(arr)
    mean_value = total_sum / len(arr)
    jcost = sum((mean_value - x)**2 for x in arr)
    return jcost

def optimize_multiplier(initial_multiplier, iterations, learning_rate):
    rows = 20
    cols = 20
    robots = [(1, 1), (20, 1), (1, 20), (20, 20)]
    obstacles = [(4,6)]

    m = initial_multiplier
    darp_solver = DARP(rows, cols, robots, obstacles, m)

    for iteration in range(iterations):
        darp_solver.assign_cells()
        result = darp_solver.visualize_assignment()
        cost = Jcost(result)

        # Update multiplier using gradient descent
        gradient = -2 * sum(result) / len(result)
        m -= learning_rate * gradient

        # Ensure multiplier is within the valid range
        m = min(1, max(0, m[0]))


        print(f"Iteration {iteration + 1}: Multiplier = {m}, Cost = {cost}")

    return m, cost, result

# Set your initial values
initial_multiplier = 0.01
iterations = 1000
learning_rate = 0.001

optimized_multiplier, final_cost, final_result = optimize_multiplier(initial_multiplier, iterations, learning_rate)

print(f"Optimized Multiplier: {optimized_multiplier}")
print(f"Final Cost: {final_cost}")
print(f"Final Assignment: {final_result}")
