import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal / Blueprint Void
ctx.set_source_rgb(0.05, 0.07, 0.1)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
PALETTE = [
    (0.92, 0.92, 0.95, 0.8),  # Technical White
    (0.85, 0.65, 0.20, 0.7),  # Mustard
    (0.75, 0.35, 0.25, 0.7),  # Terracotta
    (0.20, 0.50, 0.55, 0.6),  # Muted Teal
]

def polar_to_cartesian(r, theta):
    """Converts polar coordinates to cartesian with a slight radial distortion."""
    # Radial distortion: subtle noise-like modulation based on angle
    distortion = 1.0 + 0.03 * math.sin(theta * 8) * math.cos(theta * 3)
    dist_r = r * distortion
    return CENTER_X + dist_r * math.cos(theta), CENTER_Y + dist_r * math.sin(theta)

def draw_flow_lines(r_min, r_max, t_min, t_max, density):
    """Fills a polar cell with constrained flow paths."""
    ctx.set_line_width(0.4)
    for _ in range(density):
        # Choose a random starting point in the cell
        curr_r = random.uniform(r_min, r_max)
        curr_t = random.uniform(t_min, t_max)
        
        ctx.set_source_rgba(*random.choice(PALETTE))
        
        ctx.move_to(*polar_to_cartesian(curr_r, curr_t))
        
        # Walk through the vector field
        steps = random.randint(5, 15)
        for _ in range(steps):
            # The flow is influenced by the radial distance and a spiral component
            angle_step = 0.05 * math.sin(curr_r * 0.05)
            radial_step = 2.0 * math.cos(curr_t * 2)
            
            curr_t += angle_step
            curr_r += radial_step
            
            # Constrain to cell or let it bleed slightly
            if not (r_min - 10 < curr_r < r_max + 10): break
            
            x, y = polar_to_cartesian(curr_r, curr_t)
            ctx.line_to(x, y)
        ctx.stroke()

def draw_annotations(r, theta, size=2):
    """Draws technical markers at grid junctions."""
    ctx.set_source_rgba(0.92, 0.92, 0.95, 0.5)
    ctx.set_line_width(0.8)
    x, y = polar_to_cartesian(r, theta)
    
    # Tiny crosshairs
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()
    
    if random.random() > 0.8:
        # Small circle 'data point'
        ctx.arc(x, y, size * 0.5, 0, 2 * math.pi)
        ctx.stroke()

def subdivide(r_min, r_max, t_min, t_max, depth):
    """Recursively subdivides polar space into a hierarchical grid."""
    
    # Base case or random stop to create irregular Swiss structure
    if depth > 4 or (depth > 1 and random.random() < 0.25):
        # Draw cell boundaries (The "Bones")
        ctx.set_source_rgba(0.9, 0.9, 0.95, 0.15)
        ctx.set_line_width(0.5)
        
        # Arc segment
        ctx.arc(CENTER_X, CENTER_Y, r_min, t_min, t_max)
        ctx.stroke()
        
        # Radial segments
        x1, y1 = polar_to_cartesian(r_min, t_min)
        x2, y2 = polar_to_cartesian(r_max, t_min)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
        # Draw internal "Entropy"
        flow_density = int((r_max - r_min) * (t_max - t_min) * 0.5)
        draw_flow_lines(r_min, r_max, t_min, t_max, max(5, flow_density))
        
        # Draw annotations at corners
        draw_annotations(r_min, t_min)
        return

    # Decide split direction: 0 for radial (rings), 1 for angular (wedges)
    split_dir = random.choice([0, 1])
    
    # Golden ratio-ish split for more dynamic hierarchy
    split_factor = random.uniform(0.38, 0.62)
    
    if split_dir == 0:
        mid_r = r_min + (r_max - r_min) * split_factor
        subdivide(r_min, mid_r, t_min, t_max, depth + 1)
        subdivide(mid_r, r_max, t_min, t_max, depth + 1)
    else:
        mid_t = t_min + (t_max - t_min) * split_factor
        subdivide(r_min, r_max, t_min, mid_t, depth + 1)
        subdivide(r_min, r_max, mid_t, t_max, depth + 1)

# Execution
# Draw background noise/texture
for _ in range(200):
    ctx.set_source_rgba(1, 1, 1, 0.03)
    ctx.arc(random.uniform(0, width), random.uniform(0, height), random.uniform(0.5, 1.5), 0, 2*math.pi)
    ctx.fill()

# Start subdivision from the center outwards
num_primary_sectors = 8
for i in range(num_primary_sectors):
    t_start = (i / num_primary_sectors) * 2 * math.pi
    t_end = ((i + 1) / num_primary_sectors) * 2 * math.pi
    subdivide(50, MAX_RADIUS, t_start, t_end, 0)

# Final Overlay - A few high-precision circles for the "Swiss" hierarchy
ctx.set_source_rgba(0.92, 0.92, 0.95, 0.1)
ctx.set_line_width(1.5)
ctx.arc(CENTER_X, CENTER_Y, MAX_RADIUS * 1.05, 0, 2 * math.pi)
ctx.stroke()

ctx.set_line_width(0.5)
ctx.arc(CENTER_X, CENTER_Y, 40, 0, 2 * math.pi)
ctx.stroke()

# Add small technical label simulation (geometric blocks)
for i in range(3):
    ctx.set_source_rgba(*PALETTE[0])
    y_pos = height - 40 - (i * 10)
    ctx.rectangle(40, y_pos, 30, 2)
    ctx.fill()
    ctx.rectangle(75, y_pos, 10, 2)
    ctx.fill()

