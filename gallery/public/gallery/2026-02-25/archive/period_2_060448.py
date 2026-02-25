import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Midnight Blue
ctx.set_source_rgb(0.02, 0.05, 0.12)
ctx.paint()

# Configuration
center_x, center_y = width // 2, height // 2
num_rings = 18
num_spokes = 36
base_radius = 20

def to_cartesian(r, theta):
    """Converts polar coordinates to screen space with a radial distortion."""
    # Radial distortion: apply a sine-wave displacement based on angle
    # to create a 'harmonic' wobble characteristic of analytical maps
    distortion = 12 * math.sin(theta * 5) * (r / 200)
    r_distorted = r + distortion
    x = center_x + r_distorted * math.cos(theta)
    y = center_y + r_distorted * math.sin(theta)
    return x, y

# 1. DRAW RADIAL SYSTEM (The Polar Grid)
ctx.set_line_width(0.5)
for i in range(num_rings):
    # Non-linear spacing: logarithmic expansion to suggest perspective/depth
    r = base_radius + math.pow(i, 1.8) * 6
    
    # Draw segments of the rings to create "discrete logic" gaps
    ctx.set_source_rgba(0.9, 0.95, 1.0, 0.3)
    segments = 12
    for s in range(segments):
        start_angle = (s * 2 * math.pi / segments)
        end_angle = start_angle + (math.pi / 8) # Gaps between segments
        
        ctx.new_path()
        # Draw arcs manually using the distortion function for precision
        steps = 20
        for step in range(steps + 1):
            theta = start_angle + (end_angle - start_angle) * (step / steps)
            px, py = to_cartesian(r, theta)
            if step == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        ctx.stroke()

# 2. DRAW DATA SPOKES
for j in range(num_spokes):
    theta = j * (2 * math.pi / num_spokes)
    
    # Vary line length and weight based on quadrant (dynamic asymmetry)
    max_r = 240 + 30 * math.sin(theta * 2)
    start_r = 30 + 10 * math.cos(theta * 4)
    
    ctx.set_line_width(0.3 if j % 2 == 0 else 0.8)
    ctx.set_source_rgba(0.7, 0.9, 1.0, 0.5)
    
    x1, y1 = to_cartesian(start_r, theta)
    x2, y2 = to_cartesian(max_r, theta)
    
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 3. NODAL HIERARCHY & CROSS-CONNECTORS
# Drawing connections between disparate points in the coordinate system
random.seed(42) # Deterministic randomness for systematic feel
for _ in range(15):
    r1 = random.uniform(50, 200)
    theta1 = random.uniform(0, 2 * math.pi)
    r2 = random.uniform(50, 200)
    theta2 = theta1 + random.uniform(-math.pi/3, math.pi/3)
    
    x1, y1 = to_cartesian(r1, theta1)
    x2, y2 = to_cartesian(r2, theta2)
    
    # Thin vector paths
    ctx.set_source_rgba(1.0, 1.0, 1.0, 0.15)
    ctx.set_line_width(0.4)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()
    
    # Small bitmapped-style nodes at endpoints
    ctx.set_source_rgba(1.0, 1.0, 1.0, 0.8)
    ctx.rectangle(x1-1, y1-1, 2, 2)
    ctx.fill()

# 4. ALGORITHMIC HALFTONING (The Information Clusters)
# Distribute small geometric primitives based on a "value map"
for i in range(num_rings):
    r = base_radius + math.pow(i, 1.8) * 6
    for j in range(num_spokes * 2):
        theta = j * (math.pi / num_spokes)
        
        # Scalar field logic: determine density via trigonometric interaction
        density_threshold = math.sin(theta * 3) * math.cos(r * 0.02)
        
        if density_threshold > 0.4:
            px, py = to_cartesian(r, theta)
            
            ctx.set_source_rgba(0.0, 0.8, 1.0, 0.7)
            # Draw tiny crosses (Swiss influence)
            size = 2
            ctx.move_to(px - size, py)
            ctx.line_to(px + size, py)
            ctx.move_to(px, py - size)
            ctx.line_to(px, py + size)
            ctx.set_line_width(0.5)
            ctx.stroke()
        
        elif density_threshold < -0.6:
            # Discrete logic blocks
            px, py = to_cartesian(r, theta)
            ctx.set_source_rgba(1.0, 1.0, 1.0, 0.9)
            ctx.rectangle(px - 1, py - 3, 2, 6) # Vertical tick marks
            ctx.fill()

# 5. OVERLAY TEXTURE / MARGINALIA
# Adding precise small-scale details to simulate a blueprint
ctx.set_source_rgba(1.0, 1.0, 1.0, 0.4)
ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(8)

for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
    tx, ty = to_cartesian(260, angle)
    ctx.move_to(tx, ty)
    # Mock-analytical coordinates
    ctx.show_text(f"RAD_{int(angle*180/math.pi)} // SYS.LOG")

# Final framing line
ctx.set_line_width(1.0)
ctx.set_source_rgba(1.0, 1.0, 1.0, 0.1)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()
