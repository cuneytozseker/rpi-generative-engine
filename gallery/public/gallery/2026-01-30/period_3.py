import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_metadata(ctx, x, y, label):
    """Adds small technical typographic elements for Swiss aesthetic."""
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(6)
    ctx.set_source_rgba(0.8, 0.8, 0.9, 0.6)
    ctx.move_to(x, y)
    ctx.show_text(label)

def draw_linear_grid(ctx, angle, spacing, color_rgba, dash=None):
    """Draws a series of parallel lines across the canvas at a specific angle."""
    ctx.save()
    ctx.translate(width / 2, height / 2)
    ctx.rotate(angle)
    
    r, g, b, a = color_rgba
    ctx.set_source_rgba(r, g, b, a)
    ctx.set_line_width(0.5)
    
    if dash:
        ctx.set_dash(dash)

    # Cover a large enough area to handle rotation
    extent = int(math.sqrt(width**2 + height**2))
    for i in range(-extent // 2, extent // 2, spacing):
        ctx.move_to(i, -extent // 2)
        ctx.line_to(i, extent // 2)
        ctx.stroke()
    ctx.restore()

# --- 1. CORE MOIRÉ SYSTEM ---
# We use two grids with a very slight angular offset to generate interference patterns.
angle_offset = math.radians(1.8)  # Subtle shift for wide moiré bands
spacing = 4

# Grid A: Static vertical lines
draw_linear_grid(ctx, 0, spacing, (0.7, 0.7, 0.8, 0.4))

# Grid B: Rotated lines creating the interference
draw_linear_grid(ctx, angle_offset, spacing, (0.9, 0.9, 1.0, 0.4))

# --- 2. ATMOSPHERIC ENTROPY & THERMAL GRADIENTS ---
# Central "Nucleus" Glow
radial = cairo.RadialGradient(width/2, height/2, 20, width/2, height/2, 250)
radial.add_color_stop_rgba(0, 0.1, 0.3, 0.6, 0.15) # Deep Blue core
radial.add_color_stop_rgba(0.5, 1.0, 0.2, 0.0, 0.05) # Thermal Orange fringe
radial.add_color_stop_rgba(1, 0, 0, 0, 0)
ctx.set_source(radial)
ctx.rectangle(0, 0, width, height)
ctx.fill()

# --- 3. AXIAL GROWTH NODES ---
# Drawing "Data Nodes" along the golden spiral or radial lines
for i in range(24):
    angle = i * (math.pi / 12)
    dist = 40 + (i * 12)
    px = width/2 + math.cos(angle) * dist
    py = height/2 + math.sin(angle) * dist
    
    # Draw small crosshair nodes
    ctx.set_source_rgba(1, 1, 1, 0.5)
    ctx.set_line_width(0.3)
    size = 4
    ctx.move_to(px - size, py)
    ctx.line_to(px + size, py)
    ctx.move_to(px, py - size)
    ctx.line_to(px, py + size)
    ctx.stroke()
    
    # Metadata labels near nodes
    if i % 3 == 0:
        draw_metadata(ctx, px + 6, py + 4, f"REF_{hex(1000 + i*17)}")

# --- 4. DATA-DRIVEN VERTICAL ACCENTS ---
# Mimicking "Computational Process in Flux" with staccato bursts
for _ in range(12):
    x_pos = random.randint(50, width - 50)
    y_start = random.randint(50, height - 150)
    length = random.randint(20, 100)
    
    # Variable density blocks
    ctx.set_source_rgba(0.9, 0.2, 0.1, 0.7) # High-sat thermal puncturing
    ctx.set_line_width(1.5)
    ctx.move_to(x_pos, y_start)
    ctx.line_to(x_pos, y_start + length)
    ctx.stroke()
    
    # Associated technical block
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.rectangle(x_pos + 2, y_start, 8, length)
    ctx.fill()

# --- 5. SWISS DESIGN FRAMEWORK ---
# Boundary lines and frame data
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_line_width(1)
ctx.rectangle(30, 30, width - 60, height - 60)
ctx.stroke()

# Title Block
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.set_source_rgba(1, 1, 1, 0.8)
ctx.move_to(40, 50)
ctx.show_text("INTERFERENCE_SYSTEM // TYPE: MOIRÉ")

ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(8)
ctx.move_to(40, 62)
ctx.show_text(f"ROTATION_THETA: {round(math.degrees(angle_offset), 2)}°")
ctx.move_to(40, 72)
ctx.show_text(f"GRID_PITCH: {spacing}px")

# Digital debris - scattered points
for _ in range(100):
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.4))
    rx, ry = random.random() * width, random.random() * height
    ctx.arc(rx, ry, 0.5, 0, math.pi * 2)
    ctx.fill()

# Final focal circle (minimalist precision)
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
ctx.arc(width/2, height/2, 180, 0, math.pi * 2)
ctx.stroke()

