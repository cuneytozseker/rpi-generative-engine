import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)
ctx.paint()

# Generative Code: Radial Symmetry with Breaking Points

center_x, center_y = width / 2, height / 2
num_segments = 24  # Number of radial segments
radius = 350
line_width = 3
ctx.set_line_width(line_width)

for i in range(num_segments):
    angle = 2 * math.pi * i / num_segments
    x1 = center_x + radius * math.cos(angle)
    y1 = center_y + radius * math.sin(angle)

    # Introduce variation (breaking points)
    break_chance = 0.2 #Probability that a line will terminate early
    break_distance = random.uniform(0.2, 0.8) * radius #Distance from center where line will break

    if random.random() > break_chance:
        x2 = center_x + radius * math.cos(angle)
        y2 = center_y + radius * math.sin(angle)
    else:
        x2 = center_x + break_distance * math.cos(angle)
        y2 = center_y + break_distance * math.sin(angle)
        
    ctx.set_source_rgb(1, 1, 1)
    ctx.move_to(center_x, center_y)
    ctx.line_to(x2, y2)
    ctx.stroke()

    # Small circle at endpoints
    ctx.set_source_rgb(1, 0, 0) #small red circles
    ctx.arc(x2, y2, 2, 0, 2 * math.pi)
    ctx.fill()

# Inner circle
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.arc(center_x, center_y, 50, 0, 2 * math.pi)
ctx.stroke()
