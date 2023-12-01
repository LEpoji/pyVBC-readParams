import pandas as pd

def write_csv(rectangles, lines, filename):

    output_data = []
    module_counter = 1
    for rectangle in rectangles:
        filtered_lines = lines.loc[rectangle]
        name = 'M' + str(module_counter)
        dx = abs(max(filtered_lines['start_x'].max(), filtered_lines['end_x'].max()) - min(filtered_lines['start_x'].min(), filtered_lines['end_x'].min()))
        dy = abs(max(filtered_lines['start_y'].max(), filtered_lines['end_y'].max()) - min(filtered_lines['start_y'].min(), filtered_lines['end_y'].min()))

        if dx < dy:
            module_length = dy
            module_width = dx
            module_height = 3000
            rot = 0
            xg = min(filtered_lines['start_x'].min(), filtered_lines['end_x'].min())
            yg = min(filtered_lines['start_y'].min(), filtered_lines['end_y'].min())
            zg = 0
        else:
            module_length = dx
            module_width = dy
            module_height = 3000
            rot = -90
            xg = min(filtered_lines['start_x'].min(), filtered_lines['end_x'].min())
            yg = max(filtered_lines['start_y'].max(), filtered_lines['end_y'].max())
            zg = 0

        #Write csv where each row has the format
        output_data.append({
                'name': name,
                'module_width': module_width,
                'module_length': module_length,
                'module_height': module_height,
                'xg': xg,
                'yg': yg,
                'zg': zg,
                'rot': rot,
                'n':1
            })        
        module_counter = module_counter+1

    output_df = pd.DataFrame(output_data)
    cols_to_consider = [col for col in output_df.columns if col != 'name']
    output_df = output_df.drop_duplicates(subset=cols_to_consider)

    # Write the DataFrame to a CSV file
    output_df.to_csv(filename, index=False)