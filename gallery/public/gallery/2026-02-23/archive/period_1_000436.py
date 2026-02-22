import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Minimalist Cream/Off-white
ctx.set_source_rgb(0.96, 0.96, 0.94)
ctx.paint()

# Configuration
center_x, center_y = width // 2, height // 2
max_radius = math.sqrt(center_x**2 + center_y**2)
rings = 14
slices = 36
entropy_factor = 0.15 # Controls the "glitch" intensity

def polar_to_cartesian(r, theta, offset_x=0, offset_y=0):
    """Converts polar coordinates to cartesian with an optional distortion offset."""
    x = center_x + r * math.cos(theta) + offset_x
    y = center_y + r * math.sin(theta) + offset_y
    return x, y

def draw_technical_mark(x, y, size=2):
    """Draws a small cross-hair or pixel-like anchor."""
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

# 1. THE UNDERLYING GRID (Structural Rigidity)
# We draw the radial skeleton with very thin, precise lines
ctx.set_source_rgb(0.1, 0.1, 0.1)
ctx.set_line_width(0.4)

for i in range(rings):
    r = (i + 1) * (max_radius / rings) * 0.8
    # Concentric circles with interruptions
    for s in range(slices):
        if random.random() > 0.2: # Stochastic gaps
            angle_start = (s / slices) * 2 * math.pi
            angle_end = ((s + 0.8) / slices) * 2 * math.pi
            ctx.arc(center_x, center_y, r, angle_start, angle_end)
            ctx.stroke()

# 2. POLAR RECURSION & DATA FIELDS (Systematic Disruption)
# Subdividing grid cells based on distance from center
for i in range(rings):
    r_inner = i * (max_radius / rings) * 0.8
    r_outer = (i + 1) * (max_radius / rings) * 0.8
    
    # Increase complexity as we move outward
    current_slices = slices if i < rings // 2 else slices * 2
    
    for s in range(current_slices):
        angle = (s / current_slices) * 2 * math.pi
        
        # Stochastic decision: what to draw in this "cell"?
        seed = random.random()
        
        # Apply radial distortion (Entropy)
        distort_r = math.sin(angle * 4) * (i * 2.5) * entropy_factor
        distort_angle = math.cos(r_inner * 0.05) * entropy_factor * 0.2
        
        p1_r, p1_a = r_inner, angle + distort_angle
        p2_r, p2_a = r_outer, angle + distort_angle
        
        x1, y1 = polar_to_cartesian(p1_r, p1_a, distort_r, distort_r)
        x2, y2 = polar_to_cartesian(p2_r, p2_a, distort_r, distort_r)

        if seed < 0.15:
            # Type A: Solid Data Block (Binary Contrast)
            ctx.set_line_width(1.5)
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()
            
        elif seed < 0.30:
            # Type B: Dithered texture (Nodes)
            ctx.set_source_rgb(0.1, 0.1, 0.1)
            draw_technical_mark(x1, y1, size=1.5)
            
        elif seed < 0.40 and i % 2 == 0:
            # Type C: Recursive Arc Segment
            ctx.set_line_width(0.6)
            ctx.arc(center_x, center_y, r_inner + (r_outer-r_inner)/2, p1_a, p1_a + 0.1)
            ctx.stroke()

# 3. OVERLAY NODES & CONNECTORS (Node-Link Structure)
# Draw "signal lines" that cut across the grid
ctx.set_source_rgb(0, 0.2, 0.8) # Electric Blue highlight
ctx.set_line_width(0.8)
for _ in range(8):
    path_points = []
    r_step = max_radius / 10
    start_angle = random.uniform(0, 2 * math.pi)
    
    for j in range(6):
        curr_r = j * r_step + random.uniform(-20, 20)
        curr_a = start_angle + (j * 0.15)
        px, py = polar_to_cartesian(curr_r, curr_a)
        path_points.append((px, py))
        
    # Draw path
    ctx.move_to(path_points[0][0], path_points[0][1])
    for px, py in path_points[1:]:
        ctx.line_to(px, py)
    ctx.stroke()
    
    # Add labels/bits at ends
    last_x, last_y = path_points[-1]
    ctx.rectangle(last_x - 3, last_y - 3, 6, 6)
    ctx.fill()

# 4. MARGINALIA & METADATA (Swiss Hierarchy)
# Small blocks of "code" or "data" to anchor the composition
ctx.set_source_rgb(0.1, 0.1, 0.1)
for i in range(5):
    y_pos = height - 40 - (i * 8)
    ctx.rectangle(40, y_pos, random.randint(10, 40), 4)
    ctx.fill()

# Final focal point: The decentralized core
ctx.set_source_rgb(0.96, 0.96, 0.94) # Background color to "punch out"
ctx.arc(center_x, center_y, 40, 0, 2 * math.pi)
ctx.fill()
ctx.set_source_rgb(0.1, 0.1, 0.1)
ctx.set_line_width(1)
ctx.arc(center_x, center_y, 40, 0, 2 * math.pi)
ctx.stroke()

# Internal "glitch" in the core
ctx.set_line_width(0.5)
for i in range(4):
    ctx.move_to(center_x - 20, center_y - 15 + (i*10))
    ctx.line_to(center_x + 20, center_y - 15 + (i*10))
    ctx.stroke()

