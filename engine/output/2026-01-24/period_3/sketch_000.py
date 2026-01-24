import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)  # or your choice
ctx.paint()

# Swiss Grid with Bold Geometric Shapes

grid_size = 8  # Adjust for finer/coarser grid
cell_width = width / grid_size
cell_height = height / grid_size

ctx.set_line_width(2) # Line thickness
for row in range(grid_size):
    for col in range(grid_size):
        x = col * cell_width
        y = row * cell_height

        # Random chance to draw a shape in the cell
        if random.random() < 0.7:  # Adjust probability
            shape_type = random.randint(0, 3) # 0: rectangle, 1: circle, 2: triangle, 3: diagonal line

            if shape_type == 0: # Rectangle
                rect_width = random.uniform(cell_width * 0.2, cell_width * 0.9)
                rect_height = random.uniform(cell_height * 0.2, cell_height * 0.9)
                rect_x = x + (cell_width - rect_width) / 2
                rect_y = y + (cell_height - rect_height) / 2
                ctx.set_source_rgb(1, 1, 1) # White
                ctx.rectangle(rect_x, rect_y, rect_width, rect_height)
                if random.random() < 0.5:
                    ctx.fill()
                else:
                    ctx.stroke()
            elif shape_type == 1: # Circle
                radius = random.uniform(min(cell_width, cell_height) * 0.1, min(cell_width, cell_height) * 0.4)
                ctx.set_source_rgb(1, 1, 1)
                ctx.arc(x + cell_width / 2, y + cell_height / 2, radius, 0, 2 * math.pi)
                if random.random() < 0.5:
                    ctx.fill()
                else:
                    ctx.stroke()
            elif shape_type == 2: # Triangle
                x1 = x + cell_width / 2
                y1 = y + cell_height * 0.1
                x2 = x + cell_width * 0.1
                y2 = y + cell_height * 0.9
                x3 = x + cell_width * 0.9
                y3 = y + cell_height * 0.9

                ctx.move_to(x1, y1)
                ctx.line_to(x2, y2)
                ctx.line_to(x3, y3)
                ctx.close_path()
                ctx.set_source_rgb(1, 1, 1)
                if random.random() < 0.5:
                    ctx.fill()
                else:
                    ctx.stroke()
            elif shape_type == 3: # Diagonal Line
                line_width = random.uniform(1, 5)
                ctx.set_line_width(line_width)
                ctx.move_to(x, y)
                ctx.line_to(x + cell_width, y + cell_height)
                ctx.set_source_rgb(1, 1, 1)
                ctx.stroke()

