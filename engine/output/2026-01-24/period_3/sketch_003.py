import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Constants
PHI = (1 + 5**0.5) / 2
ITERATIONS = 8

def draw_technical_mark(x, y, size=3):
    """Draws small Swiss-style crosshairs at coordinates."""
    ctx.set_line_width(0.5)
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

def draw_density_pattern(x, y, w, h, density_type):
    """Fills a cell with mathematical texture based on a type."""
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    
    if density_type == "network":
        # Draw a network of points connected by high-transparency lines
        points = [(x + random.random() * w, y + random.random() * h) for _ in range(8)]
        ctx.set_source_rgba(1, 1, 1, 0.15)
        ctx.set_line_width(0.3)
        for i, p1 in enumerate(points):
            for p2 in points[i+1:]:
                ctx.move_to(p1[0], p1[1])
                ctx.line_to(p2[0], p2[1])
                ctx.stroke()
                
    elif density_type == "rhythm":
        # Draw modulated vertical bars
        steps = 12
        for i in range(steps):
            norm = i / steps
            pos_x = x + norm * w
            weight = 0.2 + (math.sin(norm * math.pi) * 1.5)
            ctx.set_source_rgba(1, 1, 1, 0.4)
            ctx.set_line_width(weight)
            ctx.move_to(pos_x, y)
            ctx.line_to(pos_x, y + h)
            ctx.stroke()
            
    elif density_type == "concentric":
        # Recursive squares within the cell
        ctx.set_source_rgba(1, 1, 1, 0.2)
        ctx.set_line_width(0.5)
        margin = min(w, h) * 0.1
        for i in range(1, 5):
            d = i * margin
            ctx.rectangle(x + d, y + d, w - 2*d, h - 2*d)
            ctx.stroke()

    ctx.restore()

def subdivide(x, y, w, h, depth):
    if depth <= 0 or w < 10 or h < 10:
        # Base case: Draw content in the leaf node
        style = random.choice(["network", "rhythm", "concentric", "empty"])
        if style != "empty":
            draw_density_pattern(x, y, w, h, style)
        
        # Draw border with varying alpha for "earned grey" effect
        ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.6))
        ctx.set_line_width(0.5)
        ctx.rectangle(x, y, w, h)
        ctx.stroke()
        
        # Annotate with technical marks
        if random.random() > 0.7:
            draw_technical_mark(x, y)
        return

    # Decide split orientation based on aspect ratio
    split_horizontally = w < h
    
    # Golden Ratio split
    if split_horizontally:
        h1 = h / PHI
        h2 = h - h1
        # Randomly swap weights for asymmetry
        if random.random() > 0.5: h1, h2 = h2, h1
        
        subdivide(x, y, w, h1, depth - 1)
        subdivide(x, y + h1, w, h2, depth - 1)
    else:
        w1 = w / PHI
        w2 = w - w1
        if random.random() > 0.5: w1, w2 = w2, w1
        
        subdivide(x, y, w1, h, depth - 1)
        subdivide(x + w1, y, w2, h, depth - 1)

# Execution
# 1. Background grid (Subtle)
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.2)
grid_size = 20
for i in range(0, width, grid_size):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
for i in range(0, height, grid_size):
    ctx.move_to(0, i)
    ctx.line_to(width, i)
    ctx.stroke()

# 2. Recursive Geometry
subdivide(40, 40, width - 80, height - 80, ITERATIONS)

# 3. Secondary Network Overlays
# Connecting random subdivision hubs with long, sweeping lines
ctx.set_source_rgba(1, 1, 1, 0.08)
ctx.set_line_width(0.5)
for _ in range(5):
    ctx.move_to(random.randint(0, width), 0)
    ctx.line_to(random.randint(0, width), height)
    ctx.stroke()

# 4. Focal Elements (Swiss Precision)
# Small data-like labels or points of interest
for _ in range(10):
    fx, fy = random.randint(50, width-50), random.randint(50, height-50)
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.arc(fx, fy, 1.5, 0, 2*math.pi)
    ctx.fill()
    
    # Tiny leader lines
    ctx.set_line_width(0.4)
    ctx.move_to(fx, fy)
    ctx.line_to(fx + 15, fy - 15)
    ctx.line_to(fx + 30, fy - 15)
    ctx.stroke()

# Final border
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.set_line_width(2)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()
