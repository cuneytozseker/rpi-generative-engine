import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Palette: Obsidian and Bone (with a hint of technical cobalt)
color_bg = (0.05, 0.05, 0.07)
color_line = (0.92, 0.91, 0.88)
color_accent = (0.2, 0.4, 0.7)

# Background
ctx.set_source_rgb(*color_bg)
ctx.paint()

def draw_technical_grid(cx, cy, size, angle, density, alpha=0.5):
    """Draws a dense parallel line grid rotated by an angle."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(angle)
    
    ctx.set_source_rgba(color_line[0], color_line[1], color_line[2], alpha)
    ctx.set_line_width(0.4)
    
    # Draw parallel lines to create interference patterns
    steps = int(size / density)
    for i in range(-steps, steps):
        pos = i * density
        ctx.move_to(pos, -size)
        ctx.line_to(pos, size)
        ctx.stroke()
        
    ctx.restore()

def draw_node_network(x, y, w, h, seed):
    """Generates a sparse link-node network for the 'data-sprawl' look."""
    random.seed(seed)
    nodes = []
    for _ in range(15):
        nodes.append((random.uniform(x, x+w), random.uniform(y, y+h)))
    
    ctx.set_source_rgba(color_accent[0], color_accent[1], color_accent[2], 0.6)
    ctx.set_line_width(0.6)
    
    for i in range(len(nodes)):
        # Connect to nearby nodes
        for j in range(i + 1, len(nodes)):
            dist = math.sqrt((nodes[i][0]-nodes[j][0])**2 + (nodes[i][1]-nodes[j][1])**2)
            if dist < 80:
                ctx.move_to(*nodes[i])
                ctx.line_to(*nodes[j])
                ctx.stroke()
        
        # Draw node marker (small cross)
        nx, ny = nodes[i]
        s = 2
        ctx.move_to(nx - s, ny)
        ctx.line_to(nx + s, ny)
        ctx.move_to(nx, ny - s)
        ctx.line_to(nx, ny + s)
        ctx.stroke()

def recursive_subdivide(x, y, w, h, depth):
    """Swiss-style grid subdivision for hierarchical scaling."""
    if depth <= 0:
        # Draw dense texture in small leaf nodes
        if random.random() > 0.4:
            draw_node_network(x, y, w, h, int(x+y))
        return

    # Draw border for hierarchy
    ctx.set_source_rgba(color_line[0], color_line[1], color_line[2], 0.15)
    ctx.set_line_width(0.3)
    ctx.rectangle(x, y, w, h)
    ctx.stroke()

    # Probability-based subdivision
    split_prob = 0.7
    if random.random() < split_prob:
        nw, nh = w/2, h/2
        recursive_subdivide(x, y, nw, nh, depth - 1)
        recursive_subdivide(x + nw, y, nw, nh, depth - 1)
        recursive_subdivide(x, y + nh, nw, nh, depth - 1)
        recursive_subdivide(x + nw, y + nh, nw, nh, depth - 1)
    else:
        # Fill some empty space with technical markings
        if w > 40:
            ctx.set_source_rgba(color_line[0], color_line[1], color_line[2], 0.2)
            ctx.move_to(x + 5, y + 10)
            ctx.set_line_width(1)
            # Simulated bitmapped text/data blocks
            for i in range(3):
                ctx.rectangle(x + 5, y + 10 + (i*4), random.uniform(5, 20), 2)
                ctx.fill()

# --- Execution ---

# 1. Base Systematic Layout (Recursive Grid)
random.seed(42)
recursive_subdivide(20, 20, width-40, height-40, 4)

# 2. Moiré Interference Layers
# Two grids slightly rotated relative to each other to create complex visual vibration
center_x, center_y = width / 2, height / 2
grid_radius = 800 # Large enough to cover rotation

# Grid A: Stable
draw_technical_grid(center_x, center_y, grid_radius, math.radians(15), 4.0, alpha=0.4)

# Grid B: Slightly offset and rotated to create the Moiré "beat" frequency
draw_technical_grid(center_x, center_y, grid_radius, math.radians(17.5), 4.2, alpha=0.4)

# 3. Structural Overlays
# Large circular technical guides (Golden Ratio influenced)
ctx.set_source_rgba(color_accent[0], color_accent[1], color_accent[2], 0.2)
ctx.set_line_width(0.8)
for i in range(1, 5):
    radius = (width * 0.15) * (1.618 ** i) * 0.3
    ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
    ctx.stroke()

# 4. Focal "Blueprint" Elements
# Adding some clinical crosshair elements
def draw_crosshair(x, y, size):
    ctx.set_source_rgb(*color_line)
    ctx.set_line_width(1.0)
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()
    ctx.arc(x, y, size * 0.5, 0, 2 * math.pi)
    ctx.stroke()

draw_crosshair(width * 0.8, height * 0.2, 15)
draw_crosshair(width * 0.15, height * 0.75, 10)

# Final high-contrast "Bitmapped" texture overlay
# Dithering effect on the edges
for _ in range(500):
    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    if random.random() > 0.95:
        ctx.set_source_rgba(color_line[0], color_line[1], color_line[2], 0.3)
        ctx.rectangle(tx, ty, 1, 1)
        ctx.fill()

# Final border to ground the composition
ctx.set_source_rgba(*color_line, 0.8)
ctx.set_line_width(2)
ctx.rectangle(10, 10, width-20, height-20)
ctx.stroke()
