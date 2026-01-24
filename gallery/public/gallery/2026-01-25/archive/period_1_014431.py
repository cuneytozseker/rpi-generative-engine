import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Use a deep cobalt and black palette for a technical, terminal aesthetic
BG_COLOR = (0.02, 0.02, 0.05)
PRIMARY_COLOR = (0.1, 0.4, 1.0) # Cobalt Blue
SECONDARY_COLOR = (0.9, 0.9, 1.0) # Off-white/Silver
ACCENT_COLOR = (0.3, 0.5, 0.8)

# Background
ctx.set_source_rgb(*BG_COLOR)
ctx.paint()

def draw_glyph(x, y, size):
    """Draws a micro-geometric data point (cross or dot)."""
    ctx.set_line_width(0.5)
    if random.random() > 0.5:
        # Cross
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
    else:
        # Square dot
        ctx.rectangle(x - size/2, y - size/2, size, size)
    ctx.stroke()

def draw_truchet_arc(x, y, size, orientation, weight, color, alpha=1.0):
    """Draws standard Smith-style Truchet arcs."""
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)
    ctx.set_line_width(weight)
    r = size / 2
    if orientation == 0:
        # Top-left and bottom-right
        ctx.arc(x, y, r, 0, math.pi / 2)
        ctx.stroke()
        ctx.arc(x + size, y + size, r, math.pi, 3 * math.pi / 2)
        ctx.stroke()
    else:
        # Top-right and bottom-left
        ctx.arc(x + size, y, r, math.pi / 2, math.pi)
        ctx.stroke()
        ctx.arc(x, y + size, r, 3 * math.pi / 2, 2 * math.pi)
        ctx.stroke()

def draw_metadata_label(x, y):
    """Draws tiny coordinate-aware labels to simulate data-as-texture."""
    ctx.set_source_rgba(*SECONDARY_COLOR, 0.4)
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(5)
    label = f"{int(x)}:{int(y)}"
    ctx.move_to(x + 2, y - 2)
    ctx.show_text(label)
    
    # Tiny data bar
    ctx.rectangle(x + 2, y + 2, random.randint(5, 15), 1.5)
    ctx.fill()

# --- LAYER 1: Large Brutalist Silhouettes ---
# Heavy, blocky background structures
grid_large = 120
ctx.set_operator(cairo.OPERATOR_ADD) # Additive blending for 'glow'
for i in range(0, width + grid_large, grid_large):
    for j in range(0, height + grid_large, grid_large):
        if random.random() > 0.6:
            ctx.set_source_rgba(*PRIMARY_COLOR, 0.15)
            # Randomly block out sections
            if random.random() > 0.5:
                ctx.rectangle(i, j, grid_large, grid_large/4)
            else:
                ctx.rectangle(i, j, grid_large/8, grid_large)
            ctx.fill()

# --- LAYER 2: Primary Truchet Grid ---
grid_mid = 40
random.seed(42) # Deterministic for logic, but generative
for i in range(0, width, grid_mid):
    for j in range(0, height, grid_mid):
        variant = random.randint(0, 1)
        # Main thick lines
        draw_truchet_arc(i, j, grid_mid, variant, 1.2, PRIMARY_COLOR, 0.8)
        
        # Chance for recursive subdivision
        if random.random() > 0.85:
            sub = grid_mid / 2
            for si in range(2):
                for sj in range(2):
                    draw_truchet_arc(i + si*sub, j + sj*sub, sub, random.randint(0,1), 0.5, SECONDARY_COLOR, 0.4)

# --- LAYER 3: Technical Overlays & Connectors ---
ctx.set_operator(cairo.OPERATOR_OVER)
for i in range(0, width + grid_mid, grid_mid):
    for j in range(0, height + grid_mid, grid_mid):
        # Draw "nodes" at intersections
        ctx.set_source_rgba(*SECONDARY_COLOR, 0.6)
        draw_glyph(i, j, 2)
        
        if random.random() > 0.7:
            draw_metadata_label(i, j)

# --- LAYER 4: Scanning Interference Patterns ---
# Thin horizontal hatched lines to simulate screen texture
ctx.set_line_width(0.3)
ctx.set_source_rgba(*PRIMARY_COLOR, 0.05)
for y in range(0, height, 3):
    ctx.move_to(0, y)
    ctx.line_to(width, y)
    ctx.stroke()

# --- LAYER 5: "Redacted" Data Blocks ---
# Adding Brutalist asymmetric blocks
for _ in range(5):
    ctx.set_source_rgba(*BG_COLOR, 0.9) # "Cutting" through the design
    rx = random.randint(0, width)
    ry = random.randint(0, height)
    rw = random.randint(20, 100)
    rh = 8
    ctx.rectangle(rx, ry, rw, rh)
    ctx.fill()
    
    # Outline the redaction
    ctx.set_source_rgba(*ACCENT_COLOR, 0.8)
    ctx.set_line_width(0.5)
    ctx.rectangle(rx, ry, rw, rh)
    ctx.stroke()

# Border for "Interface" feel
ctx.set_line_width(10)
ctx.set_source_rgb(*BG_COLOR)
ctx.rectangle(0, 0, width, height)
ctx.stroke()
ctx.set_line_width(1)
ctx.set_source_rgb(*ACCENT_COLOR)
ctx.rectangle(10, 10, width-20, height-20)
ctx.stroke()

