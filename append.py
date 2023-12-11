import pandas as pd
import math
import csv

def find_cuts(start, end, df):
    main_line_horizontal = start[1] == end[1]
    main_line_vertical = start[0] == end[0]
    cuts = []

    for _, row in df.iterrows():
        df_line_horizontal = row['start_y'] == row['end_y']
        df_line_vertical = row['start_x'] == row['end_x']

        if main_line_horizontal and df_line_vertical:
            # Check if the vertical line crosses the horizontal main line
            if start[0] <= row['start_x'] <= end[0] and row['start_y'] <= start[1] <= row['end_y']:
                distance = abs(row['start_x'] - start[0])  # Distance from start for horizontal main line
                cuts.append(distance)

        elif main_line_vertical and df_line_horizontal:
            # Check if the horizontal line crosses the vertical main line
            if row['start_x'] <= start[0] <= row['end_x'] and start[1] <= row['start_y'] <= end[1]:
                distance = abs(row['start_y'] - start[1])  # Distance from start for vertical main line
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
            width = float(row[2])  # Replace index as per your file structure
            length = float(row[3])
            xg = float(row[4])
            yg = float(row[5])
            rot = float(row[6]) * math.pi

            # Write the original row
            all_rows.append(row)

            corner_1 = (round(xg, 0), round(yg, 0))
            corner_2 = (round(xg + width * math.cos(rot), 0), round(yg + width * math.sin(rot), 0))
            corner_3 = (round(xg + width * math.cos(rot) - length * math.sin(rot), 0), round(yg + width * math.sin(rot) + length * math.cos(rot), 0))
            corner_4 = (round(xg - length * math.sin(rot), 0), round(yg + length * math.cos(rot), 0))

            for i in range(1, 5):
                if i == 1:
                    start = corner_1
                    end = corner_2
                elif i == 2:
                    start = corner_2
                    end = corner_3
                elif i == 3:
                    start = corner_3
                    end = corner_4
                else:
                    start = corner_4
                    end = corner_1

                cuts = find_cuts(start, end, df)
                cuts = sorted(cuts)
                n_cuts = int(len(cuts) / 3)

                for cut in range(n_cuts):
                    s = i
                    b = cuts[cut + 2] - cuts[cut]
                    h = 1000
                    x_pos = cuts[cut]
                    y_pos = 1000
                    new_row = ['', s, b, h, x_pos, y_pos, '', '', '']
                    all_rows.append(new_row)

    # Now, overwrite the original file with all_rows
    with open(file, 'w', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerows(all_rows)

