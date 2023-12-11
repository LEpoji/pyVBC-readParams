from read_dwg import read_dwg
from align_to_grid import align
from extend_lines import extend
from plot_lines import plot
import find_rectangles
from merge_lines import merge_lines
from split_lines import split_lines
from write_csv import write_csv
import os
import glob
import pandas as pd

def process_dxf(file_path):
    lines, opening_lines = read_dwg(file_path)
    print(lines)

    lines, opening_lines = align(lines, opening_lines, grid=100)

    #Initialize a variable to track changes in the dataframe
    df_changed = True

    while df_changed:
        # Make a copy of the dataframe to compare after manipulations
        lines_before = lines.copy()

        # Perform your geometric manipulations
        lines = extend(lines)
        lines = merge_lines(lines)
        #lines = split_lines(lines)
        lines = lines.drop_duplicates(subset=['start_x', 'start_y', 'end_x', 'end_y'])
        lines = lines.reset_index(drop=True)

        # Compare the dataframe before and after manipulations
        if lines.equals(lines_before):
            df_changed = False
            print('No change, end the loop')
        else:
            print('Changed data, restart the loop')


    rectangles, lines = find_rectangles.find_rectangles(lines)
    print(lines)
    no_rect_df = lines[lines['In rect'] == False]
    print(no_rect_df)

    # Generate CSV file name based on DXF file name
    csv_file_name = os.path.splitext(os.path.basename(file_path))[0] + '.csv'
    write_csv(rectangles, lines, csv_file_name)

def process_all_dxf_in_folder(folder_path):


    # List all DXF files in the given folder
    dxf_files = glob.glob(os.path.join(folder_path, '*.dxf'))

    # Process each file
    for file_path in dxf_files:
        process_dxf(file_path)

# Specify the folder containing DXF files
folder_path = 'K:/Projekt/VBC/2023-01-18 Configurator structural calcs MODULES/02 Underlag/Clean dxf'

# Delete all CSV files in the current directory
csv_files_to_delete = glob.glob('*.csv')
for file in csv_files_to_delete:
    os.remove(file)

# Rest of your script...


process_all_dxf_in_folder(folder_path)

# List and sort CSV files
csv_files = sorted([f for f in os.listdir() if f.endswith('.csv')])

# Initialize list to store DataFrames
dfs = []
combined_data = pd.DataFrame(columns=['name', 'module_width', 'module_length', 'module_height', 'xg', 'yg', 'zg', 'rot', 'n'])
print(combined_data)

for file in csv_files:
    temp_df = pd.read_csv(file)
    
    new_rows = []  # List to store new rows

    for _, row in temp_df.iterrows():
        # Check for matching rows
        match = combined_data[(combined_data['module_width'] == row['module_width']) & 
                              (combined_data['module_length'] == row['module_length']) & 
                              (combined_data['xg'] == row['xg']) & 
                              (combined_data['yg'] == row['yg'])]
        
        if not match.empty:
            # Increment 'n' value for matching row
            combined_data.loc[match.index, 'n'] += 1
        else:
            # Store new row in list
            new_rows.append(row)

    # Concatenate new rows with existing DataFrame
    if new_rows:
        combined_data = pd.concat([combined_data, pd.DataFrame(new_rows)], ignore_index=True)

module_counter = 1
for idx, row in combined_data.iterrows():
    combined_data.at[idx, 'name'] = 'M' + str(module_counter)
    module_counter = module_counter + 1

combined_data.to_csv('combined.csv', index=False, sep='\t', header=False)