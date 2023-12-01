import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_rect(df, rect):
    # Plotting the lines
    plt.figure(figsize=(6,6))

    for index, row in df.iterrows():
        if index in rect:
            linecolor = 'red'
        else:
            linecolor = 'black'
        plt.plot([row['start_x'], row['end_x']], [row['start_y'], row['end_y']], marker='o', color=linecolor)

    plt.grid(True)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Lines from DataFrame')
    plt.show()


def find_rectangles(df):
    rectangles = []
    df['Related lines'] = [[] for _ in range(len(df))]  # Initialize an empty list for each line
    df['In rect'] = False

    # Build a list of related lines for each line
    for index, row in df.iterrows():
        for index_compare, row_compare in df.iterrows():
            if index != index_compare:
                # Check if the lines are connected
                if (row['start_x'], row['start_y']) == (row_compare['start_x'], row_compare['start_y']) or \
                   (row['start_x'], row['start_y']) == (row_compare['end_x'], row_compare['end_y']) or \
                   (row['end_x'], row['end_y']) == (row_compare['start_x'], row_compare['start_y']) or \
                   (row['end_x'], row['end_y']) == (row_compare['end_x'], row_compare['end_y']):
                    df.at[index, 'Related lines'].append(index_compare)
    print(df)

    rectangles = []
    for index, row in df.iterrows():
        included_lines = set()
        included_lines.add(index)
        
        # Create a queue to process each related line
        to_process = list(row['Related lines'])
        
        while to_process:
            current_index = to_process.pop(0)  # Remove the first element from the list
            if current_index not in included_lines:
                included_lines.add(current_index)
                # Add the related lines of the current index to the queue
                related_lines_of_current = df.loc[current_index, 'Related lines']
                to_process.extend(related_lines_of_current)
        
        new_rectangle = sorted(list(included_lines))
        if len(new_rectangle) == 4 and new_rectangle not in rectangles:
            rectangles.append(new_rectangle)

    rectangle_new = []
    for rectangle in rectangles:
        # Geometry check for rectangle dimensions here (not implemented)
        filtered_lines = df.loc[rectangle]
        dx = max(filtered_lines['start_x'].max(), filtered_lines['end_x'].max()) - min(filtered_lines['start_x'].min(), filtered_lines['end_x'].min())
        dy = max(filtered_lines['start_y'].max(), filtered_lines['end_y'].max()) - min(filtered_lines['start_y'].min(), filtered_lines['end_y'].min())
        minimum_dimension = min(dy, dx)
        maximum_dimension = max (dy, dx)
        if maximum_dimension<12000 and minimum_dimension>1800:
            rectangle_new.append(rectangle)

    for rectangle in rectangle_new:
        #plot_rect(df, rectangle)
        df.loc[rectangle, 'In rect'] = True

    print(rectangles)
    return rectangle_new, df
