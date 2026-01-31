import cairo
import math
import random

# Setup
width, height = 600, 600 # Square format works best for polar transformations
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Color Palette: Swiss Minimalist with Accented Neutrals
bg_color = (0.96, 0.95, 0.92)  # Warm cream
primary_color = (0.1, 0.1, 0.1) # Deep Charcoal
accent_ochre = (0.75, 0.45, 0.15)
accent_teal = (0.1, 0.35, 0.4)

# Background
ctx.set_source_rgb(*bg_color)
ctx.paint()

def draw_dithered_arc(ctx, cx, cy, radius, start_angle, end_angle, weight):
    """Creates a 'digital-mechanical' patina using stippled dots along an arc."""
    num_dots = int(radius * (end_angle - start_angle) * 2)
    for _ in range(num_dots):
        angle = random.uniform(start_angle, end_angle)
        r_offset = random.uniform(-weight/2, weight/2)
        x = cx + (radius + r_offset) * math.cos(angle)
        y = cy + (radius + r_offset) * math.sin(angle)
        ctx.arc(x, y, 0.5, 0, 2 * math.pi)
        ctx.fill()

def kinetic_fragmentation():
    cx, cy = width / 2, height / 2
    
    # Base configuration
    rings = 45
    base_radius = 20
    ring_spacing = 8
    
    # 1. RADIAL GRID SYSTEM (The Rigid Foundation)
    ctx.set_line_width(0.2)
    ctx.set_source_rgba(0.1, 0.1, 0.1, 0.15)
    for r in range(base_radius, int(width * 0.8), 40):
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        ctx.stroke()

    # 2. THE VECTOR FIELD DISTORTION
    # We use a flow field logic to distort the polar grid
    for i in range(rings):
        r = base_radius + (i * ring_spacing)
        
        # Centrifugal Density: inner rings have more segments, outer rings are sparser
        # but outer segments are longer (fragmentation logic)
        density_factor = max(4, 32 - (i // 2))
        angle_step = (2 * math.pi) / density_factor
        
        # Radial distortion: segments shift based on their distance from center
        distortion_shift = (i * 0.05) 
        
        for j in range(density_factor):
            start_angle = j * angle_step + distortion_shift
            
            # Mathematical "Gap" logic - creates the fragmentation
            gap = random.uniform(0.1, 0.5) 
            end_angle = start_angle + (angle_step * (1.0 - gap))
            
            # Logic Layer Selection
            logic_seed = random.random()
            
            # LAYER A: Rigid Data Packets (Sharp Rectangular Arcs)
            if logic_seed > 0.4:
                ctx.set_source_rgb(*primary_color)
                ctx.set_line_width(random.choice([1, 2, 4]))
                
                # Draw the path
                ctx.new_path()
                ctx.arc(cx, cy, r, start_angle, end_angle)
                ctx.stroke()
                
                # Occasional "Micro-scale" subdivisions
                if logic_seed > 0.85:
                    ctx.set_source_rgb(*accent_teal)
                    sub_r = r + 3
                    ctx.set_line_width(0.5)
                    ctx.arc(cx, cy, sub_r, start_angle, end_angle)
                    ctx.stroke()

            # LAYER B: Stochastic Dithering (Texture Patina)
            elif logic_seed > 0.15:
                ctx.set_source_rgba(0.1, 0.1, 0.1, 0.6)
                draw_dithered_arc(ctx, cx, cy, r, start_angle, end_angle, 4)

            # LAYER C: Chromatic Accents (Structural Markers)
            else:
                ctx.set_source_rgb(*accent_ochre)
                ctx.set_line_width(random.uniform(3, 6))
                ctx.arc(cx, cy, r, start_angle, end_angle)
                ctx.stroke()

    # 3. OVERLAY: ORTHOGONAL INTERRUPTIONS
    # Swiss-style grid lines that break the polar flow
    ctx.set_line_width(0.5)
    ctx.set_source_rgba(0.1, 0.1, 0.1, 0.3)
    grid_size = 60
    for x in range(0, width, grid_size):
        for y in range(0, height, grid_size):
            if random.random() > 0.8:
                # Draw small crosshairs or "plus" markers at grid intersections
                length = 10
                ctx.move_to(x - length, y)
                ctx.line_to(x + length, y)
                ctx.move_to(x, y - length)
                ctx.line_to(x, y + length)
                ctx.stroke()

    # 4. HIERARCHICAL SCALING: Macro Blocks
    # Large, heavy "data blocks" to anchor the composition
    for _ in range(5):
        macro_r = random.uniform(100, 250)
        macro_angle = random.uniform(0, 2 * math.pi)
        macro_width = random.uniform(0.1, 0.4)
        
        ctx.set_source_rgba(0.1, 0.1, 0.1, 0.9)
        ctx.set_line_width(12)
        ctx.arc(cx, cy, macro_r, macro_angle, macro_angle + macro_width)
        ctx.stroke()
        
        # White "knockout" line for brutalist contrast
        ctx.set_source_rgb(*bg_color)
        ctx.set_line_width(1.5)
        ctx.arc(cx, cy, macro_r, macro_angle, macro_angle + macro_width)
        ctx.stroke()

# Execution
kinetic_fragmentation()

# Final border to emphasize Swiss framing
ctx.set_source_rgb(*primary_color)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

