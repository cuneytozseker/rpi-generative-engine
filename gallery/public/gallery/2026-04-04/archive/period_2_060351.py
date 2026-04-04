import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Slate/Cobalt Base
ctx.set_source_rgb(0.02, 0.03, 0.08)
ctx.paint()

# Configuration
center_x, center_y = width // 2, height // 2
num_rings = 45
num_sectors = 72
max_radius = min(width, height) * 0.45
random.seed(42)

def draw_glyph(ctx, x, y, size, glyph_type, color, weight=0.5):
    """Draws a technical primitive from a discrete library."""
    ctx.set_source_rgba(*color)
    ctx.set_line_width(weight)
    
    if glyph_type == "cross":
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
        ctx.stroke()
    elif glyph_type == "circle":
        ctx.arc(x, y, size, 0, 2 * math.pi)
        ctx.stroke()
    elif glyph_type == "dot":
        ctx.arc(x, y, size * 0.5, 0, 2 * math.pi)
        ctx.fill()
    elif glyph_type == "hairline":
        ctx.move_to(x, y - size * 2)
        ctx.line_to(x, y + size * 2)
        ctx.stroke()

# 1. ATMOSPHERIC DEPTH LAYER (Blurred Glow)
# Using transparency and larger, soft-edged logic
for i in range(num_rings):
    for j in range(num_sectors):
        # Normalize coordinates
        r_norm = i / num_rings
        theta_norm = j / num_sectors
        
        # Radial distortion logic
        distortion = math.sin(theta_norm * math.pi * 8 + r_norm * 5) * 15
        r = (r_norm * max_radius) + distortion
        theta = theta_norm * 2 * math.pi
        
        x = center_x + r * math.cos(theta)
        y = center_y + r * math.sin(theta)
        
        # Spectral logic: Violet to Thermal Orange
        if random.random() > 0.85:
            dist_to_center = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            intensity = (math.sin(dist_to_center * 0.05) + 1) / 2
            
            # Color ramp: Deep Violet (0.3, 0, 0.6) to Orange (1, 0.4, 0)
            r_col = 0.3 + (0.7 * intensity)
            g_col = 0.0 + (0.4 * intensity)
            b_col = 0.6 - (0.6 * intensity)
            
            ctx.set_source_rgba(r_col, g_col, b_col, 0.1) # Soft glow
            ctx.arc(x, y, 4 + intensity * 8, 0, 2 * math.pi)
            ctx.fill()

# 2. STRUCTURAL GRID (The "Swiss" Polar Grid)
# Fine lines and geometric precision
for i in range(num_rings):
    # Dynamic interval for data-pulse effect
    if i % 3 != 0: continue 
    
    for j in range(num_sectors):
        r_norm = i / num_rings
        theta_norm = j / num_sectors
        
        # Asymmetrical expansion logic
        pulse = math.sin(theta_norm * math.pi * 4) * 10
        r = (r_norm * max_radius) + pulse
        theta = theta_norm * 2 * math.pi
        
        # Distortion based on coordinate mapping
        r += math.cos(r * 0.1) * 5
        
        x = center_x + r * math.cos(theta)
        y = center_y + r * math.sin(theta)
        
        # Determine glyph type based on density/position
        density_val = math.sin(r_norm * 10) * math.cos(theta_norm * 10)
        
        glyph_choice = "cross"
        if density_val > 0.5: glyph_choice = "circle"
        elif density_val < -0.5: glyph_choice = "dot"
        
        # Color: Mostly white hairlines, occasional spectral peaks
        color = (1, 1, 1, 0.8)
        if abs(density_val) > 0.8:
            # Thermal orange peak
            color = (1.0, 0.4, 0.0, 0.9)
        
        # Adaptive sizing for rhythmic progression
        size = 1.0 + (r_norm * 3.0)
        draw_glyph(ctx, x, y, size, glyph_choice, color, weight=0.4)

# 3. INTERCONNECTING TOPOGRAPHICAL CONTOURS
# Drawing the "Data-Pulse" connections
ctx.set_line_width(0.2)
for j in range(0, num_sectors, 4):
    ctx.move_to(center_x, center_y)
    prev_x, prev_y = center_x, center_y
    
    for i in range(0, num_rings):
        r_norm = i / num_rings
        theta_norm = j / num_sectors
        
        # Match the distortion logic of the grid
        pulse = math.sin(theta_norm * math.pi * 4) * 10
        r = (r_norm * max_radius) + pulse + math.cos(r_norm * 20) * 5
        theta = theta_norm * 2 * math.pi
        
        x = center_x + r * math.cos(theta)
        y = center_y + r * math.sin(theta)
        
        # Draw connections with varying alpha to create depth
        ctx.set_source_rgba(1, 1, 1, 0.15 * (1 - r_norm))
        ctx.line_to(x, y)
        ctx.stroke()
        ctx.move_to(x, y)

# 4. OVERLAY - BRUTALIST ANNOTATIONS
# Adding high-contrast technical marks
for _ in range(12):
    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(max_radius * 0.8, max_radius * 1.1)
    tx = center_x + dist * math.cos(angle)
    ty = center_y + dist * math.sin(angle)
    
    # Draw "data markers"
    ctx.set_source_rgba(1, 1, 1, 0.9)
    ctx.set_line_width(1.0)
    ctx.move_to(tx, ty)
    ctx.line_to(tx + (15 if tx > center_x else -15), ty)
    ctx.stroke()
    
    # Small square terminal
    ctx.rectangle(tx - 1, ty - 1, 2, 2)
    ctx.fill()

# Final Polish: Central Seed point
ctx.set_source_rgb(1, 1, 1)
ctx.arc(center_x, center_y, 2, 0, 2 * math.pi)
ctx.fill()
