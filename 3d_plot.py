import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import cos, sin, radians

# Read CSV Data
def read_csv_data(filename):
    # Specify the indices of the columns you need
    cols = [1, 2, 4, 5, 7]  # Indices of the required columns
    headers = ['w', 'l', 'x', 'y', 'r']
    return pd.read_csv(filename, delimiter="\t", header=None, names=headers, usecols=cols)


# Function to plot a rectangle
def plot_rectangle(ax, width, length, x, y, rotation):
    # Calculate the rotation in radians

    # Rectangle's bottom left corner after rotation
    dx = x - width / 2
    dy = y - length / 2
    # Create a rectangle

    rect = patches.Rectangle((x, y), width, length, angle=rotation, edgecolor='r', facecolor=None, color=None)
    
    # Add the rectangle to the plot
    ax.add_patch(rect)
    #ax.add_patch(point1)
    #ax.add_patch(point2)
    #ax.add_patch(point3)
    #ax.add_patch(point4)




# Main function to plot rectangles from CSV
def plot_rectangles_from_csv(filename):
    data = read_csv_data(filename)
    fig, ax = plt.subplots()
    print(data)

    # Plot each rectangle
    for _, row in data.iterrows():
        plot_rectangle(ax, row[0], row[1], row[2], row[3], row[4])

    # Set plot limits and show
    ax.set_xlim(0, 200000)  # Adjust these limits based on your data
    ax.set_ylim(-100000, 100000)
    plt.show()

# Example usage
plot_rectangles_from_csv('combined.csv')
