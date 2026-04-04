import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Color Palette: Technical Blueprint
COLORS = {
    "bg": (0.02, 0.04, 0.08),      # Deep Navy
    "grid": (0.1, 0.2, 0.3),       # Subdued Cyan-Gray
    "accent1": (0.0, 0.8, 1.0),    # Electric Blue
    "accent2": (1.0, 0.2, 0.4),    # High-tension Coral
    "paper": (0.95, 0.95, 0.9),    # Technical Parchment (for highlights)
    "white": (0.9, 0.9, 0.95)
}

def draw_background():
    ctx.set_source_rgb(*COLORS["bg"])
    ctx.paint()
    
    # Subtle base grid
    ctx.set_line_width(0.5)
    ctx.set_source_rgba(*COLORS["grid"], 0.3)
    step = 20
    for i in range(0, width, step):
        ctx.move_to(i, 0)
        ctx.line_to(i, height)
        ctx.move_to(0, i)
        ctx.line_to(width, i)
    ctx.stroke()

def draw_technical_marker(x, y, size=4):
    """Draws a small crosshair or coordinate marker."""
    ctx.set_line_width(0.7)
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

def draw_truchet_tile(x, y, size, variant, weight, color_rgba):
    """
    Complex Truchet tile: Draws multiple concentric paths 
    to create a technical 'wiring' or 'schematic' look.
    """
    ctx.save()
    ctx.translate(x + size/2, y + size/2)
    
    # Random rotation for variety
    rotations = [0, math.pi/2, math.pi, 3*math.pi/2]
    ctx.rotate(random.choice(rotations))
    
    ctx.set_source_rgba(*color_rgba)
    ctx.set_line_width(weight)
    
    half = size / 2
    
    if variant == 0:
        # Concentric Arcs
        for offset in [0, size * 0.2, size * 0.4]:
            r = offset
            # Top-left corner arc
            ctx.arc(-half, -half, r, 0, math.pi/2)
            ctx.stroke()
            # Bottom-right corner arc
            ctx.arc(half, half, r, math.pi, 3*math.pi/2)
            ctx.stroke()
    elif variant == 1:
        # Diagonal Crossing
        ctx.move_to(-half, 0)
        ctx.line_to(0, -half)
        ctx.move_to(half, 0)
        ctx.line_to(0, half)
        ctx.stroke()
        # Add a central circle dot
        ctx.arc(0, 0, weight * 1.5, 0, 2*math.pi)
        ctx.fill()
    else:
        # Parallel lines (Circuit style)
        spacing = size / 4
        for i in [-1, 0, 1]:
            ctx.move_to(-half, i * spacing)
            ctx.line_to(half, i * spacing)
        ctx.stroke()

    ctx.restore()

def apply_masking_logic(x, y):
    """Determines intensity of activity based on flow-field logic."""
    # Using a combination of sine waves to simulate regional density
    val = math.sin(x * 0.005) * math.cos(y * 0.005) + math.sin((x+y) * 0.01)
    return (val + 1) / 2  # Normalize to 0.0 - 1.0

# --- MAIN EXECUTION ---

draw_background()

# LAYER 1: Large, low-opacity structural Truchet tiles
grid_size_lg = 80
for i in range(0, width, grid_size_lg):
    for j in range(0, height, grid_size_lg):
        density = apply_masking_logic(i, j)
        if density > 0.3:
            draw_truchet_tile(i, j, grid_size_lg, random.randint(0, 2), 1.5, (*COLORS["grid"], 0.2))

# LAYER 2: Medium tiles with technical 'hairline' precision
grid_size_md = 40
for i in range(0, width, grid_size_md):
    for j in range(0, height, grid_size_md):
        density = apply_masking_logic(i, j)
        
        # Regional variation in complexity
        if density > 0.5:
            color = COLORS["accent1"] if random.random() > 0.2 else COLORS["accent2"]
            alpha = 0.4 + (density * 0.4)
            draw_truchet_tile(i, j, grid_size_md, random.randint(0, 1), 0.8, (*color, alpha))
            
            # Symbolic dithering: Add dots at intersections in dense areas
            if density > 0.8 and random.random() > 0.7:
                ctx.set_source_rgba(*COLORS["paper"], 0.6)
                ctx.arc(i, j, 1.5, 0, 2*math.pi)
                ctx.fill()

# LAYER 3: Micro-schematics and Highlighted "Data Streams"
# We draw connecting paths that ignore the grid slightly for 'organic fluidity'
ctx.set_line_width(2.0)
for _ in range(12):
    x, y = random.uniform(0, width), random.uniform(0, height)
    ctx.set_source_rgba(*COLORS["accent1"], 0.7)
    
    # Create a "technical flow" path
    ctx.move_to(x, y)
    for _ in range(8):
        # Snap to a pseudo-grid within the path
        x += random.choice([-40, 40, 0])
        y += random.choice([-40, 40, 40])
        ctx.line_to(x, y)
        
        # Add a tiny label-like box
        if random.random() > 0.8:
            ctx.save()
            ctx.rectangle(x-2, y-2, 4, 4)
            ctx.set_source_rgb(*COLORS["accent2"])
            ctx.fill()
            ctx.restore()
            
    ctx.stroke()

# LAYER 4: Surface details - Markers and Glyphs
for _ in range(40):
    rx = random.randint(0, width//20) * 20
    ry = random.randint(0, height//20) * 20
    if apply_masking_logic(rx, ry) > 0.6:
        ctx.set_source_rgba(*COLORS["white"], 0.5)
        draw_technical_marker(rx, ry, size=3)

# Final Frame/Border for Swiss Design feel
ctx.set_line_width(20)
ctx.set_source_rgb(*COLORS["bg"])
ctx.rectangle(0, 0, width, height)
ctx.stroke()

ctx.set_line_width(1)
ctx.set_source_rgb(*COLORS["grid"])
ctx.rectangle(10, 10, width-20, height-20)
ctx.stroke()

# Output metadata/technical text simulation
ctx.set_source_rgba(*COLORS["grid"], 0.8)
ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.move_to(25, height - 25)
ctx.show_text("REF: TRUCHET_SYS_V4.0 // FLOW_FIELD_ACTIVE // SCALE: 1:40")
ctx.move_to(width - 180, 35)
ctx.show_text("COORDINATE_GRID: ENABLED")

