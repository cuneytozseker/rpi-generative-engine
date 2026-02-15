import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Constants
PHI = (1 + 5**0.5) / 2
PALETTE = [
    (0.95, 0.95, 0.90), # Cream
    (1.0, 0.2, 0.3),    # Crimson
    (0.1, 0.6, 0.8),    # Azure
    (1.0, 0.8, 0.0),    # Gold
]

# Background: Deep Ebony
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

def draw_flow_cell(x, y, w, h, depth):
    """Fills a subdivided cell with dense, flow-based line work."""
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    
    # Calculate density based on cell size and depth
    num_paths = int(40 + (depth * 20))
    
    # Directionality based on golden ratio proportions
    angle_offset = (x + y) * 0.01
    
    for i in range(num_paths):
        # Chromatic fragmentation
        r, g, b = random.choice(PALETTE)
        alpha = random.uniform(0.1, 0.4)
        ctx.set_source_rgba(r, g, b, alpha)
        
        # Modulated stroke weights
        ctx.set_line_width(random.uniform(0.2, 1.5))
        
        # Path generation: tension between rigidity and flux
        start_x = x + random.uniform(0, w)
        start_y = y + random.uniform(0, h)
        
        ctx.move_to(start_x, start_y)
        
        cur_x, cur_y = start_x, start_y
        steps = random.randint(10, 30)
        step_len = (w + h) / 40
        
        for s in range(steps):
            # Vector-based flow logic
            # Influence angle by distance from center and recursive depth
            cx, cy = x + w/2, y + h/2
            dist_to_center = math.sqrt((cur_x - cx)**2 + (cur_y - cy)**2)
            angle = math.atan2(cur_y - cy, cur_x - cx) + (PHI * s * 0.1) + angle_offset
            
            cur_x += math.cos(angle) * step_len
            cur_y += math.sin(angle) * step_len
            
            # Subtle curvature towards the diagonal
            ctx.line_to(cur_x, cur_y)
            
        ctx.stroke()
        
    # Draw a fine border for the subdivision (Swiss precision)
    ctx.set_source_rgba(1, 1, 1, 0.15)
    ctx.set_line_width(0.5)
    ctx.rectangle(x, y, w, h)
    ctx.stroke()
    ctx.restore()

def subdivide(x, y, w, h, depth, max_depth):
    """Recursive subdivision using Golden Ratio proportions."""
    if depth >= max_depth or (w < 40 or h < 40):
        draw_flow_cell(x, y, w, h, depth)
        return

    # Decide split direction based on aspect ratio (maintaining Golden Ratio)
    if w > h:
        # Split width
        w_prime = w / PHI
        if random.random() > 0.1:
            subdivide(x, y, w_prime, h, depth + 1, max_depth)
            subdivide(x + w_prime, y, w - w_prime, h, depth + 1, max_depth)
        else:
            draw_flow_cell(x, y, w, h, depth)
    else:
        # Split height
        h_prime = h / PHI
        if random.random() > 0.1:
            subdivide(x, y, w, h_prime, depth + 1, max_depth)
            subdivide(x, y + h_prime, w, h - h_prime, depth + 1, max_depth)
        else:
            draw_flow_cell(x, y, w, h, depth)

# Main Execution
# We use additive blending for "light interference" effects in line intersections
ctx.set_operator(cairo.OPERATOR_ADD)

# Start recursion from a slightly padded area for aesthetic margins
margin = 40
subdivide(margin, margin, width - margin*2, height - margin*2, 0, 5)

# Secondary overlay: Structural "Skeleton"
# Adds a few large, transparent geometric shapes to anchor the "structured entropy"
ctx.set_operator(cairo.OPERATOR_OVERLAY)
for _ in range(3):
    ctx.set_source_rgba(1, 1, 1, 0.03)
    r = random.uniform(100, 250)
    ctx.arc(random.uniform(0, width), random.uniform(0, height), r, 0, 2*math.pi)
    ctx.fill()

# Final high-contrast geometric signature (Swiss minimalism)
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.move_to(width - 60, height - 40)
ctx.line_to(width - 40, height - 40)
ctx.stroke()
ctx.move_to(width - 50, height - 50)
ctx.line_to(width - 50, height - 30)
ctx.stroke()

