import cairo
import math
import random

# Setup
width, height = 600, 600
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Obsidian Black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Constants
CX, CY = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
NUM_RINGS = 60
NUM_WEDGES = 72
GOLDEN_RATIO = (1 + 5 ** 0.5) / 2

def draw_polar_block(r, dr, theta, dtheta, color, alpha=1.0, fill=True):
    """Draws a segment of a polar grid cell."""
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)
    
    # Path construction for a polar 'rectangle'
    ctx.arc(CX, CY, r, theta, theta + dtheta)
    ctx.line_to(CX + (r + dr) * math.cos(theta + dtheta), CY + (r + dr) * math.sin(theta + dtheta))
    ctx.arc_negative(CX, CY, r + dr, theta + dtheta, theta)
    ctx.close_path()
    
    if fill:
        ctx.fill()
    else:
        ctx.stroke()

# 1. Structural Layer: Fine Grid Scaffolding
ctx.set_line_width(0.2)
for i in range(NUM_RINGS):
    # Non-linear radial spacing using power function for centripetal density
    r = MAX_RADIUS * math.pow(i / NUM_RINGS, 1.4)
    ctx.set_source_rgba(0.8, 0.8, 0.9, 0.15)
    ctx.arc(CX, CY, r, 0, 2 * math.pi)
    ctx.stroke()

# 2. Systematic Erosion & Polar Transformation
for i in range(NUM_RINGS):
    # Sinusoidal modulation of ring thickness
    ring_width = (MAX_RADIUS / NUM_RINGS) * (1.5 + math.sin(i * 0.2))
    r = MAX_RADIUS * math.pow(i / NUM_RINGS, 1.2)
    
    # Probability of element existence decreases with radius (Erosion)
    erosion_factor = 1.0 - (i / NUM_RINGS)
    
    for j in range(NUM_WEDGES):
        theta = (j / NUM_WEDGES) * 2 * math.pi
        d_theta = (2 * math.pi / NUM_WEDGES) * 0.8
        
        # Stochastic check for element presence
        if random.random() < (erosion_factor * 0.95):
            
            # Axial Symmetry Logic (Mirroring)
            # We use a glitch offset to break perfect symmetry occasionally
            glitch = 0
            if random.random() > 0.98:
                glitch = random.uniform(-10, 10)
            
            # Color logic: High contrast monochrome with rare punctuation
            seed = random.random()
            if seed > 0.985:
                # Chromatic Punctuation: Neon Cyan
                color = (0.0, 1.0, 0.9)
                alpha = 0.9
                r_offset = glitch
            elif seed > 0.97:
                # Chromatic Punctuation: Vibrant Magenta
                color = (1.0, 0.0, 0.4)
                alpha = 0.9
                r_offset = glitch
            else:
                # Swiss Neutrals
                gray_val = random.uniform(0.7, 1.0)
                color = (gray_val, gray_val, gray_val + 0.05)
                alpha = random.uniform(0.4, 0.8)
                r_offset = 0

            # Draw block
            draw_polar_block(r + r_offset, ring_width * 0.8, theta, d_theta, color, alpha)
            
            # Axial Mirroring (Rorschach effect)
            mirrored_theta = -theta - d_theta
            draw_polar_block(r + r_offset, ring_width * 0.8, mirrored_theta, d_theta, color, alpha * 0.5)

# 3. Precision Detail: Radial Connectors
ctx.set_line_width(0.5)
for j in range(0, NUM_WEDGES, 4):
    theta = (j / NUM_WEDGES) * 2 * math.pi
    # Logarithmic interval for stroke markers
    for k in range(5):
        r_start = MAX_RADIUS * (k / 5)
        ctx.set_source_rgba(1, 1, 1, 0.3)
        ctx.move_to(CX + r_start * math.cos(theta), CY + r_start * math.sin(theta))
        ctx.line_to(CX + (r_start + 10) * math.cos(theta), CY + (r_start + 10) * math.sin(theta))
        ctx.stroke()

# 4. Digital Noise / "Dithered" Artifacts
# Tiny particles following the grid logic
for _ in range(400):
    r_rand = MAX_RADIUS * math.sqrt(random.random())
    theta_rand = random.uniform(0, 2 * math.pi)
    size = random.uniform(0.5, 1.5)
    
    # Concentrate noise near the center
    if random.random() > (r_rand / MAX_RADIUS):
        ctx.set_source_rgba(1, 1, 1, random.uniform(0.2, 0.6))
        ctx.rectangle(CX + r_rand * math.cos(theta_rand), 
                      CY + r_rand * math.sin(theta_rand), 
                      size, size)
        ctx.fill()

# 5. Final Systematic Overlay: Outer Ring Data
ctx.set_line_width(1.0)
ctx.set_source_rgb(0.9, 0.9, 0.9)
ctx.arc(CX, CY, MAX_RADIUS + 10, 0, 2 * math.pi)
ctx.set_dash([2, 10])
ctx.stroke()

# Compass markers
for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
    ctx.set_dash([])
    ctx.set_line_width(2)
    ctx.move_to(CX + (MAX_RADIUS + 5) * math.cos(angle), CY + (MAX_RADIUS + 5) * math.sin(angle))
    ctx.line_to(CX + (MAX_RADIUS + 20) * math.cos(angle), CY + (MAX_RADIUS + 20) * math.sin(angle))
    ctx.stroke()

