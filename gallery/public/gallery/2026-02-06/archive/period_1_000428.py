import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Constants
PHI = (1 + 5**0.5) / 2
INV_PHI = 1 / PHI
COLORS = {
    "bg": (0.02, 0.02, 0.03),      # Deep Carbon
    "signal": (0.2, 0.4, 1.0),     # Cobalt accent
    "data": (0.9, 0.9, 0.95),      # Off-white
    "dim": (0.3, 0.3, 0.35)        # Muted grey
}

# Background
ctx.set_source_rgb(*COLORS["bg"])
ctx.paint()

def draw_glyph(x, y, size, type="cross"):
    """Draws small technical markers/glyphs."""
    ctx.set_line_width(0.5)
    if type == "cross":
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
    elif type == "circle":
        ctx.arc(x, y, size/1.5, 0, 2*math.pi)
    ctx.stroke()

def fill_texture(x, y, w, h, density_type):
    """Fills a subdivision with modular patterns."""
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    
    if density_type == "dither":
        step = 4
        for i in range(0, int(w), step):
            for j in range(0, int(h), step):
                if (i + j) % (step * 2) == 0:
                    ctx.set_source_rgb(*COLORS["data"])
                    ctx.rectangle(x + i, y + j, 1, 1)
                    ctx.fill()
                    
    elif density_type == "hatch":
        ctx.set_source_rgb(*COLORS["dim"])
        ctx.set_line_width(0.4)
        step = 5
        for i in range(0, int(w + h), step):
            ctx.move_to(x + i, y)
            ctx.line_to(x + i - h, y + h)
        ctx.stroke()
        
    elif density_type == "blueprint":
        ctx.set_source_rgba(*COLORS["signal"], 0.4)
        ctx.set_line_width(0.7)
        # Internal sub-grid
        for i in range(1, 4):
            offset = (w / 4) * i
            ctx.move_to(x + offset, y)
            ctx.line_to(x + offset, y + h)
            offset_h = (h / 4) * i
            ctx.move_to(x, y + offset_h)
            ctx.line_to(x + w, y + offset_h)
        ctx.stroke()
        
    elif density_type == "points":
        ctx.set_source_rgb(*COLORS["data"])
        for _ in range(int(w * h / 100)):
            px, py = x + random.random() * w, y + random.random() * h
            draw_glyph(px, py, 1.5, random.choice(["cross", "circle"]))

    ctx.restore()

def recursive_divide(x, y, w, h, depth):
    """Recursive subdivision based on the golden ratio."""
    if depth <= 0 or w < 20 or h < 20:
        # Terminal node: fill with visual information
        if random.random() > 0.3:
            style = random.choice(["dither", "hatch", "blueprint", "points", "empty"])
            if style != "empty":
                fill_texture(x, y, w, h, style)
            
            # Boundary line
            ctx.set_source_rgba(*COLORS["dim"], 0.5)
            ctx.set_line_width(0.5)
            ctx.rectangle(x, y, w, h)
            ctx.stroke()
        return

    # Determine split orientation (alternate or choose longest)
    split_vert = w > h
    
    # Golden ratio split
    split_size = w * INV_PHI if split_vert else h * INV_PHI
    
    # Draw logic
    if split_vert:
        recursive_divide(x, y, split_size, h, depth - 1)
        recursive_divide(x + split_size, y, w - split_size, h, depth - 1)
    else:
        recursive_divide(x, y, w, split_size, depth - 1)
        recursive_divide(x, y + split_size, w, h - split_size, depth - 1)

# --- Execute Composition ---

# 1. Primary Structural Divisions
recursive_divide(40, 40, width - 80, height - 80, 7)

# 2. Vector "Signal" Overlays
# Draw long connecting paths that ignore the grid boundaries
ctx.set_source_rgba(*COLORS["signal"], 0.6)
ctx.set_line_width(1.0)
for _ in range(5):
    start_x = random.randint(0, width)
    start_y = random.randint(0, height)
    ctx.move_to(start_x, start_y)
    for _ in range(3):
        ctx.line_to(random.randint(0, width), random.randint(0, height))
    ctx.stroke()
    # Add a data point at the end
    last_x, last_y = ctx.get_current_point()
    ctx.set_source_rgb(*COLORS["data"])
    ctx.arc(last_x, last_y, 3, 0, 2*math.pi)
    ctx.fill()
    ctx.set_source_rgba(*COLORS["signal"], 0.6)

# 3. Informational "Topography" Annotations
# Small technical details in corners
ctx.set_source_rgb(*COLORS["dim"])
for i in range(10):
    tx, ty = random.randint(20, width-20), random.randint(20, height-20)
    ctx.set_line_width(0.3)
    # Mock coordinates
    ctx.move_to(tx, ty)
    ctx.line_to(tx + 20, ty)
    ctx.stroke()
    # Tiny data bars
    for b in range(random.randint(2, 5)):
        ctx.rectangle(tx + (b*4), ty - 5, 2, random.randint(2, 8))
        ctx.fill()

# 4. Final Polish: Large structural frame
ctx.set_source_rgba(*COLORS["data"], 0.15)
ctx.set_line_width(2)
ctx.rectangle(20, 20, width - 40, height - 40)
ctx.stroke()

# Marginalia
ctx.set_source_rgb(*COLORS["dim"])
ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(8)
ctx.move_to(25, 15)
ctx.show_text("REF_GR_SYSTEM_v0.9 // TOPOGRAPHIC_DATA_FRAGMENT")
ctx.move_to(width - 150, height - 10)
ctx.show_text(f"COORD_MAPPING: {width}x{height} // PHI_RECURSION")

# End of script
