import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Technical Navy
ctx.set_source_rgb(0.01, 0.02, 0.05)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
SIDES = 8  # Principal axes of the Swiss radial grid

def to_polar_coords(u, v, distortion=0.15):
    """
    Transforms normalized (0-1) u, v coordinates into a distorted polar space.
    u maps to radius, v maps to angle.
    """
    # Map u to radius with a slight power curve for density distribution
    r = u * MAX_RADIUS
    
    # Map v to a full circle (0 to 2*PI)
    theta = v * 2 * math.pi
    
    # Apply radial distortion based on harmonic oscillation
    # Creates a 'breathing' geometric effect
    r_distorted = r * (1 + distortion * math.sin(SIDES * theta))
    
    x = CENTER_X + r_distorted * math.cos(theta)
    y = CENTER_Y + r_distorted * math.sin(theta)
    return x, y

def draw_distorted_line(u1, v1, u2, v2, segments=30):
    """Draws a line in the transformed coordinate space by interpolating segments."""
    for i in range(segments + 1):
        t = i / segments
        curr_u = u1 + (u2 - u1) * t
        curr_v = v1 + (v2 - v1) * t
        px, py = to_polar_coords(curr_u, curr_v)
        if i == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    ctx.stroke()

def draw_glyph(u, v, size=3):
    """Draws a technical marker (cross or circle) at the data node."""
    px, py = to_polar_coords(u, v)
    ctx.save()
    ctx.set_line_width(0.7)
    # Crosshair
    ctx.move_to(px - size, py)
    ctx.line_to(px + size, py)
    ctx.move_to(px, py - size)
    ctx.line_to(px, py + size)
    ctx.stroke()
    # Tiny circle
    ctx.arc(px, py, size/2, 0, 2*math.pi)
    ctx.stroke()
    ctx.restore()

# 1. THE RADIAL GRID (Primary Territories)
ctx.set_line_width(0.4)
ctx.set_source_rgba(0.2, 0.5, 0.8, 0.4) # Faint blueprint blue

# Draw concentric rings (Radial divisions)
for r_step in [0.2, 0.4, 0.6, 0.8, 1.0]:
    draw_distorted_line(r_step, 0, r_step, 1.0, segments=120)

# Draw spokes (Angular divisions)
for theta_step in range(SIDES * 2):
    draw_distorted_line(0, theta_step/(SIDES * 2), 1.0, theta_step/(SIDES * 2), segments=20)

# 2. RECURSIVE SUBDIVISION (The "Data Mapping")
# We use a quadtree-like logic on the (u, v) plane before transforming it
def subdivide(u, v, w, h, depth):
    if depth > 4 or (depth > 1 and random.random() < 0.3):
        # Draw the resulting "cell" in the systematic map
        ctx.set_source_rgba(0.9, 0.9, 1.0, 0.8) # Stark white/blue
        ctx.set_line_width(0.6)
        
        # Draw edges of the mapped cell
        draw_distorted_line(u, v, u+w, v, 20)
        draw_distorted_line(u+w, v, u+w, v+h, 20)
        draw_distorted_line(u+w, v+h, u, v+h, 20)
        draw_distorted_line(u, v+h, u, v, 20)
        
        # Chance to add a "node" connection or glyph
        if random.random() > 0.5:
            ctx.set_source_rgba(0.0, 0.8, 1.0, 0.9) # Data highlight
            draw_glyph(u + w/2, v + h/2, size=random.uniform(1, 4))
        return

    # Split logic
    if random.random() > 0.5:
        subdivide(u, v, w/2, h, depth+1)
        subdivide(u+w/2, v, w/2, h, depth+1)
    else:
        subdivide(u, v, w, h/2, depth+1)
        subdivide(u, v+h/2, w, h/2, depth+1)

# Seed for reproducibility of the specific systematic layout
random.seed(42)
subdivide(0.1, 0, 0.8, 1.0, 0)

# 3. NETWORK OVERLAY (Global Connections)
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_line_width(0.2)
nodes = [(random.uniform(0.2, 1.0), random.random()) for _ in range(12)]
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        # Only connect nodes that are somewhat close in radial space
        if abs(nodes[i][0] - nodes[j][0]) < 0.4:
            draw_distorted_line(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1], 40)

# 4. MICRO-GLYPHS AND MARGINS
ctx.set_source_rgb(0.5, 0.6, 0.7)
ctx.set_line_width(1.0)
# Scale markers at the corners
for i in range(0, 5):
    ctx.move_to(20 + i*10, height - 20)
    ctx.line_to(20 + i*10, height - (25 if i % 2 == 0 else 30))
    ctx.stroke()

# Textual abstraction (Simulated data readout)
def draw_micro_block(x, y):
    ctx.rectangle(x, y, 15, 2)
    ctx.fill()
    ctx.rectangle(x, y+4, 10, 2)
    ctx.fill()

ctx.set_source_rgba(0.5, 0.6, 0.7, 0.5)
draw_micro_block(20, 20)
draw_micro_block(width - 40, 20)
draw_micro_block(width - 40, height - 30)

# 5. FINAL CENTER FOCUS
ctx.set_source_rgb(1, 1, 1)
ctx.arc(CENTER_X, CENTER_Y, 2, 0, 2 * math.pi)
ctx.fill()
ctx.set_line_width(0.5)
ctx.arc(CENTER_X, CENTER_Y, 10, 0, 2 * math.pi)
ctx.stroke()

# Finished composition
