import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep charcoal for a brutalist foundation
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Center of the composition
cx, cy = width / 2, height / 2

def draw_polar_grid(ctx, cx, cy, rings, sectors, distortion_factor):
    """
    Generates a polar coordinate system with non-linear radial scaling 
    and angular drift to simulate 'Structured Fluidity'.
    """
    
    # 1. Background Grid: Subtle atmospheric layering
    ctx.set_line_width(0.3)
    for i in range(rings):
        # Non-linear radial distribution (exponential growth)
        # Creates a sense of hierarchy and depth
        r = math.pow(i / rings, 1.4) * (max(width, height) * 0.7)
        
        # Color shift: Faint neutrals
        alpha = 0.1 + (i / rings) * 0.2
        ctx.set_source_rgba(0.8, 0.8, 0.9, alpha)
        
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        ctx.stroke()

    # 2. Vector Paths: The 'Fluid' Logic
    # We use a modular arithmetic approach to create rhythm
    for s in range(sectors):
        angle_base = (s / sectors) * 2 * math.pi
        
        # High-chroma accent logic: Break the neutral field at specific intervals
        is_accent = (s % 7 == 0)
        
        if is_accent:
            ctx.set_line_width(0.8)
            accent_color = random.choice([
                (0.0, 0.8, 1.0, 0.6), # Cyan
                (1.0, 0.2, 0.4, 0.6), # Crimson
                (0.9, 0.9, 0.1, 0.6)  # Yellow
            ])
            ctx.set_source_rgba(*accent_color)
        else:
            ctx.set_line_width(0.4)
            ctx.set_source_rgba(0.7, 0.7, 0.7, 0.2)

        # Draw distorted radial lines
        ctx.move_to(cx, cy)
        
        points = 40
        for p in range(points):
            # The radius grows non-linearly
            r_progression = (p / points)
            r = r_progression * (max(width, height) * 0.8)
            
            # Radial distortion: Angle drifts based on distance from center (Vortex effect)
            # and a sine wave for 'organic entropy'
            drift = (r_progression * distortion_factor) + (math.sin(r * 0.05) * 0.05)
            angle = angle_base + drift
            
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            
            ctx.line_to(px, py)
        
        ctx.stroke()

    # 3. Intersections: 'Structured Data-Flow' nodes
    # Adding geometric markers at logical mathematical intersections
    for i in range(5, rings, 4):
        r = math.pow(i / rings, 1.4) * (max(width, height) * 0.7)
        for s in range(0, sectors, 12):
            angle_base = (s / sectors) * 2 * math.pi
            drift = ((i / rings) * distortion_factor) + (math.sin(r * 0.05) * 0.05)
            angle = angle_base + drift
            
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            
            # Draw a precision marker (Swiss cross or dot)
            ctx.set_source_rgba(1, 1, 1, 0.8)
            marker_size = 1.5
            ctx.move_to(px - marker_size, py)
            ctx.line_to(px + marker_size, py)
            ctx.move_to(px, py - marker_size)
            ctx.line_to(px, py + marker_size)
            ctx.set_line_width(0.5)
            ctx.stroke()

# Execution
# Parameters: Context, center_x, center_y, rings, sectors, distortion
draw_polar_grid(ctx, cx, cy, 40, 120, 1.2)

# Overlay a subtle gradient blur effect to simulate "Atmospheric Diffusion"
# Created by drawing many large, low-opacity strokes
for _ in range(30):
    grad_x = random.uniform(0, width)
    grad_y = random.uniform(0, height)
    ctx.set_source_rgba(0.1, 0.1, 0.2, 0.01)
    ctx.arc(grad_x, grad_y, random.uniform(50, 150), 0, 2*math.pi)
    ctx.fill()

# Finishing touch: High-precision frame (Swiss aesthetic)
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.set_line_width(1.0)
frame_margin = 20
ctx.rectangle(frame_margin, frame_margin, width - frame_margin*2, height - frame_margin*2)
ctx.stroke()

# Small technical metadata (Simulated typography)
ctx.set_source_rgba(1, 1, 1, 0.5)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.move_to(width - 110, height - 28)
ctx.show_text("POLAR_SYSTEM_V.01")
ctx.move_to(width - 110, height - 38)
ctx.show_text("STRUCTURAL ENTROPY // 2024")

