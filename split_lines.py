import pandas as pd

def split_lines(lines):
    action_split = False
    all_new_lines = []  # List to store all new line segments
    new_rows = []


    for index, line in lines.iterrows():
        xstart, ystart, xend, yend = line['start_x'], line['start_y'], line['end_x'], line['end_y']
        line_dir = 'H' if abs(xstart - xend) > abs(ystart - yend) else 'V'

        # Initialize variables to store potential split points
        split_points = []

        # Filter out perpendicular lines
        perp_lines = lines[lines.index != index]
        for _, perp_line in perp_lines.iterrows():
            pxstart, pystart, pxend, pyend = perp_line['start_x'], perp_line['start_y'], perp_line['end_x'], perp_line['end_y']
            perp_dir = 'H' if abs(pxstart - pxend) > abs(pystart - pyend) else 'V'

            # Check for intersection
            if line_dir != perp_dir:
                if line_dir == 'H' and (pystart == ystart or pyend == ystart) and min(xstart, xend) <= pxstart <= max(xstart, xend):
                    split_points.append((pxstart, ystart))
                elif line_dir == 'V' and (pxstart == xstart or pxend == xstart) and min(ystart, yend) <= pystart <= max(ystart, yend):
                    split_points.append((xstart, pystart))

        # Split the line at intersection points
        if split_points:
            split_points.sort()
            prev_point = (line['start_x'], line['start_y'])
            for point in split_points:
                # Create a new line segment for each split
                new_line = line.copy()
                new_line['start_x'], new_line['start_y'] = prev_point
                new_line['end_x'], new_line['end_y'] = point
                new_rows.append(new_line)
                prev_point = point
                action_split = True
        else:
            new_rows.append(line)

    # Concatenate new rows and replace the original DataFrame
    new_df = pd.concat(new_rows, axis=1).transpose()
    return new_df, action_split