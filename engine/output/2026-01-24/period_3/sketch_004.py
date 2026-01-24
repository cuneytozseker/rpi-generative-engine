import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)  # Black background
ctx.paint()

# Generative code: Wave interference

num_waves = 20
amplitude = 50
wavelength_base = 100
phase_shift_increment = math.pi / 10
y_offset = height / 2
x_offset = width / 2
line_width = 2

ctx.set_line_width(line_width)

for i in range(num_waves):
    wavelength = wavelength_base + i * 5
    phase_shift = i * phase_shift_increment
    
    ctx.set_source_rgb(1, 1, 1) # White lines
    
    path_length = width * 2 # Extend path beyond the visible area
    
    ctx.move_to(-width/2, y_offset + amplitude * math.sin(phase_shift)) # Start slightly off screen

    for x in range(-int(width/2), path_length): # Extend rendering of lines
        y = y_offset + amplitude * math.sin(x / wavelength * 2 * math.pi + phase_shift)
        ctx.line_to(x, y)
    
    ctx.stroke()
