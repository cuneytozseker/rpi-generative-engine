import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep "Terminal" Black/Navy
ctx.set_source_rgb(0.02, 0.02, 0.04)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
max_radius = min(width, height) * 0.45
rings = 18
slices = 36
accent_color = (1.0, 0.22, 0.1)  # International Orange (Swiss Accent)
blueprint_color = (0.3, 0.4, 0.6, 0.5) # Muted blueprint blue/gray

def polar_to_cartesian(r, theta):
    return center_x + r * math.cos(theta), center_y + r * math.sin(theta)

# 1. STRUCTURAL SCAFFOLDING (Radial Grid)
# Non-linear grid subdivision: tightening exponentially toward the center
ctx.set_line_cap(cairo.LINE_CAP_BUTT)
for i in range(1, rings + 1):
    # Centripetal density logic: r approaches 0 faster as i decreases
    norm = i / rings
    r = max_radius * math.pow(norm, 1.4) 
    
    # Visual weight hierarchy
    is_major = i % 6 == 0
    ctx.set_line_width(0.8 if is_major else 0.3)
    ctx.set_source_rgba(*blueprint_color)
    
    ctx.arc(center_x, center_y, r, 0, 2 * math.pi)
    ctx.stroke()
    
    # Add metadata markers (Swiss-style numeric indicators)
    if is_major:
        ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(6)
        ctx.move_to(center_x + r + 2, center_y - 2)
        ctx.show_text(f"{int(r)} UNITS")

# 2. STACCATO ANGULAR PATHS
# Stochastic flow fields mapped onto polar coordinates
for s in range(slices):
    base_angle = (s / slices) * 2 * math.pi
    
    # Vary the "flow" based on angle to create organic entropy
    distortion = math.sin(base_angle * 3) * 0.15
    
    ctx.set_source_rgba(0.8, 0.8, 0.9, 0.6)
    ctx.set_line_width(0.5)
    
    current_r = 10 # Start slightly away from dead center
    while current_r < max_radius * 1.2:
        # Step size increases as we move out (expansive negative space)
        step = random.uniform(5, 15) * (current_r / 100 + 1)
        
        # Calculate segmented line
        x1, y1 = polar_to_cartesian(current_r, base_angle + distortion)
        current_r += step
        x2, y2 = polar_to_cartesian(current_r, base_angle + distortion)
        
        # Randomly skip segments to create "staccato" texture
        if random.random() > 0.3:
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()
            
            # Add "active data" nodes at ends of some segments
            if random.random() > 0.92:
                ctx.set_source_rgb(*accent_color)
                ctx.rectangle(x2-1.5, y2-1.5, 3, 3)
                ctx.fill()
                ctx.set_source_rgba(0.8, 0.8, 0.9, 0.6)

# 3. CONVERGENT NODES (Data Clustering)
# High-frequency clustering at specific intersections
for _ in range(120):
    # Bias selection toward center
    r_bias = max_radius * math.pow(random.random(), 2)
    angle_bias = random.randint(0, slices) * (2 * math.pi / slices)
    
    px, py = polar_to_cartesian(r_bias, angle_bias)
    
    # Draw tiny technical crosses
    ctx.set_source_rgba(1, 1, 1, 0.4)
    ctx.set_line_width(0.2)
    ctx.move_to(px - 3, py)
    ctx.line_to(px + 3, py)
    ctx.move_to(px, py - 3)
    ctx.line_to(px, py + 3)
    ctx.stroke()

# 4. TYPOGRAPHIC OVERLAY (Non-functional Texture)
# Using coordinate data as a rhythmic texture layer
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_font_size(7)
for i in range(5):
    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(max_radius * 0.8, max_radius * 1.1)
    tx, ty = polar_to_cartesian(dist, angle)
    
    ctx.save()
    ctx.translate(tx, ty)
    ctx.rotate(angle + math.pi/2)
    ctx.move_to(0, 0)
    ctx.show_text(f"SYS_REF: {hex(int(dist*1000))}")
    ctx.restore()

# 5. FINAL ACCENT: CENTRAL CORE
# The "Convergent System" focal point
ctx.set_source_rgb(*accent_color)
ctx.set_line_width(2.0)
ctx.arc(center_x, center_y, 4, 0, 2 * math.pi)
ctx.stroke()

ctx.set_line_width(0.5)
ctx.arc(center_x, center_y, 8, 0, 2 * math.pi)
ctx.stroke()

# Framing: Technical borders
ctx.set_source_rgba(1, 1, 1, 0.2)
ctx.set_line_width(1)
ctx.rectangle(20, 20, width - 40, height - 40)
ctx.stroke()

# Small corner identification block
ctx.rectangle(width - 80, height - 40, 60, 20)
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.fill()
