import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.02, 0.02, 0.05)  # Deep midnight blue-black
ctx.paint()

def draw_truchet_cell(x, y, size, variant, color, weight, dashed=False):
    """Draws a sophisticated Truchet tile variant with multiple arcs or lines."""
    ctx.save()
    ctx.translate(x + size/2, y + size/2)
    
    r, g, b, a = color
    ctx.set_source_rgba(r, g, b, a)
    ctx.set_line_width(weight)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    
    if dashed:
        ctx.set_dash([size * 0.1, size * 0.1])
    else:
        ctx.set_dash([])

    half = size / 2
    
    # Variant logic: 0 and 1 are standard arcs, 2 is a cross, 3 is nested arcs
    if variant == 0:
        # Arcs connecting adjacent sides
        ctx.arc(-half, -half, half, 0, math.pi / 2)
        ctx.stroke()
        ctx.arc(half, half, half, math.pi, 3 * math.pi / 2)
        ctx.stroke()
    elif variant == 1:
        ctx.arc(half, -half, half, math.pi / 2, math.pi)
        ctx.stroke()
        ctx.arc(-half, half, half, 3 * math.pi / 2, 2 * math.pi)
        ctx.stroke()
    elif variant == 2:
        # Geometric "X" with central circular node
        ctx.move_to(-half, 0)
        ctx.line_to(half, 0)
        ctx.move_to(0, -half)
        ctx.line_to(0, half)
        ctx.stroke()
        ctx.arc(0, 0, size * 0.1, 0, 2 * math.pi)
        ctx.fill()
    else:
        # Multi-line/Nested effect
        for i in [0.3, 0.5, 0.7]:
            ctx.arc(-half, -half, size * i, 0, math.pi / 2)
            ctx.stroke()

    ctx.restore()

# --- GENERATIVE COMPOSITION ---

# 1. Background Structure Layer (Large, soft, geometric)
grid_size_bg = 120
for i in range(int(width / grid_size_bg) + 1):
    for j in range(int(height / grid_size_bg) + 1):
        x, y = i * grid_size_bg, j * grid_size_bg
        # Use a harmonic function to decide variant
        variant = int((math.sin(i * 0.5) + math.cos(j * 0.5) + 2)) % 2
        draw_truchet_cell(x, y, grid_size_bg, variant, (0.2, 0.3, 0.5, 0.15), 12)

# 2. Intermediate Logic Layer (Fluidity and Rhythm)
grid_size_mid = 40
for i in range(int(width / grid_size_mid)):
    for j in range(int(height / grid_size_mid)):
        x, y = i * grid_size_mid, j * grid_size_mid
        
        # Determine intensity based on distance from an organic "flow" center
        dist = math.sqrt((i - 7)**2 + (j - 6)**2)
        noise_val = random.random()
        
        if noise_val > 0.3:
            # Color shifts from cyan to magenta across the grid
            r = 0.2 + (i / 15) * 0.6
            g = 0.4
            b = 0.8 - (j / 12) * 0.4
            
            variant = random.randint(0, 1)
            # Offset every other row for an interlocking feel
            off_x = (j % 2) * (grid_size_mid / 2)
            draw_truchet_cell(x + off_x, y, grid_size_mid, variant, (r, g, b, 0.4), 1.5)

# 3. High-Frequency Staccato Layer (Swiss Precision & Vibrancy)
# This layer uses a smaller grid and higher contrast
grid_size_small = 20
ctx.set_operator(cairo.OPERATOR_ADD) # Additive blending for "glow"

for i in range(int(width / grid_size_small)):
    for j in range(int(height / grid_size_small)):
        # Strategic placement: use a math pattern to create "density clusters"
        density = math.sin(i * 0.2) * math.cos(j * 0.2)
        
        if density > 0.4:
            x, y = i * grid_size_small, j * grid_size_small
            
            # Bright highlight colors
            color_choice = random.choice([
                (1.0, 1.0, 1.0, 0.8), # Pure White
                (1.0, 0.1, 0.4, 0.7), # Swiss Red-ish
                (0.0, 0.9, 1.0, 0.7)  # Electric Cyan
            ])
            
            # High-frequency thin lines
            v = random.choice([0, 1, 3])
            draw_truchet_cell(x, y, grid_size_small, v, color_choice, 0.8, dashed=(random.random() > 0.8))

# 4. Final Accent: Global Interconnects
# Drawing long, sweeping Bezier paths that follow the Truchet "logic"
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_line_width(0.5)
ctx.set_source_rgba(1, 1, 1, 0.1)

for _ in range(12):
    start_x = random.randint(0, width)
    start_y = random.randint(0, height)
    ctx.move_to(start_x, start_y)
    
    curr_x, curr_y = start_x, start_y
    for _ in range(5):
        # Move in 90-degree steps to mimic grid-based wiring
        curr_x += random.choice([-grid_size_mid, grid_size_mid]) * 2
        curr_y += random.choice([-grid_size_mid, grid_size_mid]) * 2
        ctx.line_to(curr_x, curr_y)
    ctx.stroke()

# 5. Framing and Border
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Topography-like subtle Grain (Simulated with random points)
for _ in range(1000):
    gx = random.uniform(0, width)
    gy = random.uniform(0, height)
    ctx.set_source_rgba(1, 1, 1, 0.03)
    ctx.arc(gx, gy, 0.5, 0, 2 * math.pi)
    ctx.fill()
