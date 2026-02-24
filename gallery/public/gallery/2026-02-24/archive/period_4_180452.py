import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
rings = 18
segments = 60
phi = (1 + 5**0.5) / 2  # Golden ratio for proportional spacing

def polar_to_cartesian(r, theta, distortion_factor=0.0):
    """Converts polar to cartesian with a non-linear radial distortion."""
    # Apply a wave-based distortion to the radius based on angle
    r_distorted = r + (math.sin(theta * 5 + r * 0.02) * distortion_factor)
    x = center_x + r_distorted * math.cos(theta)
    y = center_y + r_distorted * math.sin(theta)
    return x, y

# --- LAYER 1: The Atmospheric Foundation (Faint Vector Field) ---
ctx.set_line_width(0.5)
for i in range(100):
    r_start = random.uniform(50, 400)
    theta = random.uniform(0, 2 * math.pi)
    length = random.uniform(20, 100)
    
    x1, y1 = polar_to_cartesian(r_start, theta, 15)
    x2, y2 = polar_to_cartesian(r_start + length, theta + 0.1, 15)
    
    ctx.set_source_rgba(0.4, 0.4, 0.5, 0.15)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# --- LAYER 2: The Swiss Polar Grid (Structural Order) ---
# This system uses modulated line weights and "broken" segments to create rhythm
for r_idx in range(1, rings):
    radius = r_idx * 22
    # Vary intensity based on distance (Atmospheric gradient)
    alpha = max(0.1, 1.0 - (radius / 400))
    
    # Draw Ring Segments
    ctx.set_line_width(1.5 if r_idx % 3 == 0 else 0.5)
    
    step = (2 * math.pi) / segments
    for s in range(segments):
        # Systematic gaps (Swiss spacing)
        if (s + r_idx) % 7 == 0:
            continue
            
        theta1 = s * step
        theta2 = (s + 0.8) * step
        
        # Distortion intensity increases with radius
        distort = radius * 0.12
        
        x1, y1 = polar_to_cartesian(radius, theta1, distort)
        x2, y2 = polar_to_cartesian(radius, theta2, distort)
        
        # Color mapping: Neutral field with high-chroma pulses
        if random.random() > 0.96:
            ctx.set_source_rgba(1.0, 0.2, 0.3, 0.9) # Vibrant Pulse (High Chroma)
            ctx.set_line_width(3.0)
        else:
            ctx.set_source_rgba(0.9, 0.9, 0.9, alpha * 0.6) # Neutral
            ctx.set_line_width(0.8)
            
        ctx.move_to(x1, y1)
        # Approximate arc with line for distortion effect
        ctx.line_to(x2, y2)
        ctx.stroke()

# --- LAYER 3: Recursive Data Markers (Geometric Logic) ---
# Placing "Brutalist" blocks at specific harmonic intersections
for r_idx in [4, 8, 12, 16]:
    radius = r_idx * 22
    angle_step = (2 * math.pi) / 8
    
    for a in range(8):
        theta = a * angle_step + (r_idx * 0.1)
        distort = radius * 0.12
        px, py = polar_to_cartesian(radius, theta, distort)
        
        # Swiss Hierarchy: High contrast rectangular markers
        ctx.save()
        ctx.translate(px, py)
        ctx.rotate(theta + math.pi/2)
        
        # High-chroma spectral highlight
        ctx.set_source_rgba(0.0, 0.8, 1.0, 0.8) 
        ctx.rectangle(-2, -10, 4, 20)
        ctx.fill()
        
        # Offset white marker
        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.rectangle(4, -5, 2, 10)
        ctx.fill()
        ctx.restore()

# --- LAYER 4: The Radial Expansion (Kinetic Energy) ---
# Long, sweeping rays that follow the distorted field
ctx.set_line_width(0.3)
for i in range(40):
    theta = (i / 40.0) * 2 * math.pi
    distort = 40.0
    
    # Creating a "motion blur" or "atmospheric noise" effect
    for iteration in range(5):
        alpha = 0.05 / (iteration + 1)
        ctx.set_source_rgba(0.8, 0.9, 1.0, alpha)
        
        ctx.move_to(center_x, center_y)
        for r_step in range(0, 450, 10):
            # The distortion evolves as it travels outward
            tx, ty = polar_to_cartesian(r_step, theta + (iteration * 0.005), distort * (r_step/100))
            ctx.line_to(tx, ty)
        ctx.stroke()

# Final Polish: Central Core (The "Source")
ctx.set_source_rgb(1, 1, 1)
ctx.arc(center_x, center_y, 3, 0, 2 * math.pi)
ctx.fill()

ctx.set_source_rgba(1, 1, 1, 0.2)
ctx.set_line_width(1)
ctx.arc(center_x, center_y, 15, 0, 2 * math.pi)
ctx.stroke()

