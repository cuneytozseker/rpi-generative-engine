import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep architectural black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def rotate_point(x, y, angle, cx, cy):
    """Rotates a point (x, y) around a center (cx, cy)."""
    s = math.sin(angle)
    c = math.cos(angle)
    x -= cx
    y -= cy
    new_x = x * c - y * s
    new_y = x * s + y * c
    return new_x + cx, new_y + cy

def draw_info_grid(angle, spacing, color, line_width, entropy=0):
    """Draws a grid of lines at a specific angle with optional jitter."""
    ctx.set_source_rgba(*color)
    ctx.set_line_width(line_width)
    
    # Calculate a large enough area to cover the surface when rotated
    diag = int(math.sqrt(width**2 + height**2))
    offset = (diag - width) // 2
    
    for i in range(-offset, width + offset, spacing):
        # Start and end points for lines spanning the canvas
        x1, y1 = i, -offset
        x2, y2 = i, height + offset
        
        # Apply rotation around center
        rx1, ry1 = rotate_point(x1, y1, angle, width/2, height/2)
        rx2, ry2 = rotate_point(x2, y2, angle, width/2, height/2)
        
        # Add 'Entropy' - breaking the mathematical rigidity
        if entropy > 0:
            shift = random.uniform(-entropy, entropy)
            rx1 += shift
            ry2 += shift

        ctx.move_to(rx1, ry1)
        ctx.line_to(rx2, ry2)
        ctx.stroke()

def draw_metadata_node(x, y, scale):
    """Draws a 'data packet' node: a combination of circles, crosses, and blocks."""
    ctx.set_line_width(0.5)
    ctx.set_source_rgba(0.9, 0.9, 1.0, 0.8)
    
    # Euclidean crosshair
    ctx.move_to(x - scale, y)
    ctx.line_to(x + scale, y)
    ctx.move_to(x, y - scale)
    ctx.line_to(x, y + scale)
    ctx.stroke()
    
    # Recursive circle
    ctx.arc(x, y, scale * 0.4, 0, 2 * math.pi)
    ctx.stroke()
    
    # Segmented data block (pixelated aesthetic)
    if random.random() > 0.5:
        ctx.rectangle(x + scale*0.5, y + scale*0.5, scale*0.3, scale*0.3)
        ctx.fill()

# --- 1. BASE LAYER: The Static System ---
# Primary vertical grid
draw_info_grid(math.radians(0), 6, (0.2, 0.3, 0.4, 0.3), 0.5)

# --- 2. MOIRÉ LAYER: The Rotating Interference ---
# Secondary grid slightly rotated to create the Moiré effect
# The interaction of these two creates complex 'Architecture of Information'
draw_info_grid(math.radians(3.5), 6, (0.8, 0.8, 0.9, 0.4), 0.7)

# --- 3. VECTOR FLOW: Dynamic Striated Rectangles ---
# Simulating data packets flowing along a vector field
for _ in range(15):
    vx = random.randint(50, width-50)
    vy = random.randint(50, height-50)
    vw = random.randint(40, 150)
    vh = random.randint(2, 8)
    
    # Modulated by 'Flow Field' logic (using sine for wave-like movement)
    angle_offset = math.sin(vx * 0.01) * 0.2
    
    ctx.save()
    ctx.translate(vx, vy)
    ctx.rotate(angle_offset)
    
    # Draw a striated (lined) rectangle
    ctx.set_source_rgba(0.0, 0.6, 1.0, 0.4)
    for j in range(0, vh, 2):
        ctx.rectangle(0, j, vw, 0.5)
        ctx.fill()
    ctx.restore()

# --- 4. HIERARCHICAL NODES: Focal Points ---
# Distribute nodes based on a mathematical progression
for i in range(5):
    for j in range(4):
        # Systematic placement with controlled jitter
        nx = (i + 1) * (width / 6) + random.uniform(-10, 10)
        ny = (j + 1) * (height / 5) + random.uniform(-10, 10)
        
        # Interaction: Draw nodes where grids might 'interface'
        draw_metadata_node(nx, ny, 12)

# --- 5. ANNOTATIONS: Coordinate System ---
# Small ticks and labels along the edges for the blueprint aesthetic
ctx.set_source_rgba(1, 1, 1, 0.6)
ctx.set_line_width(1.0)
for k in range(0, width, 40):
    # Top margin ticks
    ctx.move_to(k, 0)
    ctx.line_to(k, 10)
    # Bottom margin blocks
    if k % 80 == 0:
        ctx.rectangle(k, height-15, 20, 2)
        ctx.fill()
ctx.stroke()

# --- 6. ENTROPY: Signal Jitter ---
# A final layer of thin, broken lines representing signal noise
for _ in range(20):
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ex = random.randint(0, width)
    ey = random.randint(0, height)
    ctx.move_to(ex, ey)
    ctx.line_to(ex + random.randint(50, 200), ey + random.uniform(-2, 2))
    ctx.set_line_width(0.2)
    ctx.stroke()

# Final visual rhythm through negative space preservation
# (The code naturally creates dense clusters and sparse areas)
