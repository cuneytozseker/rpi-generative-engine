import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Stark Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Center point
cx, cy = width / 2, height / 2

def polar_to_cartesian(r, theta, distortion_factor=0.0):
    # Apply a non-linear radial distortion based on frequency harmonics
    r_distorted = r * (1 + distortion_factor * math.sin(theta * 8) * math.cos(r * 0.02))
    x = cx + r_distorted * math.cos(theta)
    y = cy + r_distorted * math.sin(theta)
    return x, y

def draw_glyph(x, y, size, style="cross"):
    ctx.set_line_width(0.5)
    if style == "cross":
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
    elif style == "square":
        ctx.rectangle(x - size/2, y - size/2, size, size)
    ctx.stroke()

# 1. GENERATE LOGARITHMIC GRID SYSTEM
# Rings at power-law intervals to create technical depth
num_rings = 18
ring_base = 1.28
ctx.set_source_rgba(0.8, 0.8, 0.9, 0.15) # Faint technical lines

for i in range(1, num_rings + 1):
    radius = pow(ring_base, i) * 8
    ctx.set_line_width(0.3 if i % 3 != 0 else 0.8)
    
    # Draw distorted rings via segments
    steps = 200
    for j in range(steps + 1):
        theta = (j / steps) * 2 * math.pi
        x, y = polar_to_cartesian(radius, theta, distortion_factor=0.04)
        if j == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.stroke()

# 2. RADIAL PRECISION SECTORS
# Divide the space into functional "data domains"
num_sectors = 48
for i in range(num_sectors):
    theta = (i / num_sectors) * 2 * math.pi
    
    # Variable line lengths based on sector logic
    inner_r = 40
    outer_r = 220 + 30 * math.sin(i * 0.5)
    
    # Logic-based sparsity: skip certain sectors to create visual "voids"
    if (i % 7 == 0) or (20 < i < 25):
        continue

    x1, y1 = polar_to_cartesian(inner_r, theta, 0.02)
    x2, y2 = polar_to_cartesian(outer_r, theta, 0.02)
    
    ctx.set_source_rgba(0.9, 0.9, 1.0, 0.4)
    ctx.set_line_width(0.4)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 3. CONVERGENT NODES AND ANNOTATIONS
# Placing "chromatic data points" at specific intersections
random.seed(42) # Deterministic randomness for precision
for _ in range(60):
    # Select a random intersection on the grid
    r_idx = random.randint(5, num_rings)
    t_idx = random.randint(0, num_sectors)
    
    r = pow(ring_base, r_idx) * 8
    theta = (t_idx / num_sectors) * 2 * math.pi
    
    x, y = polar_to_cartesian(r, theta, 0.04)
    
    # Systematic markers
    chance = random.random()
    if chance > 0.85:
        # High-contrast "Event" markers (Cyan/Orange)
        if random.random() > 0.5:
            ctx.set_source_rgb(0.0, 0.8, 1.0) # Cobalt highlight
        else:
            ctx.set_source_rgb(1.0, 0.3, 0.0) # Signal orange
        draw_glyph(x, y, 4, "square")
    elif chance > 0.5:
        # Technical annotation markers
        ctx.set_source_rgba(1, 1, 1, 0.8)
        draw_glyph(x, y, 2, "cross")

# 4. ALGORITHMIC HATCHING (Tonal modulation)
# Creating texture through density rather than shading
ctx.set_source_rgba(0.5, 0.6, 1.0, 0.1)
for i in range(120):
    r = random.uniform(50, 200)
    theta = random.uniform(0, 2 * math.pi)
    x, y = polar_to_cartesian(r, theta, 0.04)
    
    # Draw tiny vertical ticks mimicking measurement scales
    angle_offset = theta + math.pi/2
    tick_len = 3
    ctx.move_to(x, y)
    ctx.line_to(x + math.cos(angle_offset)*tick_len, y + math.sin(angle_offset)*tick_len)
    ctx.set_line_width(0.3)
    ctx.stroke()

# 5. THE CENTRAL HUB
# Representing the "Attractor" with higher geometry density
ctx.set_source_rgb(1, 1, 1)
ctx.arc(cx, cy, 3, 0, 2 * math.pi)
ctx.fill()

# Protective circular mask to emphasize Swiss hierarchy
ctx.set_line_width(1.5)
ctx.set_source_rgb(1, 1, 1)
ctx.arc(cx, cy, 35, 0, 2 * math.pi)
ctx.stroke()

# Final detail: Distant "Satellite" systems
for orbit in [240, 245]:
    ctx.set_line_width(0.2)
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.arc(cx, cy, orbit, 0, 2 * math.pi)
    ctx.stroke()

# Visual balance: A single technical "legend" or marker
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.move_to(width - 60, height - 40)
ctx.line_to(width - 20, height - 40)
ctx.stroke()
ctx.rectangle(width - 60, height - 50, 5, 5)
ctx.fill()
