import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Black
ctx.set_source_rgb(0.02, 0.02, 0.02)
ctx.paint()

def draw_truchet_tile(x, y, size, orientation, weight, alpha):
    """Draws a Smith-style Truchet tile (two arcs)."""
    ctx.set_line_width(weight)
    ctx.set_source_rgba(1, 1, 1, alpha)
    
    r = size / 2
    if orientation == 0:
        # Top-left and Bottom-right arcs
        ctx.arc(x, y, r, 0, math.pi / 2)
        ctx.stroke()
        ctx.arc(x + size, y + size, r, math.pi, 3 * math.pi / 2)
        ctx.stroke()
    else:
        # Top-right and Bottom-left arcs
        ctx.arc(x + size, y, r, math.pi / 2, math.pi)
        ctx.stroke()
        ctx.arc(x, y + size, r, 3 * math.pi / 2, 2 * math.pi)
        ctx.stroke()

def recursive_subdivide(x, y, size, depth, max_depth):
    """Hierarchically subdivides space based on mathematical probability."""
    # Probability of subdivision increases with proximity to 'focal points'
    # or simply decreases with depth for a balanced distribution.
    divide_prob = 0.75 - (depth * 0.15)
    
    # Force subdivision at early levels to ensure complexity
    if depth < 2 or (depth < max_depth and random.random() < divide_prob):
        new_size = size / 2
        recursive_subdivide(x, y, new_size, depth + 1, max_depth)
        recursive_subdivide(x + new_size, y, new_size, depth + 1, max_depth)
        recursive_subdivide(x, y + new_size, new_size, depth + 1, max_depth)
        recursive_subdivide(x + new_size, y + new_size, new_size, depth + 1, max_depth)
    else:
        # Visual weight and alpha are tied to depth (Swiss Hierarchy)
        # Deep recursion results in thinner, more delicate lines
        weight = max(0.5, 4.0 - depth * 0.8)
        alpha = 0.2 + (depth * 0.12)
        orientation = random.randint(0, 1)
        draw_truchet_tile(x, y, size, orientation, weight, alpha)

# --- Generative Execution ---

# 1. LAYER ONE: The Foundation Grid
# Large, faint structural paths that define the primary network
ctx.set_line_cap(cairo.LINE_CAP_ROUND)
grid_size = 120
for i in range(0, width, grid_size):
    for j in range(0, height, grid_size):
        draw_truchet_tile(i, j, grid_size, random.randint(0, 1), 1.5, 0.15)

# 2. LAYER TWO: The Recursive Network
# High density of marks, creating the "earned grey" textures
random.seed(42) # Deterministic for this specific composition balance
recursive_subdivide(0, 0, 480, 0, 5) # Square recursive area
recursive_subdivide(480, 0, 120, 0, 4) # Fill the remainder
recursive_subdivide(480, 120, 120, 0, 4)
recursive_subdivide(480, 240, 120, 0, 4)
recursive_subdivide(480, 360, 120, 0, 4)

# 3. LAYER THREE: The Offset Interference (Moiré effect)
# A secondary layer slightly shifted to create visual tension and depth
ctx.save()
ctx.translate(5, 5)
for i in range(0, width, 60):
    for j in range(0, height, 60):
        if random.random() > 0.6:
            draw_truchet_tile(i, j, 60, random.randint(0, 1), 0.75, 0.1)
ctx.restore()

# 4. SWISS DESIGN ELEMENTS: Framing and Annotation
# Using rectangles and lines to anchor the composition
ctx.set_source_rgba(1, 1, 1, 0.8)
ctx.set_line_width(1)

# Vertical Margin Line
ctx.move_to(30, 20)
ctx.line_to(30, height - 20)
ctx.stroke()

# Data markers (symbolic mapping)
for _ in range(12):
    ry = random.randint(40, height - 40)
    ctx.rectangle(28, ry, 4, 1)
    ctx.fill()

# Geometric focus points
ctx.set_line_width(0.5)
for _ in range(3):
    cx, cy = random.randint(100, 500), random.randint(100, 380)
    ctx.arc(cx, cy, 15, 0, 2 * math.pi)
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.stroke()
    ctx.move_to(cx - 20, cy)
    ctx.line_to(cx + 20, cy)
    ctx.move_to(cx, cy - 20)
    ctx.line_to(cx, cy + 20)
    ctx.stroke()

# Final subtle grain/noise would be here, but using density of lines instead.
# The intersections of the recursive tiles create a "Network Density" 
# that fluctuates between claustrophobic detail and minimalist voids.

