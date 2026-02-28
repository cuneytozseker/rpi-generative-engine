import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Constants for the Polar Grid
CENTER_X, CENTER_Y = width // 2, height // 2
RINGS = 18
SEGMENTS = 42
MAX_RADIUS = min(width, height) * 0.45

def get_polar_coords(r, theta, distortion_scale=1.0):
    """Calculates distorted polar coordinates for a more organic, fluid movement."""
    # Create a flow field effect using harmonic sines
    noise = math.sin(r * 0.02 - theta * 2.0) * 15.0 * distortion_scale
    noise += math.cos(theta * 5.0 + r * 0.01) * 10.0 * distortion_scale
    
    distorted_r = r + noise
    x = CENTER_X + distorted_r * math.cos(theta)
    y = CENTER_Y + distorted_r * math.sin(theta)
    return x, y

def draw_module(r1, r2, t1, t2, color, weight, subdivision=1):
    """Draws a 'bit-mapped' geometric module within a polar segment."""
    if subdivision > 1 and random.random() > 0.4:
        # Recursive subdivision into smaller blocks
        mid_r = (r1 + r2) / 2
        mid_t = (t1 + t2) / 2
        draw_module(r1, mid_r, t1, mid_t, color, weight, subdivision - 1)
        draw_module(mid_r, r2, mid_t, t2, color, weight, subdivision - 1)
    else:
        # Draw the primitive
        ctx.set_source_rgba(*color)
        ctx.set_line_width(weight)
        
        # Calculate 4 corners of the quad
        p1 = get_polar_coords(r1, t1)
        p2 = get_polar_coords(r2, t1)
        p3 = get_polar_coords(r2, t2)
        p4 = get_polar_coords(r1, t2)
        
        ctx.move_to(*p1)
        ctx.line_to(*p2)
        ctx.line_to(*p3)
        ctx.line_to(*p4)
        ctx.close_path()
        
        # Density as value: alternating fill and stroke
        if random.random() > 0.7:
            ctx.fill()
        else:
            ctx.stroke()

# Functional Chromatic Hierarchy
SWISS_RED = (0.89, 0.12, 0.09, 0.9)
WHITE = (0.95, 0.95, 0.95, 0.8)
GREY = (0.4, 0.4, 0.45, 0.5)

# Layer 1: The Underlying Grid Structure (Subtle)
ctx.set_line_width(0.3)
ctx.set_source_rgba(0.2, 0.2, 0.3, 0.3)
for r_idx in range(RINGS):
    r = (r_idx / RINGS) * MAX_RADIUS
    for s_idx in range(SEGMENTS):
        t = (s_idx / SEGMENTS) * (2 * math.pi)
        p = get_polar_coords(r, t, distortion_scale=0.5)
        if s_idx == 0:
            ctx.move_to(*p)
        else:
            ctx.line_to(*p)
    ctx.close_path()
    ctx.stroke()

# Layer 2: Stochastic Modularity - Recursive Blocks
random.seed(42) # Deterministic for composition balance
for r_idx in range(1, RINGS):
    r_start = (r_idx / RINGS) * MAX_RADIUS
    r_end = ((r_idx + 1) / RINGS) * MAX_RADIUS
    
    for s_idx in range(SEGMENTS):
        t_start = (s_idx / SEGMENTS) * (2 * math.pi)
        t_end = ((s_idx + 1) / SEGMENTS) * (2 * math.pi)
        
        # Parameters driven by distance from center
        normalized_dist = r_start / MAX_RADIUS
        sub_level = 1 if normalized_dist < 0.4 else 3
        
        # Color logic based on curvature/proximity
        if random.random() > 0.92:
            clr = SWISS_RED
        elif random.random() > 0.6:
            clr = WHITE
        else:
            clr = GREY
            
        line_w = 0.5 + (1.0 - normalized_dist) * 2.0
        
        draw_module(r_start, r_end, t_start, t_end, clr, line_w, subdivision=sub_level)

# Layer 3: High-Frequency Digital Grain (Lines)
# Using density to imply depth
for i in range(1200):
    r = random.uniform(MAX_RADIUS * 0.2, MAX_RADIUS * 1.1)
    theta = random.uniform(0, 2 * math.pi)
    
    # Line length modulated by distance
    length = random.uniform(2, 15) * (1.1 - (r / MAX_RADIUS))
    
    p_start = get_polar_coords(r, theta)
    p_end = get_polar_coords(r + length, theta + 0.02)
    
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.4))
    ctx.set_line_width(random.uniform(0.2, 0.8))
    ctx.move_to(*p_start)
    ctx.line_to(*p_end)
    ctx.stroke()

# Decorative Elements: Systematic Typography-like markings
ctx.set_source_rgb(0.9, 0.9, 0.9)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)

for i in range(8):
    angle = i * (math.pi / 4)
    tx, ty = get_polar_coords(MAX_RADIUS + 25, angle, distortion_scale=0)
    ctx.move_to(tx, ty)
    ctx.show_text(f"REF_{i*45:03}°")

# Final framing border (Brutalist aesthetic)
ctx.set_source_rgb(0.9, 0.9, 0.9)
ctx.set_line_width(12)
ctx.rectangle(0, 0, width, height)
ctx.stroke()
