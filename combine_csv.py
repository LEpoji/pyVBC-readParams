import pandas as pd

def safe_convert_to_float(val):
    try:
        return float(val)
    except ValueError:
        return float(0)  # Convert non-numeric values to NaN

def combine(files):
    combined_df = None

    for file in files:

        n = 0
        data = pd.read_csv(file, delimiter=',')
        data['group'] = 0
        data = data.fillna('empty')

        for index, row in data.iterrows():
            if row['name'] != 'empty':
                n += 1
            data.at[index, 'group'] = n

        max_group = data['group'].max()

        for group_num in range(1, max_group + 1):
            add_new_group = True
            filtered_group = data[data['group'] == group_num]

            # Extract and sort numeric values from specific columns
            group_values = sorted([safe_convert_to_float(x) for x in filtered_group[['module_width', 'module_length', 'xg', 'yg', 'rot']].values.flatten()])


            if combined_df is not None:
                for existing_group in combined_df['group'].unique():
                    filtered_from_combined = combined_df[combined_df['group'] == existing_group]
                    combined_group_values = sorted([safe_convert_to_float(x) for x in filtered_from_combined[['module_width', 'module_length', 'xg', 'yg', 'rot']].values.flatten()])

                    if group_values == combined_group_values:
                        print('Found a match')
                        match_row = combined_df[(combined_df['group'] == existing_group) & (combined_df['name'] != 'empty')]
                        if not match_row.empty:
                            match_row_index = match_row.index[0]
                            combined_df.at[match_row_index, 'n'] += 1                    

                        add_new_group = False
                        break

            if add_new_group:
                # Check for first row match
                first_row = filtered_group.head(1)
                first_row_match_sum = 0
                if combined_df is not None:
                    for existing_group in combined_df['group'].unique():
                        existing_first_row = combined_df[combined_df['group'] == existing_group].head(1)
                        # Compare the specified columns
                        if all(first_row[col].values[0] == existing_first_row[col].values[0] for col in ['module_width', 'module_length', 'xg', 'yg', 'rot']):
                            first_row_match_sum += existing_first_row['n'].iloc[0] * existing_first_row['module_height'].iloc[0]

                    # Update 'zg' in the first row of the filtered group
                    if first_row_match_sum > 0:
                        filtered_group.at[filtered_group.index[0], 'zg'] = first_row_match_sum
                        print('found something here')

                if combined_df is None:
                    print('First row')
                    # Initialize combined_df with the structure of the data DataFrame
                    combined_df = pd.DataFrame(columns=data.columns)
                else:
                    print('none found')
                    new_group_num = combined_df['group'].max() + 1
                    filtered_group.loc[:,'group'] = new_group_num
                combined_df = pd.concat([combined_df, filtered_group])

    with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                        'display.precision', 3,
                        ):
        print(combined_df)

    m_counter = 1
    combined_df.reset_index(drop=True, inplace=True)
    for index, row in combined_df.iterrows():
        if row['name'] != 'empty':
            combined_df.at[index, 'name'] = f'M{m_counter}'
            m_counter += 1
    combined_df = combined_df.replace('empty', '')
    combined_df = combined_df.drop(columns=['group'])
    combined_df.to_csv('combined_with_openings.csv', index=False, sep='\t', header=False)