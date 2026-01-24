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

# Generative Code: Wave Interference

def draw_wave(ctx, x_offset, y_offset, amplitude, frequency, phase, color):
    ctx.set_source_rgb(*color)
    ctx.set_line_width(2)
    ctx.move_to(0, y_offset + amplitude * math.sin(frequency * 0 + phase))

    for x in range(width):
        y = y_offset + amplitude * math.sin(frequency * x + phase)
        ctx.line_to(x, y)

    ctx.stroke()


num_waves = 10
amplitude = 30
frequency_base = 0.01
phase_increment = math.pi / 4
y_spacing = height / (num_waves + 1)

for i in range(num_waves):
    y_offset = (i + 1) * y_spacing
    frequency = frequency_base + i * 0.002  # Vary frequency slightly
    phase = i * phase_increment
    color = (1, 1, 1)  # White
    draw_wave(ctx, 0, y_offset, amplitude, frequency, phase, color)

# Second wave set, inverted

for i in range(num_waves):
    y_offset = (i + 1) * y_spacing
    frequency = frequency_base + i * 0.002 # Vary frequency slightly
    phase = i * phase_increment
    color = (0, 0, 0) # Black
    draw_wave(ctx, 0, y_offset, amplitude, frequency, -phase, color) # Invert the phase

