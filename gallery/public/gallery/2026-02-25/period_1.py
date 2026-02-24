import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: The "Deep Void"
ctx.set_source_rgb(0.02, 0.02, 0.03) 
ctx.paint()

# Configuration
center_x, center_y = width // 2, height // 2
num_rings = 45
max_radius = min(width, height) * 0.48
phi = (1 + math.sqrt(5)) / 2  # Golden ratio for harmonic spacing

def to_cartesian(r, theta):
    return center_x + r * math.cos(theta), center_y + r * math.sin(theta)

# System Logic: Polar Transformation of a Swiss Grid
# We use a non-linear radial distribution (logarithmic growth) to create depth
# and a variable angular subdivision to simulate systematic distortion.

for i in range(1, num_rings):
    # Radial scaling: Exponential growth creates the "Void" expansion effect
    r_norm = i / num_rings
    r = math.pow(r_norm, 1.5) * max_radius
    
    # Mathematical distortion factor based on radius
    distortion = math.sin(r * 0.05) * 0.15
    
    # Grid density: Increases as we move outward, following a modulated pattern
    segments = int(12 + (i * 1.5))
    
    # Storage for node coordinates to draw connectivity vectors
    nodes = []
    
    for j in range(segments):
        # Base angle plus a radial-dependent shift (The "Spiral Twist")
        angle = (j / segments) * 2 * math.pi + (i * 0.02)
        
        # Apply non-linear "radial distortion" to the angle
        angle += distortion
        
        x, y = to_cartesian(r, angle)
        nodes.append((x, y))

    # --- DRAWING LAYER 1: Relational Vectors (The Blueprint) ---
    ctx.set_line_width(0.3)
    ctx.set_source_rgba(0.8, 0.8, 0.9, 0.25) # Ghostly white
    
    for k in range(len(nodes)):
        p1 = nodes[k]
        p2 = nodes[(k + 1) % len(nodes)]
        
        ctx.move_to(p1[0], p1[1])
        ctx.line_to(p2[0], p2[1])
        ctx.stroke()
        
        # Cross-ring connectivity (Relational node-based connectivity)
        if i > 1:
            # Connect to a subset of nodes in the previous ring to create a web
            prev_angle = (k / segments) * 2 * math.pi + ((i-1) * 0.02) + (math.sin((i-1) * 0.05) * 0.15)
            px, py = to_cartesian(math.pow((i-1)/num_rings, 1.5) * max_radius, prev_angle)
            
            ctx.set_source_rgba(0.5, 0.6, 1.0, 0.15)
            ctx.move_to(p1[0], p1[1])
            ctx.line_to(px, py)
            ctx.stroke()

    # --- DRAWING LAYER 2: Functional Accents (Data States) ---
    # We highlight specific intersections using a systematic modulus
    if i % 3 == 0:
        ctx.set_source_rgba(1.0, 0.3, 0.1, 0.8) # Saturated "Alert" Orange
        for k in range(0, len(nodes), 4):
            x, y = nodes[k]
            # Draw a precision marker
            marker_size = 1.5
            ctx.arc(x, y, marker_size, 0, 2 * math.pi)
            ctx.fill()
            
            # Subtle radial line pointing towards the void center
            ctx.set_line_width(0.2)
            ctx.move_to(x, y)
            ctx.line_to(center_x + (x-center_x)*0.95, center_y + (y-center_y)*0.95)
            ctx.stroke()

# --- DRAWING LAYER 3: Structural Framework ---
# Draw primary axes to reinforce the Swiss design principle
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
    ctx.move_to(center_x, center_y)
    tx, ty = to_cartesian(max_radius * 1.1, angle)
    ctx.line_to(tx, ty)
    ctx.stroke()

# Add a subtle "Scale" indicator in the corner (Brutalist metadata)
ctx.set_source_rgba(0.9, 0.9, 0.9, 0.6)
ctx.rectangle(40, height - 60, 100, 1) # Horizontal rule
ctx.fill()
for m in range(5):
    ctx.rectangle(40 + (m * 25), height - 65, 1, 5)
    ctx.fill()

# Final focal point: The "Void" core
ctx.set_source_rgba(0.1, 0.4, 1.0, 0.05)
for r_glow in range(1, 20):
    ctx.arc(center_x, center_y, r_glow * 3, 0, 2 * math.pi)
    ctx.fill()

