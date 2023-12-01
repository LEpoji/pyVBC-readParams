import pandas

def align(lines, openings, grid=100):
    round_to_100 = lambda x: round(x / grid) * grid

    lines=lines.drop(columns=['Part of rectangle'])
    aligned_lines = lines.map(round_to_100)
    aligned_openings = openings.map(round_to_100)
    aligned_lines['Part of rectangle']=None
    return aligned_lines, aligned_openings
