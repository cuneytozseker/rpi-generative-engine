import cairo
import math
import random

# Setup
width, height = 600, 600
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Obsidian
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width * 0.45, height * 0.55  # Dynamic Asymmetry
COLS, ROWS = 45, 18
MAX_RADIUS = min(width, height) * 0.8
ACCENT_COLOR = (1.0, 0.2, 0.1)  # International Orange (Swiss Accent)
NEUTRAL_COLOR = (0.95, 0.95, 0.92)  # Bone White

def project(r_norm, theta_norm):
    """
    Transforms normalized grid coordinates (0-1) into distorted polar space.
    r_norm: distance from center (0 to 1)
    theta_norm: angular position (0 to 1)
    """
    # Non-linear radial compression (Swiss logic: precision via math)
    # Raising to a power creates 'compressed' zones near the center
    r = (r_norm ** 1.4) * MAX_RADIUS
    
    # Radial distortion: angle shifts based on distance
    # Creates a 'vortex' or 'torque' effect in the grid
    theta = theta_norm * 2 * math.pi
    theta += math.sin(r_norm * math.pi * 1.5) * 0.4
    
    x = CENTER_X + r * math.cos(theta)
    y = CENTER_Y + r * math.sin(theta)
    return x, y

# --- Layer 1: The Underlying Structural Skeleton ---
ctx.set_line_width(0.3)
ctx.set_source_rgba(*NEUTRAL_COLOR, 0.2)

for i in range(COLS):
    theta_val = i / COLS
    ctx.move_to(*project(0.05, theta_val))
    for step in range(1, 21):
        r_val = 0.05 + (step / 20.0) * 0.9
        ctx.line_to(*project(r_val, theta_val))
    ctx.stroke()

# --- Layer 2: Modular Progression & Blocks ---
# Systematic repetition with variations in element density
for j in range(ROWS):
    r_start = (j / ROWS)
    r_end = ((j + 0.8) / ROWS)
    
    # Calculate line weight based on "convergence" (nearer to center = thicker)
    weight = 0.5 + (1.0 - r_start) * 2.5
    ctx.set_line_width(weight)
    
    for i in range(COLS):
        # Probability gate for block placement (Emergent hierarchy)
        if random.random() > 0.4:
            theta_start = i / COLS
            theta_end = (i + 0.7) / COLS
            
            # Draw an "arc-segment" in the distorted space
            p1 = project(r_start, theta_start)
            p2 = project(r_start, theta_end)
            p3 = project(r_end, theta_end)
            p4 = project(r_end, theta_start)
            
            # Alternate between line fragments and solid blocks
            if random.random() > 0.85:
                # High-chroma segments (Functional Data Layer)
                ctx.set_source_rgb(*ACCENT_COLOR)
                ctx.move_to(*p1)
                ctx.line_to(*p2)
                ctx.line_to(*p3)
                ctx.line_to(*p4)
                ctx.close_path()
                ctx.fill()
            else:
                ctx.set_source_rgba(*NEUTRAL_COLOR, 0.8)
                ctx.move_to(*p1)
                ctx.line_to(*p2)
                ctx.stroke()

# --- Layer 3: High-Frequency Markers (Mechanical Dither) ---
# Small glyph-like ticks to simulate depth and digital grain
ctx.set_line_width(1.0)
for j in range(ROWS * 2):
    for i in range(COLS):
        r_val = (j / (ROWS * 2))
        theta_val = (i / COLS)
        
        if random.random() > 0.7:
            x, y = project(r_val, theta_val)
            # Create small "crosshair" markers
            size = 2 + (1.0 - r_val) * 3
            ctx.set_source_rgba(*NEUTRAL_COLOR, 0.4)
            
            ctx.move_to(x - size, y)
            ctx.line_to(x + size, y)
            ctx.move_to(x, y - size)
            ctx.line_to(x, y + size)
            ctx.stroke()

# --- Layer 4: Geometric Overlays (Hierarchy) ---
# Large circular voids that break the grid (Negative Space)
ctx.set_operator(cairo.OPERATOR_DEST_OUT) # Cut out shapes for brutalist feel
for _ in range(3):
    angle = random.uniform(0, math.pi * 2)
    dist = random.uniform(MAX_RADIUS * 0.3, MAX_RADIUS * 0.7)
    cx = CENTER_X + math.cos(angle) * dist
    cy = CENTER_Y + math.sin(angle) * dist
    
    ctx.arc(cx, cy, random.uniform(10, 40), 0, 2 * math.pi)
    ctx.fill()

ctx.set_operator(cairo.OPERATOR_OVER)

# Final Polish: Subtle Border
ctx.set_source_rgb(*NEUTRAL_COLOR)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()
