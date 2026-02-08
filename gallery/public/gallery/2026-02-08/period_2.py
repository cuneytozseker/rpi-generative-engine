import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Clinical Dark Grey
ctx.set_source_rgb(0.04, 0.04, 0.05)
ctx.paint()

def draw_angular_grid(cx, cy, angle, spacing, length, opacity, color=(1, 1, 1)):
    """Draws a dense parallel line system at a specific angle."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(angle)
    
    r, g, b = color
    ctx.set_source_rgba(r, g, b, opacity)
    ctx.set_line_width(0.5)
    
    num_lines = int(length / spacing)
    for i in range(-num_lines, num_lines):
        offset = i * spacing
        ctx.move_to(-length, offset)
        ctx.line_to(length, offset)
        ctx.stroke()
    ctx.restore()

def draw_data_markers(grid_size, density):
    """Adds 'signal' markers to simulate decoded data points."""
    ctx.set_source_rgb(1, 0.1, 0.2)  # Signal Red
    ctx.set_line_width(1.0)
    
    for x in range(0, width, grid_size):
        for y in range(0, height, grid_size):
            if random.random() < density:
                # Draw a small cross
                s = 3
                ctx.move_to(x - s, y)
                ctx.line_to(x + s, y)
                ctx.move_to(x, y - s)
                ctx.line_to(x, y + s)
                ctx.stroke()
                
                # Draw a small technical label (geometric placeholder)
                if random.random() < 0.2:
                    ctx.rectangle(x + 5, y - 5, 10, 2)
                    ctx.fill()

# 1. PRIMARY MOIRÉ FIELD
# Two grids slightly offset in angle to create a large-scale interference pattern
center_x, center_y = width // 2, height // 2
angle_offset = math.radians(2.5) # The critical interference angle
base_spacing = 3.2

# Grid A: The Static Reference
draw_angular_grid(center_x, center_y, 0, base_spacing, 800, 0.4)

# Grid B: The Interference Layer
# Rotating this layer creates the 'shimmering' moiré effect
draw_angular_grid(center_x, center_y, angle_offset, base_spacing, 800, 0.4)


# 2. STRATIFIED HIERARCHY (The 'Swiss' Grid)
# We use large rectangles to mask areas, creating negative space voids
ctx.set_operator(cairo.OPERATOR_DEST_OUT) # Cut holes in the moiré
for _ in range(5):
    rw = random.choice([40, 80, 120])
    rh = random.choice([100, 200, 300])
    rx = random.randint(0, width - rw)
    ry = random.randint(0, height - rh)
    ctx.rectangle(rx, ry, rw, rh)
    ctx.fill()

ctx.set_operator(cairo.OPERATOR_OVER) # Back to normal drawing


# 3. QUANTIZED SUB-LATTICE
# Adding a tertiary grid only in specific zones to increase "Information Density"
zones = [
    (100, 100, 150, 150),
    (400, 250, 100, 180),
    (50, 300, 40, 40)
]

for (zx, zy, zw, zh) in zones:
    # Local high-frequency grid
    ctx.save()
    ctx.rectangle(zx, zy, zw, zh)
    ctx.clip()
    draw_angular_grid(zx + zw/2, zy + zh/2, math.radians(45), 1.5, 200, 0.8, (0.2, 0.6, 1.0))
    ctx.restore()
    
    # Border for the zone
    ctx.set_source_rgba(0.2, 0.6, 1.0, 0.5)
    ctx.set_line_width(0.5)
    ctx.rectangle(zx, zy, zw, zh)
    ctx.stroke()


# 4. SIGNAL SPIKES & ANNOTATIONS
# High-contrast elements that denote "active logic states"
draw_data_markers(20, 0.03)

# Add a "Scale Bar" at the bottom (Swiss precision)
ctx.set_source_rgb(0.9, 0.9, 0.9)
ctx.set_line_width(1)
ctx.move_to(40, height - 40)
ctx.line_to(240, height - 40)
ctx.stroke()

for i in range(11):
    x_pos = 40 + (i * 20)
    tick_h = 10 if i % 5 == 0 else 4
    ctx.move_to(x_pos, height - 40)
    ctx.line_to(x_pos, height - 40 - tick_h)
    ctx.stroke()

# 5. FINAL TEXTURAL PASS
# Fine vertical 'grain' or scanning lines
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
for x in range(0, width, 4):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()

