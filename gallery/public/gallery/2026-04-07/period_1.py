import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal / Blueprint style
ctx.set_source_rgb(0.04, 0.04, 0.06)
ctx.paint()

# Constants
CX, CY = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
NUM_RINGS = 24
NUM_SPOKES = 32

def draw_glitch_line(ctx, x1, y1, x2, y2, segments=4):
    """Draws a line as a series of slightly offset segments for a 'staccato' effect."""
    dx = (x2 - x1) / segments
    dy = (y2 - y1) / segments
    for i in range(segments):
        if random.random() > 0.1: # Systematic omission
            off_x = random.uniform(-0.5, 0.5)
            off_y = random.uniform(-0.5, 0.5)
            ctx.move_to(x1 + dx * i + off_x, y1 + dy * i + off_y)
            ctx.line_to(x1 + dx * (i + 0.8) + off_x, y1 + dy * (i + 0.8) + off_y)
            ctx.stroke()

def polar_to_cartesian(r, theta, distortion_factor=0.0):
    """Converts polar to cartesian with a radial distortion based on angle."""
    # Radial distortion creates the 'Annotated Flow' movement
    distorted_r = r * (1 + distortion_factor * math.sin(theta * 6))
    x = CX + distorted_r * math.cos(theta)
    y = CY + distorted_r * math.sin(theta)
    return x, y

# --- Layer 1: The Systematic Polar Grid ---
ctx.set_line_width(0.4)
ctx.set_source_rgba(0.8, 0.8, 0.9, 0.3)

for i in range(NUM_RINGS):
    # Non-linear spacing (power function) for depth
    r = math.pow(i / NUM_RINGS, 1.2) * MAX_RADIUS
    
    # Distortion intensity increases with radius
    d_factor = (i / NUM_RINGS) * 0.12
    
    ctx.new_sub_path()
    for step in range(200):
        theta = (step / 200) * 2 * math.pi
        x, y = polar_to_cartesian(r, theta, d_factor)
        if step == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.close_path()
    ctx.stroke()

# --- Layer 2: Vector Flow Spanning ---
ctx.set_source_rgba(0.2, 0.6, 1.0, 0.6) # Technical Blue
ctx.set_line_width(0.7)

for s in range(NUM_SPOKES):
    theta_base = (s / NUM_SPOKES) * 2 * math.pi
    
    # Draw radial lines with "staccato" breaks
    for i in range(NUM_RINGS - 1):
        r1 = math.pow(i / NUM_RINGS, 1.2) * MAX_RADIUS
        r2 = math.pow((i + 1) / NUM_RINGS, 1.2) * MAX_RADIUS
        
        d1 = (i / NUM_RINGS) * 0.12
        d2 = ((i+1) / NUM_RINGS) * 0.12
        
        x1, y1 = polar_to_cartesian(r1, theta_base, d1)
        x2, y2 = polar_to_cartesian(r2, theta_base, d2)
        
        # Only draw based on a mathematical pattern (Swiss hierarchy)
        if (s % 4 == 0) or (i % 3 == 0):
            draw_glitch_line(ctx, x1, y1, x2, y2, segments=2)

# --- Layer 3: Technical Annotations & Nodes ---
# Colors represent "data states"
node_colors = [
    (0.9, 0.2, 0.3), # Primary Red
    (1.0, 0.8, 0.1), # Primary Yellow
    (0.9, 0.9, 0.9)  # White
]

for i in range(1, NUM_RINGS):
    r = math.pow(i / NUM_RINGS, 1.2) * MAX_RADIUS
    d_factor = (i / NUM_RINGS) * 0.12
    
    for s in range(NUM_SPOKES):
        theta = (s / NUM_SPOKES) * 2 * math.pi
        
        # Place annotations at specific algorithmic intersections
        if (i * s) % 17 == 0:
            x, y = polar_to_cartesian(r, theta, d_factor)
            
            # Select categorical color
            ctx.set_source_rgb(*random.choice(node_colors))
            
            # Draw "Blueprint" Glyphs
            style = random.randint(0, 2)
            if style == 0: # Small Cross
                size = 3
                ctx.move_to(x - size, y)
                ctx.line_to(x + size, y)
                ctx.move_to(x, y - size)
                ctx.line_to(x, y + size)
                ctx.set_line_width(0.5)
                ctx.stroke()
            elif style == 1: # Hollow Square
                size = 2
                ctx.rectangle(x - size, y - size, size * 2, size * 2)
                ctx.set_line_width(0.8)
                ctx.stroke()
            elif style == 2: # Micro Label (Geometric)
                ctx.rectangle(x + 4, y - 1, 6, 2)
                ctx.fill()

# --- Layer 4: Floating Geometric Voids ---
# Large subtle circles to create asymmetrical balance
ctx.set_source_rgba(1, 1, 1, 0.03)
for _ in range(5):
    vx = random.uniform(0, width)
    vy = random.uniform(0, height)
    vr = random.uniform(20, 100)
    ctx.arc(vx, vy, vr, 0, 2 * math.pi)
    ctx.fill()

# --- Final Polish: Frame/Margin ---
ctx.set_source_rgba(1, 1, 1, 0.8)
ctx.set_line_width(1)
margin = 20
ctx.rectangle(margin, margin, width - margin*2, height - margin*2)
ctx.stroke()

# Technical label placeholder (Small rects as typography)
ctx.set_source_rgb(0.9, 0.9, 0.9)
ctx.rectangle(margin + 10, height - margin - 15, 40, 2)
ctx.rectangle(margin + 10, height - margin - 10, 25, 2)
ctx.fill()

