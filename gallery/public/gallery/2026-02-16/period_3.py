import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep matte charcoal
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_distorted_arc(cx, cy, r, start_angle, end_angle, segments=50, noise_factor=5.0):
    """Draws an arc with radial distortion based on its angular position."""
    ctx.move_to(*polar_to_cartesian(cx, cy, r + math.sin(start_angle * 5) * noise_factor, start_angle))
    for i in range(1, segments + 1):
        angle = start_angle + (end_angle - start_angle) * (i / segments)
        # Radial distortion: modulation of radius via sine waves to create 'organic tension'
        distorted_r = r + (math.sin(angle * 8) * math.cos(r * 0.02) * noise_factor)
        ctx.line_to(*polar_to_cartesian(cx, cy, distorted_r, angle))

def draw_technical_marker(x, y, size=3):
    """Swiss-style crosshair marker."""
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

# Configuration
center_x, center_y = width // 2, height // 2
num_rings = 18
num_spokes = 32
max_radius = min(width, height) * 0.45

# --- Layer 1: Atmospheric Flow (The 'Glow') ---
for r_idx in range(num_rings):
    r = (r_idx / num_rings) * max_radius
    alpha = 0.05 + (r_idx / num_rings) * 0.1
    ctx.set_source_rgba(0.4, 0.6, 1.0, alpha)
    ctx.set_line_width(2.5)
    
    # Fragmented distorted rings
    for i in range(4):
        start = (i * math.pi / 2) + (r_idx * 0.1)
        draw_distorted_arc(center_x, center_y, r, start, start + math.pi/3, noise_factor=12.0)
        ctx.stroke()

# --- Layer 2: The Core Swiss Polar Grid ---
ctx.set_line_width(0.3)
for i in range(num_spokes):
    angle = (i / num_spokes) * 2 * math.pi
    
    # Luminous technical lines
    if i % 4 == 0:
        ctx.set_source_rgba(0.9, 0.9, 1.0, 0.4)
        ctx.set_dash([10, 5])
    else:
        ctx.set_source_rgba(0.5, 0.5, 0.6, 0.2)
        ctx.set_dash([])
        
    p1 = polar_to_cartesian(center_x, center_y, 20, angle)
    # Distortion applied to radial lines
    distort_r = max_radius + math.sin(angle * 10) * 15
    p2 = polar_to_cartesian(center_x, center_y, distort_r, angle)
    
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.stroke()

# --- Layer 3: Recursive Subdivision Nodes ---
ctx.set_dash([])
for r_idx in [4, 8, 12, 16]:
    r = (r_idx / num_rings) * max_radius
    for s_idx in range(num_spokes):
        if (s_idx + r_idx) % 7 == 0:
            angle = (s_idx / num_spokes) * 2 * math.pi
            # Apply same distortion logic for node placement
            distorted_r = r + (math.sin(angle * 8) * math.cos(r * 0.02) * 5.0)
            x, y = polar_to_cartesian(center_x, center_y, distorted_r, angle)
            
            # Primary node
            ctx.set_source_rgba(1, 1, 1, 0.8)
            ctx.set_line_width(0.5)
            draw_technical_marker(x, y, 4)
            
            # Secondary offset markers (simulating data jitter)
            ctx.set_source_rgba(0, 0.8, 1, 0.4)
            ctx.arc(x + 5, y - 5, 1.5, 0, 2 * math.pi)
            ctx.fill()
            
            # Small "blueprint" line connecting nodes
            next_angle = ((s_idx + 1) / num_spokes) * 2 * math.pi
            nx, ny = polar_to_cartesian(center_x, center_y, distorted_r, next_angle)
            ctx.set_source_rgba(1, 1, 1, 0.1)
            ctx.move_to(x, y)
            ctx.line_to(nx, ny)
            ctx.stroke()

# --- Layer 4: Sharp High-Precision Overlays ---
ctx.set_line_width(0.7)
ctx.set_source_rgba(1.0, 1.0, 1.0, 0.9)
for r_factor in [0.3, 0.6, 0.95]:
    r = r_factor * max_radius
    # Broken precision rings
    for segment in range(12):
        start = (segment / 12) * 2 * math.pi
        if segment % 3 != 0:
            draw_distorted_arc(center_x, center_y, r, start, start + 0.15, noise_factor=2.0)
            ctx.stroke()

# --- Layer 5: Data Pulse (Visual Rhythm) ---
random.seed(42)
for _ in range(25):
    angle = random.uniform(0, 2 * math.pi)
    r_start = random.uniform(20, max_radius * 0.8)
    length = random.uniform(20, 60)
    
    ctx.set_line_width(random.uniform(0.1, 1.2))
    # Pulse colors: Spectral highlight
    ctx.set_source_rgba(0.8, 0.9, 1.0, random.uniform(0.3, 0.7))
    
    p1 = polar_to_cartesian(center_x, center_y, r_start, angle)
    p2 = polar_to_cartesian(center_x, center_y, r_start + length, angle)
    
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.stroke()
    
    # Tiny dot at end of pulse
    ctx.arc(p2[0], p2[1], 1, 0, 2 * math.pi)
    ctx.fill()

# Final Polish: Central Data Hub
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.arc(center_x, center_y, 15, 0, 2 * math.pi)
ctx.stroke()
ctx.set_source_rgba(0, 0.6, 1, 0.6)
ctx.arc(center_x, center_y, 2, 0, 2 * math.pi)
ctx.fill()

# Signature Swiss Detail: Border labels
ctx.set_source_rgba(1, 1, 1, 0.3)
ctx.set_line_width(0.5)
ctx.move_to(20, 20)
ctx.line_to(40, 20)
ctx.move_to(20, 20)
ctx.line_to(20, 40)
ctx.stroke()

