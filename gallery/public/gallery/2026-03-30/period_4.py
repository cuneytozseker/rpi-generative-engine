import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Constants
PHI = (1 + 5**0.5) / 2
BG_COLOR = (0.05, 0.05, 0.07)
ACCENT_COLOR = (1.0, 0.2, 0.1) # International Orange
NEUTRAL_LIGHT = (0.9, 0.9, 0.9)

# Background
ctx.set_source_rgb(*BG_COLOR)
ctx.paint()

def get_noise_offset(x, y, scale=0.005, magnitude=15):
    """Simulates a low-frequency flow field using trigonometric functions."""
    angle = math.sin(x * scale) * math.cos(y * scale) * math.pi * 2
    dx = math.cos(angle) * magnitude
    dy = math.sin(angle) * magnitude
    return dx, dy

def draw_stochastic_grain(x, y, w, h, density):
    """Creates digital grain texture through variable-frequency dithering."""
    ctx.set_line_width(0.5)
    num_dots = int(w * h * density)
    for _ in range(num_dots):
        px = x + random.random() * w
        py = y + random.random() * h
        
        # Perturb point based on flow field
        dx, dy = get_noise_offset(px, py)
        
        ctx.set_source_rgba(0.8, 0.8, 0.8, random.uniform(0.1, 0.4))
        ctx.arc(px + dx, py + dy, 0.6, 0, 2 * math.pi)
        ctx.fill()

def draw_shard(points, alpha=0.8, color=NEUTRAL_LIGHT):
    """Draws a fragment/shard with a technical aesthetic."""
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)
    ctx.set_line_width(0.7)
    
    ctx.move_to(points[0][0], points[0][1])
    for p in points[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    
    if random.random() > 0.7:
        ctx.fill()
    else:
        ctx.stroke()

def recursive_subdivide(x, y, w, h, depth):
    if depth <= 0 or w < 10 or h < 10:
        # Base case: draw texture and shards
        density = (1.0 / (depth + 1)) * 0.15
        draw_stochastic_grain(x, y, w, h, density)
        
        # Draw distorted structural lines (shards)
        if random.random() > 0.4:
            p1 = (x, y)
            p2 = (x + w, y)
            p3 = (x + w, y + h)
            p4 = (x, y + h)
            
            # Apply kinetic entropy to corners
            corners = []
            for px, py in [p1, p2, p3, p4]:
                dx, dy = get_noise_offset(px, py, magnitude=20)
                corners.append((px + dx, py + dy))
            
            # Draw structural shard
            draw_shard(corners, alpha=random.uniform(0.2, 0.6))
            
            # Potential chromatic accent at intersections
            if random.random() > 0.92:
                ctx.set_source_rgb(*ACCENT_COLOR)
                ctx.arc(corners[0][0], corners[0][1], 2, 0, 2 * math.pi)
                ctx.fill()
        return

    # Golden ratio subdivision logic
    split_horizontally = w > h
    
    # Non-linear coordinate architecture: favor central weight
    # We use PHI to determine the split point
    if split_horizontally:
        nw = w / PHI
        if random.random() > 0.5:
            recursive_subdivide(x, y, nw, h, depth - 1)
            recursive_subdivide(x + nw, y, w - nw, h, depth - 1)
        else:
            recursive_subdivide(x, y, w - nw, h, depth - 1)
            recursive_subdivide(x + (w - nw), y, nw, h, depth - 1)
    else:
        nh = h / PHI
        if random.random() > 0.5:
            recursive_subdivide(x, y, w, nh, depth - 1)
            recursive_subdivide(x, y + nh, w, h - nh, depth - 1)
        else:
            recursive_subdivide(x, y, w, h - nh, depth - 1)
            recursive_subdivide(x, y + (h - nh), w, nh, depth - 1)

# Main Execution
# Start with a slightly padded container
margin = 40
main_w, main_h = width - margin*2, height - margin*2

# Layer 1: Systematic Grid Background
ctx.set_source_rgba(0.2, 0.2, 0.3, 0.1)
ctx.set_line_width(0.5)
grid_steps = 12
for i in range(grid_steps + 1):
    # Logarithmic-ish spacing for the grid lines
    pos_x = margin + main_w * (math.log1p(i) / math.log1p(grid_steps))
    pos_y = margin + main_h * (math.log1p(i) / math.log1p(grid_steps))
    
    ctx.move_to(pos_x, margin)
    ctx.line_to(pos_x, height - margin)
    ctx.move_to(margin, pos_y)
    ctx.line_to(width - margin, pos_y)
ctx.stroke()

# Layer 2: Recursive Golden Ratio Shards
recursive_subdivide(margin, margin, main_w, main_h, 7)

# Layer 3: High-contrast Peripheral Fragmentation
# Overlaying some larger "glitch" elements at the edges
for _ in range(15):
    edge_x = random.choice([random.uniform(0, 100), random.uniform(width-100, width)])
    edge_y = random.uniform(0, height)
    
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.rectangle(edge_x, edge_y, random.uniform(5, 50), 1)
    ctx.fill()

# Final polish: Technical markings
ctx.set_source_rgb(*NEUTRAL_LIGHT)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.move_to(width - 80, height - 15)
ctx.show_text("SYS_REF: PHI_v.04")

ctx.set_line_width(1)
ctx.move_to(20, 20)
ctx.line_to(40, 20)
ctx.move_to(20, 20)
ctx.line_to(20, 40)
ctx.stroke() # Top-left bracket

# End of code
