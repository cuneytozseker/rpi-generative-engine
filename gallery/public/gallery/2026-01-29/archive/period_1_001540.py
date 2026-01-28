import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Stark Black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def get_field_value(x, y):
    """
    Simulates a reaction-diffusion 'Turing' field using 
    interference of multiple sine-wave octaves.
    """
    nx = x * 0.015
    ny = y * 0.015
    
    # Summing harmonic frequencies to create "vermiculated" (worm-like) patterns
    val = math.sin(nx) + math.sin(ny)
    val += math.sin(nx * 2.1 + ny * 1.3) * 0.5
    val += math.sin(nx * 0.5 - ny * 1.8) * 0.5
    val += math.sin(math.sqrt(nx*nx + ny*ny) * 0.8)
    
    return val

def draw_turing_ribbon(x, y, length, steps):
    """
    Draws a single path following the gradient of the field
    to mimic the organic growth of reaction-diffusion.
    """
    ctx.move_to(x, y)
    curr_x, curr_y = x, y
    
    # Use variable transparency for "atmospheric" depth
    alpha = random.uniform(0.1, 0.6)
    ctx.set_source_rgba(1, 1, 1, alpha)
    
    for _ in range(steps):
        v = get_field_value(curr_x, curr_y)
        # Calculate angle based on field value (thresholding the 'reaction')
        angle = v * math.pi * 1.5
        
        curr_x += math.cos(angle) * length
        curr_y += math.sin(angle) * length
        
        # Keep within bounds with a slight margin
        if 0 <= curr_x <= width and 0 <= curr_y <= height:
            ctx.line_to(curr_x, curr_y)
        else:
            break
            
    ctx.set_line_width(0.6)
    ctx.stroke()

# --- 1. THE REACTION FIELD (Atmospheric Layer) ---
# Create thousands of fine traces to build density
for _ in range(1200):
    rx = random.uniform(0, width)
    ry = random.uniform(0, height)
    draw_turing_ribbon(rx, ry, 4, random.randint(5, 25))

# --- 2. THE RIGID SYSTEM (Swiss Grid Layer) ---
# Overlapping a geometric hierarchy to ground the fluidity
grid_size = 60
for i in range(int(width / grid_size) + 1):
    for j in range(int(height / grid_size) + 1):
        px = i * grid_size
        py = j * grid_size
        
        # Check field at grid point
        val = get_field_value(px, py)
        
        # Swiss Design Element: Crosshair or Scale
        if abs(val) > 1.2:
            ctx.set_source_rgba(1, 1, 1, 0.8)
            ctx.set_line_width(1.5)
            # Draw a rigid geometric marker
            size = 10
            ctx.move_to(px - size, py)
            ctx.line_to(px + size, py)
            ctx.move_to(px, py - size)
            ctx.line_to(px, py + size)
            ctx.stroke()
            
            # Recursive subdivision logic: draw smaller box if "active"
            ctx.rectangle(px - 2, py - 2, 4, 4)
            ctx.fill()

# --- 3. MOIRÉ INTERFERENCE (High Contrast Texture) ---
# Draw rhythmic horizontal lines modulated by the field
line_spacing = 6
for l in range(0, height, line_spacing):
    ctx.move_to(0, l)
    segments = 100
    for s in range(segments + 1):
        sx = (s / segments) * width
        # Modulate Y position slightly based on field value
        sy = l + (get_field_value(sx, l) * 5)
        
        # Thresholding for "Dithered" bit-pattern look
        if get_field_value(sx, l) > 0.5:
            ctx.set_line_width(0.8)
            ctx.set_source_rgba(1, 1, 1, 0.9)
            ctx.line_to(sx, sy)
        else:
            ctx.move_to(sx, sy)
    ctx.stroke()

# --- 4. DATA OVERLAY (Brutalist Typography/Marks) ---
# Adding systematic labels to imply a "computational" readout
ctx.set_source_rgb(1, 1, 1)
for k in range(5):
    tx = 40
    ty = 40 + (k * 100)
    ctx.set_line_width(0.5)
    ctx.move_to(tx, ty)
    ctx.line_to(tx + 40, ty) # Horizontal rule
    ctx.stroke()
    
    # Tiny "bit" rectangles
    for b in range(4):
        if random.random() > 0.5:
            ctx.rectangle(tx + (b * 10), ty + 5, 6, 2)
            ctx.fill()

# --- 5. THE CENTER OF REACTION ---
# A focal point where the math is most 'solid'
ctx.arc(width/2, height/2, 80, 0, 2*math.pi)
ctx.set_source_rgba(0, 0, 0, 0.7) # Dark "void" to clear the center
ctx.fill()

# Re-draw heavy Turing worms inside the void
for _ in range(200):
    angle = random.uniform(0, math.pi * 2)
    dist = random.uniform(0, 75)
    rx = width/2 + math.cos(angle) * dist
    ry = height/2 + math.sin(angle) * dist
    
    # High contrast white against the void
    ctx.set_source_rgba(1, 1, 1, 0.9)
    ctx.set_line_width(1.2)
    
    # Small circular "cells"
    val = get_field_value(rx, ry)
    if val > 0:
        ctx.arc(rx, ry, abs(val) * 2, 0, 2*math.pi)
        ctx.stroke()

# Edge vignette to focus the atmospheric effect
lg = cairo.LinearGradient(0, 0, 0, height)
lg.add_color_stop_rgba(0, 0, 0, 0, 1.0)
lg.add_color_stop_rgba(0.2, 0, 0, 0, 0.0)
lg.add_color_stop_rgba(0.8, 0, 0, 0, 0.0)
lg.add_color_stop_rgba(1, 0, 0, 0, 1.0)
ctx.set_source(lg)
ctx.paint()

