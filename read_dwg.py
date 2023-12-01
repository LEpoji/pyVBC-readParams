import ezdxf
import math
import pandas as pd

def calculate_length(start_x, start_y, end_x, end_y):
    length = ((end_x - start_x)**2 + (end_y - start_y)**2)**(1/2)
    return length

def rotate_point(point, angle, origin=(0, 0)):
    """Rotate a point counterclockwise by a given angle around a given origin."""
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def read_dwg(file_path):
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()

    lines_data = []
    opening_lines_data = []

    for entity in msp.query('LINE[layer=="Construction Line"]'):
        start = (entity.dxf.start.x, entity.dxf.start.y)
        end = (entity.dxf.end.x, entity.dxf.end.y)
        lines_data.append({'start_x': start[0], 'start_y': start[1], 'end_x': end[0], 'end_y': end[1]})

    for insert in msp.query('INSERT'):
        block = doc.blocks[insert.dxf.name]
        dx, dy, _ = insert.dxf.insert
        angle = insert.dxf.rotation if insert.dxf.hasattr('rotation') else 0

        for entity in block.query('LINE[layer=="Construction Line"]'):
            start = rotate_point((entity.dxf.start.x, entity.dxf.start.y), angle)
            end = rotate_point((entity.dxf.end.x, entity.dxf.end.y), angle)
            start_x = start[0] + dx
            start_y = start[1] + dy
            end_x = end[0] + dx
            end_y = end[1] + dy
            if calculate_length(start_x, start_y, end_x, end_y) < 500:
                opening_lines_data.append({'start_x': start_x, 'start_y': start_y, 'end_x': end_x, 'end_y': end_y})

    lines_df = pd.DataFrame(lines_data)
    opening_lines_df = pd.DataFrame(opening_lines_data)
    lines_df['Part of rectangle'] = None
    return lines_df, opening_lines_df
