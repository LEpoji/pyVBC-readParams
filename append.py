import pandas as pd
import math
import csv
import matplotlib.pyplot as plt

def find_cuts(start, end, df):
    main_line_horizontal = start[1] == end[1]
    main_line_vertical = start[0] == end[0]
    cuts = []

    # Use min and max to handle lines in both directions
    main_line_start_x, main_line_end_x = min(start[0], end[0]), max(start[0], end[0])
    main_line_start_y, main_line_end_y = min(start[1], end[1]), max(start[1], end[1])

    main_line_start_x_dist = start[0]
    main_line_start_y_dist = start[1]

    for _, row in df.iterrows():
        df_line_horizontal = row['start_y'] == row['end_y']
        df_line_vertical = row['start_x'] == row['end_x']
        df_line_start_x, df_line_end_x = min(row['start_x'], row['end_x']), max(row['start_x'], row['end_x'])
        df_line_start_y, df_line_end_y = min(row['start_y'], row['end_y']), max(row['start_y'], row['end_y'])

        if main_line_horizontal and df_line_vertical:
            # Check if the vertical line crosses the horizontal main line
            if main_line_start_x <= row['start_x'] <= main_line_end_x and df_line_start_y <= start[1] <= df_line_end_y:
                distance = abs(row['start_x'] - main_line_start_x_dist)
                cuts.append(distance)

        elif main_line_vertical and df_line_horizontal:
            # Check if the horizontal line crosses the vertical main line
            if df_line_start_x <= start[0] <= df_line_end_x and main_line_start_y <= row['start_y'] <= main_line_end_y:
                distance = abs(row['start_y'] - main_line_start_y_dist)
                cuts.append(distance)

    return cuts


    

def openings(file, df):
    with open(file, 'r', newline='') as read_obj:
        csv_reader = csv.reader(read_obj)
        all_rows = []  # Store all rows here, including new ones
        # Assuming the first row is the header
        header = next(csv_reader)
        all_rows.append(header)

        for row in csv_reader:
            # Convert row items to the appropriate types as needed
            width = float(row[1])  # Replace index as per your file structure
            length = float(row[2])
            xg = float(row[4])
            yg = float(row[5])
            rot = float(row[7]) * math.pi/180
            print(rot)

            # Write the original row
            all_rows.append(row)

            corner_1 = (round(xg, 0), round(yg, 0))
            corner_2 = (round(xg + width * math.cos(1*rot), 0), round(yg + width * math.sin(1*rot), 0))
            corner_3 = (round(xg + width * math.cos(1*rot) - length * math.sin(1*rot), 0), round(yg + width * math.sin(1*rot) + length * math.cos(1*rot), 0))
            corner_4 = (round(xg - length * math.sin(1*rot), 0), round(yg + length * math.cos(1*rot), 0))

            for i in range(1, 5):
                print(i)
                if i == 1:
                    start = corner_2
                    end = corner_3
                elif i == 2:
                    start = corner_3
                    end = corner_4
                elif i == 3:
                    start = corner_4
                    end = corner_1
                else:
                    start = corner_1
                    end = corner_2

                cuts = find_cuts(start, end, df)
                cuts = sorted(cuts)
                n_cuts = int(len(cuts) / 3)

                for counter in range(0, len(cuts), 3):
                    if counter + 2 < len(cuts):  # Ensure there are three elements to process
                        s = i
                        b = cuts[counter + 2] - cuts[counter]
                        h = 1000
                        x_pos = cuts[counter]
                        y_pos = 1000
                        new_row = ['', s, b, h, x_pos, y_pos, '', '', '']
                        all_rows.append(new_row)

    # Now, overwrite the original file with all_rows
    with open(file, 'w', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerows(all_rows)

