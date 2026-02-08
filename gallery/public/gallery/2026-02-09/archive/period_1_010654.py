import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.02, 0.02, 0.03)  # Deep technical charcoal
ctx.paint()

# Configuration
GRID_SIZE = 8
COLS = width // GRID_SIZE
ROWS = height // GRID_SIZE
ACCENT_COLOR = (1.0, 0.2, 0.2)  # Functional red highlight

def get_field_value(x, y):
    """
    Simulates a reaction-diffusion 'Turing' state using layered interference patterns.
    This creates the labyrinthine structures of RD simulations mathematically.
    """
    nx, ny = x * 0.05, y * 0.05
    # Layering frequencies to create organic-yet-systematic interference
    val = math.sin(nx) + math.sin(ny)
    val += math.sin(nx * 0.5 + ny * 0.8) * 1.2
    val += math.cos(nx * 0.2 - ny * 0.3) * 0.8
    # Add high-frequency jitter for 'staccato' feel
    val += math.sin(nx * 5.0) * 0.1
    return val

# 1. DRAW TECHNICAL UNDERLAY (THE "CARTOGRAPHY" GRID)
ctx.set_line_width(0.5)
ctx.set_source_rgba(0.2, 0.2, 0.25, 0.4)
for i in range(0, width, GRID_SIZE * 4):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
for j in range(0, height, GRID_SIZE * 4):
    ctx.move_to(0, j)
    ctx.line_to(width, j)
    ctx.stroke()

# 2. GENERATE KINETIC REACTION FIELD
# We iterate through the grid and interpret field values as "axis-aligned primitives"
for r in range(ROWS):
    for c in range(COLS):
        x = c * GRID_SIZE
        y = r * GRID_SIZE
        
        # Calculate localized intensity
        val = get_field_value(c, r)
        
        # Thresholding for "stark black and white" logic
        # High intensity = dense blocks, Mid = thin shards, Low = void
        if val > 0.8:
            # Dense solid blocks (The "Hotspots")
            ctx.set_source_rgb(0.95, 0.95, 0.98)
            size_mod = math.sin(val) * 0.5 + 0.5
            ctx.rectangle(x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            ctx.fill()
            
            # Occasional technical highlight
            if random.random() > 0.98:
                ctx.set_source_rgb(*ACCENT_COLOR)
                ctx.rectangle(x - GRID_SIZE, y, GRID_SIZE * 3, 1)
                ctx.fill()

        elif 0.2 < val <= 0.8:
            # Fragmented shards (Quantized motion)
            ctx.set_source_rgba(0.8, 0.8, 0.9, 0.7)
            ctx.set_line_width(0.8)
            if random.random() > 0.5:
                # Vertical shard
                ctx.move_to(x + GRID_SIZE/2, y)
                ctx.line_to(x + GRID_SIZE/2, y + GRID_SIZE * random.uniform(0.5, 2.0))
            else:
                # Horizontal shard
                ctx.move_to(x, y + GRID_SIZE/2)
                ctx.line_to(x + GRID_SIZE * random.uniform(0.5, 2.0), y + GRID_SIZE/2)
            ctx.stroke()

        elif -0.2 < val <= 0.2:
            # "Ghost" lines / Metadata dots
            if random.random() > 0.9:
                ctx.set_source_rgba(0.4, 0.4, 0.5, 0.5)
                ctx.rectangle(x + 2, y + 2, 1.5, 1.5)
                ctx.fill()

# 3. OVERLAY VECTOR DISPLACEMENT STRANDS
# Long, thin horizontal/vertical trajectories that follow the 'flow'
ctx.set_line_width(0.3)
for _ in range(40):
    curr_x = random.randint(0, width)
    curr_y = random.randint(0, height)
    ctx.set_source_rgba(1, 1, 1, 0.15)
    
    ctx.move_to(curr_x, curr_y)
    for _ in range(15):
        # Step in axis-aligned directions based on field value
        v = get_field_value(curr_x / GRID_SIZE, curr_y / GRID_SIZE)
        if abs(v) > 0.5:
            curr_x += GRID_SIZE if v > 0 else -GRID_SIZE
        else:
            curr_y += GRID_SIZE if v > 0 else -GRID_SIZE
        
        ctx.line_to(curr_x, curr_y)
    ctx.stroke()

# 4. MARGINALIA (Swiss Design Typography-like elements)
def draw_marker(x, y, label):
    ctx.set_source_rgb(0.6, 0.6, 0.7)
    ctx.set_line_width(1)
    # Draw a tiny corner bracket
    ctx.move_to(x, y + 5)
    ctx.line_to(x, y)
    ctx.line_to(x + 5, y)
    ctx.stroke()
    # Draw a small data-bar
    ctx.rectangle(x, y + 10, random.randint(10, 30), 2)
    ctx.fill()

draw_marker(20, 20, "SYS_01")
draw_marker(width - 50, height - 30, "REF_DATA")
draw_marker(20, height - 30, "RD_SIM_V4")

# Final contrast pass: random vertical slices to break symmetry
ctx.set_source_rgba(0.02, 0.02, 0.03, 0.3)
for _ in range(5):
    slice_x = random.randint(0, width)
    ctx.rectangle(slice_x, 0, 2, height)
    ctx.fill()
