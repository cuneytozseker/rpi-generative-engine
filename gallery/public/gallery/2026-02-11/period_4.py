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

def get_distance_to_center(x, y):
    return math.sqrt((x - width/2)**2 + (y - height/2)**2)

def draw_glitch_line(x1, y1, x2, y2, weight, alpha):
    """Draws a line with a slight horizontal jitter to evoke a glitch aesthetic."""
    ctx.set_line_width(weight)
    ctx.set_source_rgba(0.9, 0.9, 1.0, alpha)
    
    jitter_amt = 2.5
    steps = 4
    ctx.move_to(x1, y1)
    for i in range(1, steps):
        t = i / steps
        px = x1 + (x2 - x1) * t + random.uniform(-jitter_amt, jitter_amt)
        py = y1 + (y2 - y1) * t
        ctx.line_to(px, py)
    ctx.line_to(x2, y2)
    ctx.stroke()

def recursive_partition(x, y, w, h, depth):
    """Recursive Quadtree-like partitioning with logic based on central density."""
    if depth <= 0:
        return []
    
    cx, cy = x + w/2, y + h/2
    dist = get_distance_to_center(cx, cy)
    
    # Split probability increases near the center (concentric density)
    # Normalized distance (0 to 1 roughly)
    norm_dist = dist / (math.sqrt(width**2 + height**2) / 2)
    split_prob = 0.85 * math.exp(-norm_dist * 2.0)
    
    nodes = []
    
    if random.random() < split_prob or depth > 4:
        # Determine split points (not exactly half to create variation)
        sw = w * random.uniform(0.4, 0.6)
        sh = h * random.uniform(0.4, 0.6)
        
        # Recurse into 4 quadrants
        nodes.extend(recursive_partition(x, y, sw, sh, depth - 1))
        nodes.extend(recursive_partition(x + sw, y, w - sw, sh, depth - 1))
        nodes.extend(recursive_partition(x, y + sh, sw, h - sh, depth - 1))
        nodes.extend(recursive_partition(x + sw, y + sh, w - sw, h - sh, depth - 1))
    else:
        # Base case: store the cell metadata
        nodes.append({'x': x, 'y': y, 'w': w, 'h': h, 'cx': cx, 'cy': cy})
        
    return nodes

# 1. GENERATE THE SYSTEMIC GRID
cells = recursive_partition(20, 20, width - 40, height - 40, 7)

# 2. DRAW RELATIONAL CONNECTIVITY (The "Vector Array")
# Connect nearby cell centers to simulate Voronoi-like adjacency
ctx.set_line_width(0.3)
for i in range(len(cells)):
    c1 = cells[i]
    # Check only a subset for performance and visual clarity
    for j in range(i + 1, min(i + 15, len(cells))):
        c2 = cells[j]
        d = math.sqrt((c1['cx'] - c2['cx'])**2 + (c1['cy'] - c2['cy'])**2)
        if d < 60:
            alpha = max(0, 0.4 - (d / 150))
            ctx.set_source_rgba(0.7, 0.8, 1.0, alpha)
            ctx.move_to(c1['cx'], c1['cy'])
            ctx.line_to(c2['cx'], c2['cy'])
            ctx.stroke()

# 3. DRAW CELL BOUNDARIES (The "Structural Integrity")
for cell in cells:
    dist = get_distance_to_center(cell['cx'], cell['cy'])
    # High contrast: inner cells are sharper, outer are ghost-like
    stroke_alpha = max(0.05, 0.6 - (dist / 400))
    
    # Draw rectangle with slight offset "glitch"
    ctx.set_source_rgba(1, 1, 1, stroke_alpha)
    ctx.set_line_width(0.5 if dist > 150 else 0.8)
    
    # Apply subtle gradient fill to simulate light depth within cells
    grad = cairo.RadialGradient(cell['cx'], cell['cy'], 2, cell['cx'], cell['cy'], cell['w'])
    grad.add_color_stop_rgba(0, 1, 1, 1, stroke_alpha * 0.2)
    grad.add_color_stop_rgba(1, 1, 1, 1, 0)
    ctx.set_source(grad)
    ctx.rectangle(cell['x']+1, cell['y']+1, cell['w']-2, cell['h']-2)
    ctx.fill()
    
    # Stroke the cell
    ctx.set_source_rgba(1, 1, 1, stroke_alpha)
    ctx.rectangle(cell['x'], cell['y'], cell['w'], cell['h'])
    ctx.stroke()

# 4. OVERLAY STOCHASTIC JITTER (The "Entropy")
# Draw long hair-like horizontal lines to break the vertical hierarchy
for _ in range(30):
    ry = random.uniform(50, height-50)
    rx_start = random.uniform(0, width * 0.3)
    rx_end = random.uniform(width * 0.7, width)
    draw_glitch_line(rx_start, ry, rx_end, ry, 0.2, random.uniform(0.1, 0.3))

# 5. FOCAL NODES (The "Precision Elements")
# Small circular markers at specific high-density intersections
for cell in cells:
    if random.random() > 0.92:
        ctx.set_source_rgba(1, 1, 1, 0.9)
        ctx.arc(cell['x'], cell['y'], 1.5, 0, 2 * math.pi)
        ctx.fill()
        
        # Technical annotation lines (Swiss style)
        if random.random() > 0.8:
            ctx.set_line_width(0.4)
            ctx.move_to(cell['x'], cell['y'])
            ctx.line_to(cell['x'] + 15, cell['y'] - 15)
            ctx.stroke()
            ctx.move_to(cell['x'] + 15, cell['y'] - 15)
            ctx.line_to(cell['x'] + 40, cell['y'] - 15)
            ctx.stroke()

# 6. CENTRAL VOID DEPTH
# Dark radial overlay to focus the viewer's eye on the "Core"
void_grad = cairo.RadialGradient(width/2, height/2, 50, width/2, height/2, 350)
void_grad.add_color_stop_rgba(0, 0, 0, 0, 0)
void_grad.add_color_stop_rgba(1, 0, 0, 0, 0.6)
ctx.set_source(void_grad)
ctx.rectangle(0, 0, width, height)
ctx.fill()

