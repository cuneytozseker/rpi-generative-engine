import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep charcoal for a technical feel
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
grid_steps_r = 14
grid_steps_theta = 48
max_radius = min(width, height) * 0.45
accent_color = (1.0, 0.2, 0.1)  # Swiss International Orange

def polar_to_cartesian(r, theta, distortion_factor=0):
    """Maps polar coordinates to Cartesian with a radial wave distortion."""
    # Radial distortion influenced by angle and distance
    # Creates a 'pulsing' grid effect
    r_distorted = r * (1 + distortion_factor * math.sin(theta * 6 + r * 0.02))
    x = center_x + r_distorted * math.cos(theta)
    y = center_y + r_distorted * math.sin(theta)
    return x, y

def draw_staccato_arc(r, theta_start, theta_end, segments=10):
    """Draws a dashed/fragmented arc to simulate technical 'bitmapped' grain."""
    step = (theta_end - theta_start) / segments
    for i in range(segments):
        if random.random() > 0.4:
            t1 = theta_start + i * step
            t2 = t1 + step * 0.7
            
            # Distortion varies by radius for 'liquid' grid feel
            dist = 0.12 * (r / max_radius)
            x1, y1 = polar_to_cartesian(r, t1, dist)
            x2, y2 = polar_to_cartesian(r, t2, dist)
            
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()

# 1. LAYER: SUBTLE UNDER-GRID (Mathematical Foundation)
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.4, 0.4, 0.4, 0.3)
for r_idx in range(1, grid_steps_r + 1):
    r = (r_idx / grid_steps_r) * max_radius
    ctx.arc(center_x, center_y, r, 0, 2 * math.pi)
    ctx.stroke()

# 2. LAYER: THE DISTORTED SWISS GRID
# Radial lines and Concentric Arcs transformed via polar logic
for i in range(grid_steps_theta):
    angle = (i / grid_steps_theta) * 2 * math.pi
    
    # Alternate weights for visual hierarchy
    if i % 4 == 0:
        ctx.set_line_width(0.8)
        ctx.set_source_rgba(0.9, 0.9, 0.9, 0.8)
    else:
        ctx.set_line_width(0.3)
        ctx.set_source_rgba(0.7, 0.7, 0.7, 0.5)
        
    # Draw radial segments with gaps (structural tension)
    for r_idx in range(grid_steps_r):
        r_inner = (r_idx / grid_steps_r) * max_radius
        r_outer = ((r_idx + 0.8) / grid_steps_r) * max_radius
        
        # Calculate distorted positions
        dist = 0.15 * (r_inner / max_radius)
        x1, y1 = polar_to_cartesian(r_inner, angle, dist)
        x2, y2 = polar_to_cartesian(r_outer, angle, dist)
        
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()

# 3. LAYER: RADIAL FRAGMENTS (Density Modulation)
ctx.set_line_width(0.5)
ctx.set_source_rgba(1, 1, 1, 0.6)
for r_idx in range(1, grid_steps_r):
    r = (r_idx / grid_steps_r) * max_radius
    # Increase segments as radius increases to maintain density
    segs = int(8 + r_idx * 4)
    draw_staccato_arc(r, 0, 2 * math.pi, segments=segs)

# 4. LAYER: INTERCONNECTIVITY NODES
# Connecting points between layers to create 'Vector-Field' tension
random.seed(42) # Deterministic randomness for layout
for _ in range(120):
    r_idx = random.randint(2, grid_steps_r - 1)
    t_idx = random.randint(0, grid_steps_theta - 1)
    
    r = (r_idx / grid_steps_r) * max_radius
    angle = (t_idx / grid_steps_theta) * 2 * math.pi
    
    # Target a nearby coordinate
    r2 = r + (max_radius / grid_steps_r)
    angle2 = angle + (2 * math.pi / grid_steps_theta) * (random.choice([-1, 1]))
    
    dist_val = 0.15 * (r / max_radius)
    x1, y1 = polar_to_cartesian(r, angle, dist_val)
    x2, y2 = polar_to_cartesian(r2, angle2, dist_val)
    
    # Accent color sporadically
    if random.random() > 0.85:
        ctx.set_source_rgba(*accent_color, 0.8)
        ctx.set_line_width(1.2)
        # Add small 'technical' square at node
        ctx.rectangle(x1-1.5, y1-1.5, 3, 3)
        ctx.fill()
    else:
        ctx.set_source_rgba(0.8, 0.8, 1.0, 0.4)
        ctx.set_line_width(0.4)
    
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 5. LAYER: "STACCATO" DATA BLOCKS (Typography-as-Texture)
# Simulating the aesthetic of data readouts or Swiss Swiss precision markings
for i in range(12):
    angle = (i / 12) * 2 * math.pi + 0.1
    r = max_radius * 1.05
    x, y = polar_to_cartesian(r, angle, 0.05)
    
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle + math.pi/2)
    
    # Draw tiny vertical bars representing "bitmapped" logic
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    for b in range(5):
        h = random.uniform(2, 10)
        ctx.rectangle(b * 3, 0, 1.5, h)
        ctx.fill()
    ctx.restore()

# Final focal ring
ctx.set_line_width(0.3)
ctx.set_source_rgba(1, 1, 1, 0.2)
ctx.arc(center_x, center_y, max_radius * 1.1, 0, 2 * math.pi)
ctx.stroke()

