import pandas as pd

"""def are_collinear_and_connected(row1, row2, tolerance=0.01):
    # Extract points from the DataFrame rows
    x1, y1, x2, y2 = row1['start_x'], row1['start_y'], row1['end_x'], row1['end_y']
    x3, y3, x4, y4 = row2['start_x'], row2['start_y'], row2['end_x'], row2['end_y']

    # Collinearity and connection checks are similar to before
    collinear = abs((x2 - x1) * (y3 - y2) - (x3 - x2) * (y2 - y1)) < tolerance and \
                abs((x2 - x1) * (y4 - y2) - (x4 - x2) * (y2 - y1)) < tolerance
    connected = min(abs(x2 - x3), abs(x2 - x4), abs(x1 - x3), abs(x1 - x4)) < tolerance and \
                min(abs(y2 - y3), abs(y2 - y4), abs(y1 - y3), abs(y1 - y4)) < tolerance
    return collinear and connected

def merge_lines(df):
    merged = True
    while merged:
        merged = False
        i = 0
        while i < len(df):
            row1 = df.iloc[i]
            j = i + 1
            while j < len(df):
                row2 = df.iloc[j]
                if are_collinear_and_connected(row1, row2):
                    # Merge lines and update DataFrame
                    new_line = pd.DataFrame({
                        'start_x': [min(row1['start_x'], row1['end_x'], row2['start_x'], row2['end_x'])],
                        'start_y': [min(row1['start_y'], row1['end_y'], row2['start_y'], row2['end_y'])],
                        'end_x': [max(row1['start_x'], row1['end_x'], row2['start_x'], row2['end_x'])],
                        'end_y': [max(row1['start_y'], row1['end_y'], row2['start_y'], row2['end_y'])]
                    })
                    df = pd.concat([df.iloc[:i], df.iloc[i+1:j], df.iloc[j+1:], new_line]).reset_index(drop=True)
                    merged = True
                    break
                j += 1
            if merged:
                break
            i += 1
    return df"""


def are_collinear_and_connected(row1, row2, tolerance1=150, tolerance2=100):
    # Extract points from the DataFrame rows
    x1, y1, x2, y2 = row1['start_x'], row1['start_y'], row1['end_x'], row1['end_y']
    x3, y3, x4, y4 = row2['start_x'], row2['start_y'], row2['end_x'], row2['end_y']

    # Collinearity and connection checks
    connected = min(abs(x2 - x3), abs(x2 - x4), abs(x1 - x3), abs(x1 - x4)) < tolerance2 and \
                min(abs(y2 - y3), abs(y2 - y4), abs(y1 - y3), abs(y1 - y4)) < tolerance2
    
    if abs(x1 - x2) < tolerance1:
        if abs(x3 - x4) < tolerance1:
            collinear = True
        else:
            collinear = False
    else:
        if abs(y3 - y4) < tolerance1:
            collinear = True
        else:
            collinear = False
    


    return collinear and connected

def merge_lines(df):
    action_merge = False
    df['Merged'] = False
    new_rows = []

    for index1 in range(len(df)):
        for index2 in range(index1 + 1, len(df)):
            row1, row2 = df.iloc[index1], df.iloc[index2]
            if are_collinear_and_connected(row1, row2):
                # Mark as merged
                df.at[index1, 'Merged'] = True
                df.at[index2, 'Merged'] = True

                # Prepare new merged line
                new_line = {'start_x': min(row1['start_x'], row1['end_x'], row2['start_x'], row2['end_x']),
                            'start_y': min(row1['start_y'], row1['end_y'], row2['start_y'], row2['end_y']),
                            'end_x': max(row1['start_x'], row1['end_x'], row2['start_x'], row2['end_x']),
                            'end_y': max(row1['start_y'], row1['end_y'], row2['start_y'], row2['end_y'])}
                new_rows.append(new_line)
                action_merge = True

    # Convert new_rows to DataFrame
    new_rows_df = pd.DataFrame(new_rows)

    # Filter out merged rows and append new rows
    df = pd.concat([df[~df['Merged']], new_rows_df]).reset_index(drop=True)

    # Optionally, drop the 'Merged' column if no longer needed
    df = df.drop(columns=['Merged'])

    return df