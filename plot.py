import matplotlib.pyplot as plt

# Example data
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # x-axis values
y = [4.45, 3.167, 2.433, 2.167, 2.067, 1.9167, 1.767, 1.667, 1.55, 1.45] # runtime
z = [218, 306, 398, 447, 470, 503, 547, 581, 626, 670] # mb/s read

y_2 = [ 1 / (element / y[0]) for element in y]

plt.plot(x, z)
plt.xlabel('Number of Cores')
plt.ylabel('Processing Speed (MB/s)')
plt.title('Core Count vs Processing Speed')
plt.show()
