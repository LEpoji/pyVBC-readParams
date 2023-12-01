def extend(lines):
    action_extend = False
    print(lines)
    
    # Identify the direction of each line
    for idx, line in lines.iterrows():
        xstart, ystart, xend, yend = line['start_x'], line['start_y'], line['end_x'], line['end_y']

        if abs(xstart - xend) < 50:  # Vertical line
            lines.at[idx, 'Direction'] = 'V'
        else:  # Horizontal line
            lines.at[idx, 'Direction'] = 'H'

    # Extend lines in both directions to nearest perpendicular intersection within 1000 mm
    for idx, line in lines.iterrows():
        xstart, ystart, xend, yend, dir = line['start_x'], line['start_y'], line['end_x'], line['end_y'], line['Direction']
        closest_distance_start, closest_distance_end = 1000, 1000  # Limits for both ends
        new_xstart, new_ystart, new_xend, new_yend = xstart, ystart, xend, yend

        filtered_lines = lines[lines['Direction'] != dir]

        for _, perp_line in filtered_lines.iterrows():
            pxstart, pystart, pxend, pyend = perp_line['start_x'], perp_line['start_y'], perp_line['end_x'], perp_line['end_y']

            # Calculate potential intersection points and distances for both ends
            if dir == 'V':
                # Check for intersections with horizontal lines
                if xstart >= min(pxstart, pxend) and xstart <= max(pxstart, pxend):
                    distance_start = abs(ystart - pystart)
                    distance_end = abs(yend - pyend)
                    if distance_start < closest_distance_start:
                        closest_distance_start = distance_start
                        new_ystart = pystart
                    if distance_end < closest_distance_end:
                        closest_distance_end = distance_end
                        new_yend = pyend
            else:
                # Check for intersections with vertical lines
                if ystart >= min(pystart, pyend) and ystart <= max(pystart, pyend):
                    distance_start = abs(xstart - pxstart)
                    distance_end = abs(xend - pxend)
                    if distance_start < closest_distance_start:
                        closest_distance_start = distance_start
                        new_xstart = pxstart
                    if distance_end < closest_distance_end:
                        closest_distance_end = distance_end
                        new_xend = pxend

            # Update the line if within 1000 mm for both ends
            if closest_distance_start <= 1000:
                lines.at[idx, 'start_x'], lines.at[idx, 'start_y'] = new_xstart, new_ystart
                action_extend = True
            if closest_distance_end <= 1000:
                lines.at[idx, 'end_x'], lines.at[idx, 'end_y'] = new_xend, new_yend
                action_extend = True

    return lines, action_extend