import matplotlib.pyplot as plt

def plot(df):

    # Plotting the lines
    plt.figure(figsize=(6,6))

    for index, row in df.iterrows():
        if row['Part of rectangle'] == True:
            linecolor = 'red'
        else:
            linecolor = 'black'
        plt.plot([row['start_x'], row['end_x']], [row['start_y'], row['end_y']], marker='o', color=linecolor)

    plt.grid(True)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Lines from DataFrame')
    plt.show()