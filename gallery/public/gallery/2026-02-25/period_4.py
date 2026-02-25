import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Void
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_truchet_tile(x, y, size, orientation, color, weight, alpha=1.0):
    """Draws a Smith-style Truchet tile (two arcs) within a square cell."""
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)
    ctx.set_line_width(weight)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    
    # Orientation 0: Top-Left to Bottom-Right connectivity
    # Orientation 1: Top-Right to Bottom-Left connectivity
    if orientation == 0:
        # Arc 1: Top-Left
        ctx.arc(x, y, size / 2, 0, math.pi / 2)
        ctx.stroke()
        # Arc 2: Bottom-Right
        ctx.arc(x + size, y + size, size / 2, math.pi, 3 * math.pi / 2)
        ctx.stroke()
    else:
        # Arc 1: Top-Right
        ctx.arc(x + size, y, size / 2, math.pi / 2, math.pi)
        ctx.stroke()
        # Arc 2: Bottom-Left
        ctx.arc(x, y + size, size / 2, 3 * math.pi / 2, 2 * math.pi)
        ctx.stroke()

def recursive_grid(x, y, size, depth):
    """Subdivides space based on a probability threshold to create hierarchy."""
    if depth < 3 and random.random() < 0.45:
        new_size = size / 2
        recursive_grid(x, y, new_size, depth + 1)
        recursive_grid(x + new_size, y, new_size, depth + 1)
        recursive_grid(x, y + new_size, new_size, depth + 1)
        recursive_grid(x + new_size, y + new_size, new_size, depth + 1)
    else:
        # Once at a leaf node, we layer multiple Truchet interactions
        draw_layered_cell(x, y, size)

def draw_layered_cell(x, y, size):
    """Layers multiple Truchet patterns with varying weights and colors."""
    # Palette
    ochre = (0.85, 0.6, 0.2)
    teal = (0.1, 0.5, 0.5)
    vermillion = (0.8, 0.2, 0.1)
    parchment = (0.9, 0.9, 0.85)
    
    # Shared random state for consistent structure within layers
    seed = random.randint(0, 1)
    
    # Layer 1: The "Atmospheric Flow" (Subtle, wide, low opacity)
    draw_truchet_tile(x, y, size, seed, parchment, size * 0.2, 0.05)
    
    # Layer 2: The "Structural Backbone" (High contrast, medium weight)
    # We occasionally flip the seed for the second layer to create intersections
    sub_seed = seed if random.random() > 0.2 else 1 - seed
    draw_truchet_tile(x, y, size, sub_seed, parchment, 1.5, 0.6)
    
    # Layer 3: "Interference Patterns" (Accent colors)
    if random.random() > 0.6:
        color = random.choice([ochre, teal, vermillion])
        # Draw thinner, more intense lines
        draw_truchet_tile(x, y, size, seed, color, 0.8, 0.9)
        
    # Layer 4: "Optical Noise" (Micro-dots at midpoints)
    if random.random() > 0.8:
        ctx.set_source_rgba(1, 1, 1, 0.4)
        dot_radius = 1.2
        ctx.arc(x + size/2, y, dot_radius, 0, 2 * math.pi)
        ctx.arc(x + size/2, y + size, dot_radius, 0, 2 * math.pi)
        ctx.arc(x, y + size/2, dot_radius, 0, 2 * math.pi)
        ctx.arc(x + size, y + size/2, dot_radius, 0, 2 * math.pi)
        ctx.fill()

# Main Composition Execution
cols, rows = 8, 6
cell_w = width / cols
cell_h = height / rows

# We use a slightly smaller grid area to allow for a border (Swiss design)
margin = 40
inner_width = width - (margin * 2)
inner_height = height - (margin * 2)
grid_size = 60 # Base module size

# Center the grid
start_x = (width - (inner_width // grid_size * grid_size)) / 2
start_y = (height - (inner_height // grid_size * grid_size)) / 2

# Apply a global rotation for dynamic energy
ctx.translate(width/2, height/2)
ctx.rotate(random.uniform(-0.02, 0.02))
ctx.translate(-width/2, -height/2)

for i in range(int(inner_width // grid_size)):
    for j in range(int(inner_height // grid_size)):
        recursive_grid(
            start_x + i * grid_size, 
            start_y + j * grid_size, 
            grid_size, 
            0
        )

# Post-processing: Subtle grid overlay for "Mechanical" feel
ctx.set_source_rgba(1, 1, 1, 0.03)
ctx.set_line_width(0.5)
for i in range(cols + 1):
    ctx.move_to(i * cell_w, 0)
    ctx.line_to(i * cell_w, height)
    ctx.stroke()
for j in range(rows + 1):
    ctx.move_to(0, j * cell_h)
    ctx.line_to(width, j * cell_h)
    ctx.stroke()

# Final focal point: Vermillion "Data-Point"
ctx.set_source_rgb(0.8, 0.2, 0.1)
ctx.arc(width - margin, height - margin, 4, 0, 2 * math.pi)
ctx.fill()

# Clean border (Brutalist frame)
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.set_line_width(margin * 0.8)
ctx.rectangle(0, 0, width, height)
ctx.stroke()
