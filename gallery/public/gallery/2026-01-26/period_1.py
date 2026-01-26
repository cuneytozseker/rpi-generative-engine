import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep "Terminal" Blue-Black
ctx.set_source_rgb(0.02, 0.03, 0.08)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
rings = 18
segments = 40
inner_radius = 20
outer_radius = 320

def to_polar_coords(r, theta, jitter=0):
    """Converts r, theta to cartesian with optional jitter."""
    # Add radial distortion based on angle for "entropy"
    distortion = math.sin(theta * 5) * 5 + math.cos(theta * 3) * 10
    r_final = r + distortion + random.uniform(-jitter, jitter)
    x = center_x + r_final * math.cos(theta)
    y = center_y + r_final * math.sin(theta)
    return x, y

# --- LAYER 1: The Radial Euclidean Grid ---
ctx.set_line_width(0.3)
ctx.set_source_rgba(0.2, 0.5, 1.0, 0.3)

for i in range(rings):
    r = inner_radius + (i / rings) * (outer_radius - inner_radius)
    ctx.arc(center_x, center_y, r, 0, 2 * math.pi)
    ctx.stroke()

for j in range(segments):
    theta = (j / segments) * 2 * math.pi
    x1, y1 = to_polar_coords(inner_radius, theta)
    x2, y2 = to_polar_coords(outer_radius, theta)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# --- LAYER 2: Dispersed Rectangular Primitives (Central Entropy) ---
# High density at center, thinning out at periphery
num_particles = 450
for _ in range(num_particles):
    # Normalized distribution favoring center
    t = 1.0 - random.random()**1.5
    r = inner_radius + t * (outer_radius - inner_radius)
    theta = random.uniform(0, 2 * math.pi)
    
    # Jitter increases with radius (entropy)
    jitter_amt = t * 25
    x, y = to_polar_coords(r, theta, jitter=jitter_amt)
    
    # Scale decreases with radius
    size = (1.0 - t) * 12 + 1
    
    # Rotation aligns to the radial vector
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(theta + random.uniform(-0.1, 0.1))
    
    # Geometric variety: Dithered blocks vs wireframes
    if random.random() > 0.4:
        ctx.set_source_rgba(0.9, 0.95, 1.0, 0.8) # High contrast white/blue
        ctx.rectangle(-size/2, -size/2, size, size * random.uniform(0.1, 2.0))
        if random.random() > 0.8:
            ctx.fill()
        else:
            ctx.set_line_width(0.5)
            ctx.stroke()
    else:
        # Crosshairs/Metadata ticks
        ctx.set_source_rgba(0.0, 0.8, 1.0, 0.6)
        ctx.set_line_width(0.4)
        ctx.move_to(-size, 0)
        ctx.line_to(size, 0)
        ctx.move_to(0, -size)
        ctx.line_to(0, size)
        ctx.stroke()
    ctx.restore()

# --- LAYER 3: Informational Overlays (Swiss Precision) ---
ctx.set_source_rgba(1.0, 1.0, 1.0, 0.9)
ctx.set_line_width(1.0)

# Circular "Scope" ring
ctx.set_dash([10, 5])
ctx.arc(center_x, center_y, outer_radius - 40, 0, 2 * math.pi)
ctx.stroke()
ctx.set_dash([])

# Axis Metadata (Ticks and labels)
for angle_deg in range(0, 360, 45):
    rad = math.radians(angle_deg)
    x_start, y_start = to_polar_coords(outer_radius + 5, rad)
    x_end, y_end = to_polar_coords(outer_radius + 25, rad)
    
    ctx.move_to(x_start, y_start)
    ctx.line_to(x_end, y_end)
    ctx.stroke()
    
    # Technical "block" at the end of axes
    ctx.rectangle(x_end-2, y_end-2, 4, 4)
    ctx.fill()

# --- LAYER 4: The Glitch Grid (Bottom-Right Metadata) ---
margin = 40
grid_size = 8
for i in range(6):
    for j in range(4):
        gx = width - margin - (i * 12)
        gy = height - margin - (j * 12)
        if random.random() > 0.3:
            ctx.set_source_rgb(0.0, 0.8, 1.0)
            ctx.rectangle(gx, gy, 8, 8)
            if random.random() > 0.7:
                ctx.fill()
            else:
                ctx.set_line_width(0.5)
                ctx.stroke()

# --- LAYER 5: Global Texture (Fine grain via lines) ---
ctx.set_source_rgba(1, 1, 1, 0.05)
for _ in range(1000):
    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    ctx.rectangle(tx, ty, 1, 1)
    ctx.fill()

# Fine connecting lines for "Network" feel in low energy zones
ctx.set_line_width(0.2)
ctx.set_source_rgba(1, 1, 1, 0.2)
for _ in range(30):
    r1 = random.uniform(inner_radius, outer_radius)
    a1 = random.uniform(0, math.pi * 2)
    r2 = r1 + random.uniform(-20, 20)
    a2 = a1 + random.uniform(-0.2, 0.2)
    
    p1 = to_polar_coords(r1, a1)
    p2 = to_polar_coords(r2, a2)
    
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.stroke()

