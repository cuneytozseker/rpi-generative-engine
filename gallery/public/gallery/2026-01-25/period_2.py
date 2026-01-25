import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

# Constants
center_x, center_y = width // 2, height // 2
max_radius = min(width, height) * 0.45
num_rings = 40
num_sectors = 64

def polar_to_cartesian(r, theta):
    """Converts polar coordinates to cartesian with a slight radial distortion."""
    # Apply a non-linear radial compression to create variable density
    # This simulates the "localized compression" requested in the brief
    r_distorted = r * (1 + 0.15 * math.sin(r * 0.05)) 
    x = center_x + r_distorted * math.cos(theta)
    y = center_y + r_distorted * math.sin(theta)
    return x, y

# 1. THE SYSTEMATIC GRID: Polar Swiss Transformation
# Creating the "hairline vector precision" layer
ctx.set_line_width(0.3)
for i in range(num_rings):
    # Ring density follows a power law for hierarchy
    r = (i / num_rings) ** 1.2 * max_radius
    
    # Calculate opacity based on radius to create depth
    alpha = 0.1 + (i / num_rings) * 0.4
    ctx.set_source_rgba(0.8, 0.9, 1.0, alpha)
    
    # Draw arcs (Rings)
    ctx.arc(center_x, center_y, r, 0, 2 * math.pi)
    ctx.stroke()

for j in range(num_sectors):
    theta = (j / num_sectors) * 2 * math.pi
    
    # Varying line lengths for rhythmic variation
    length_mod = 1.0 if j % 4 == 0 else 0.7
    if j % 16 == 0: length_mod = 1.1
    
    p1 = polar_to_cartesian(10, theta)
    p2 = polar_to_cartesian(max_radius * length_mod, theta)
    
    ctx.set_source_rgba(0.7, 0.8, 1.0, 0.2)
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.stroke()

# 2. VARIABLE-DENSITY PARTITIONING (Recursive Logic)
# Subdividing specific sectors to create focal points
random.seed(42) # Deterministic randomness for systematic feel
for _ in range(12):
    angle_start = random.randint(0, num_sectors) * (2 * math.pi / num_sectors)
    angle_sweep = (random.randint(1, 4)) * (2 * math.pi / num_sectors)
    r_start = random.uniform(0.3, 0.8) * max_radius
    r_end = r_start + random.uniform(20, 60)
    
    # Draw a "Technical Block" (Spectral Accent)
    ctx.set_source_rgba(0.0, 0.6, 1.0, 0.15) # Cyan glow
    ctx.arc(center_x, center_y, r_start, angle_start, angle_start + angle_sweep)
    ctx.arc_negative(center_x, center_y, r_end, angle_start + angle_sweep, angle_start)
    ctx.fill()
    
    # Outline of the block
    ctx.set_source_rgba(0.4, 0.8, 1.0, 0.8)
    ctx.set_line_width(0.5)
    ctx.arc(center_x, center_y, r_start, angle_start, angle_start + angle_sweep)
    ctx.stroke()
    ctx.arc(center_x, center_y, r_end, angle_start, angle_start + angle_sweep)
    ctx.stroke()

# 3. STOCHASTIC NODE-LINK STRUCTURES
# Connecting intersections to simulate a cosmic/data map
nodes = []
for _ in range(80):
    r_idx = random.randint(10, num_rings-1)
    s_idx = random.randint(0, num_sectors-1)
    r = (r_idx / num_rings) ** 1.2 * max_radius
    theta = (s_idx / num_sectors) * 2 * math.pi
    nodes.append(polar_to_cartesian(r, theta))

ctx.set_line_width(0.2)
for i, p1 in enumerate(nodes):
    # Connect nodes that are spatially close
    for p2 in nodes[i+1:]:
        dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        if dist < 45:
            ctx.set_source_rgba(1, 1, 1, 0.15)
            ctx.move_to(*p1)
            ctx.line_to(*p2)
            ctx.stroke()
            
    # Draw "Geometric Events" (Nodes)
    if random.random() > 0.7:
        ctx.set_source_rgba(1, 0.3, 0.4, 0.8) # Magenta accent
        ctx.arc(p1[0], p1[1], 1.5, 0, 2*math.pi)
        ctx.fill()
    else:
        ctx.set_source_rgba(1, 1, 1, 0.6)
        ctx.rectangle(p1[0]-1, p1[1]-1, 2, 2)
        ctx.fill()

# 4. OPTICAL DIFFUSION (Glow effect)
# Create a soft central radial gradient to simulate "electronic glow"
grad = cairo.RadialGradient(center_x, center_y, 0, center_x, center_y, max_radius * 1.2)
grad.add_color_stop_rgba(0, 0.1, 0.3, 0.5, 0.15)
grad.add_color_stop_rgba(1, 0, 0, 0, 0)
ctx.set_source(grad)
ctx.arc(center_x, center_y, max_radius * 1.2, 0, 2*math.pi)
ctx.fill()

# 5. ANNOTATIONS (Simulated Technical Typography)
# Small rhythmic markers to suggest data-driven warmth
ctx.set_source_rgba(0.9, 0.9, 1.0, 0.4)
for i in range(5):
    r = (i+1) * 0.2 * max_radius
    for a in [0, math.pi/2, math.pi, 3*math.pi/2]:
        px, py = polar_to_cartesian(r + 5, a + 0.05)
        ctx.rectangle(px, py, 8, 1) # Tiny dashes like text
        ctx.fill()

# Final hairline border for Swiss precision
ctx.set_line_width(0.5)
ctx.set_source_rgba(1, 1, 1, 0.2)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()

