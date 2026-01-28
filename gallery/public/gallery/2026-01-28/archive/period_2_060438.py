import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Cobalt substrate
ctx.set_source_rgb(0.02, 0.05, 0.12)
ctx.paint()

def transform_point(x, y, cx, cy, entropy_scale):
    """
    Applies a polar transformation to a Cartesian coordinate with 
    radial distortion based on distance from center.
    """
    # Normalize relative to center
    nx, ny = (x - cx) / 200.0, (y - cy) / 200.0
    
    r = math.sqrt(nx**2 + ny**2)
    theta = math.atan2(ny, nx)
    
    # Mathematical distortion: Sine-based radial oscillation
    # This creates the "Synthetic Entropy" effect
    distortion = math.sin(theta * 6 + r * 5) * 0.15 * entropy_scale
    r_new = r + distortion
    
    # Slight angular twist based on radius
    theta_new = theta + (r * 0.4 * entropy_scale)
    
    # Back to Cartesian
    tx = cx + r_new * 250 * math.cos(theta_new)
    ty = cy + r_new * 250 * math.sin(theta_new)
    
    return tx, ty

def draw_grid_layer(ctx, cx, cy, rows, cols, entropy, color, line_width, alpha):
    """
    Draws a Swiss grid subdivided into segments and transformed into polar space.
    """
    ctx.set_line_width(line_width)
    r, g, b = color
    ctx.set_source_rgba(r, g, b, alpha)
    
    spacing = 30
    start_x = cx - (cols * spacing) / 2
    start_y = cy - (rows * spacing) / 2

    # Vertical grid lines (subdivided for smooth curves)
    for i in range(cols + 1):
        x = start_x + i * spacing
        first = True
        steps = 60
        for s in range(steps + 1):
            y = start_y + (s / steps) * (rows * spacing)
            tx, ty = transform_point(x, y, cx, cy, entropy)
            if first:
                ctx.move_to(tx, ty)
                first = False
            else:
                ctx.line_to(tx, ty)
        ctx.stroke()

    # Horizontal grid lines
    for j in range(rows + 1):
        y = start_y + j * spacing
        first = True
        steps = 60
        for s in range(steps + 1):
            x = start_x + (s / steps) * (cols * spacing)
            tx, ty = transform_point(x, y, cx, cy, entropy)
            if first:
                ctx.move_to(tx, ty)
                first = False
            else:
                ctx.line_to(tx, ty)
        ctx.stroke()

def draw_nodes(ctx, cx, cy, rows, cols, entropy):
    """
    Places small geometric nodes at the distorted intersections.
    """
    spacing = 30
    start_x = cx - (cols * spacing) / 2
    start_y = cy - (rows * spacing) / 2

    for i in range(cols + 1):
        for j in range(rows + 1):
            if (i + j) % 3 == 0: # Systematic spacing
                x = start_x + i * spacing
                y = start_y + j * spacing
                tx, ty = transform_point(x, y, cx, cy, entropy)
                
                # Spectral node color
                ctx.set_source_rgba(1.0, 0.2, 0.4, 0.8) # Vibrant Pink
                ctx.arc(tx, ty, 1.5, 0, 2 * math.pi)
                ctx.fill()
                
                # Small technical tick
                ctx.set_line_width(0.5)
                ctx.set_source_rgba(1, 1, 1, 0.5)
                ctx.move_to(tx - 4, ty)
                ctx.line_to(tx + 4, ty)
                ctx.stroke()

# --- Execution ---

cx, cy = width / 2, height / 2

# Layer 1: The "Ghost" Grid (Faint, high entropy)
draw_grid_layer(ctx, cx, cy, 16, 16, 1.8, (0.0, 0.8, 1.0), 0.5, 0.2)

# Layer 2: The Core Structural Grid
draw_grid_layer(ctx, cx, cy, 12, 12, 1.0, (1.0, 1.0, 1.0), 0.8, 0.6)

# Layer 3: Kinetic Momentum (Slightly offset spectral echo)
ctx.save()
ctx.translate(5, 5)
draw_grid_layer(ctx, cx, cy, 12, 12, 1.05, (0.5, 0.0, 1.0), 0.3, 0.3)
ctx.restore()

# Layer 4: Coordinate Nodes
draw_nodes(ctx, cx, cy, 12, 12, 1.0)

# Layer 5: Concentric Swiss Rings (Modulated by entropy)
for r_step in range(4, 12):
    radius = r_step * 25
    ctx.set_line_width(2 if r_step % 4 == 0 else 0.5)
    ctx.set_source_rgba(1, 1, 1, 0.15)
    
    first = True
    for a_step in range(100):
        angle = (a_step / 100) * 2 * math.pi
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        tx, ty = transform_point(x, y, cx, cy, 0.5) # Lower entropy for rings
        
        if first:
            ctx.move_to(tx, ty)
            first = False
        else:
            ctx.line_to(tx, ty)
    ctx.close_path()
    ctx.stroke()

# Final Detail: Visual Hierarchy labels (Swiss numeric markers)
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)

# Draw simulated coordinates on the periphery
for i in range(5):
    angle = i * (math.pi / 2.5)
    tx, ty = transform_point(cx + 200, cy + 200, cx, cy, 1.2)
    ctx.move_to(40, 40 + i * 15)
    ctx.show_text(f"NODE_REF: 00{i+1} // DISTORTION_V.{10+i}")

# Border to ground the composition
ctx.set_line_width(20)
ctx.set_source_rgb(0.02, 0.05, 0.12)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Thin white technical frame
ctx.set_line_width(0.5)
ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()

