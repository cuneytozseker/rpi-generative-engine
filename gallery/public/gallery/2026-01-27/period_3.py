import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Palette: Obsidian and Bone
COLOR_BG = (0.05, 0.05, 0.07)    # Deep Obsidian
COLOR_LINE = (0.95, 0.92, 0.88)  # Aged Bone
COLOR_SHADOW = (0.02, 0.02, 0.03)

# Background
ctx.set_source_rgb(*COLOR_BG)
ctx.paint()

def iso_projection(x, y, z):
    """Converts 3D coordinates to Isometric 2D coordinates."""
    # Standard isometric angles: 30 degrees
    angle = math.radians(30)
    curr_x = (x - y) * math.cos(angle)
    curr_y = (x + y) * math.sin(angle) - z
    return curr_x, curr_y

def draw_lattice_node(ctx, x, y, z, size, alpha=1.0):
    """Draws a small diamond/rhombus representing a lattice node."""
    px, py = iso_projection(x, y, z)
    ctx.save()
    ctx.translate(px, py)
    
    # Draw a small isometric octahedron/diamond
    ctx.move_to(0, -size)
    ctx.line_to(size * 0.8, 0)
    ctx.line_to(0, size)
    ctx.line_to(-size * 0.8, 0)
    ctx.close_path()
    
    ctx.set_source_rgba(COLOR_LINE[0], COLOR_LINE[1], COLOR_LINE[2], alpha)
    ctx.set_line_width(0.5)
    ctx.stroke()
    ctx.restore()

# Parameters
grid_size = 12
spacing = 25
center_offset = (grid_size - 1) * spacing / 2
max_dist = math.sqrt(3 * (center_offset**2))

ctx.translate(width / 2, height / 2 + 50)

# 1. SHADOW LAYER (Ground Projection)
ctx.set_source_rgba(0, 0, 0, 0.3)
for i in range(grid_size):
    for j in range(grid_size):
        for k in range(grid_size):
            # Central Attractor Logic
            dx, dy, dz = i * spacing - center_offset, j * spacing - center_offset, k * spacing - center_offset
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            # Stochastic dispersion: only draw if within certain probability/radius
            influence = 1.0 - (dist / max_dist)
            if random.random() > influence * 1.5:
                continue

            # Project shadow onto ground plane (z = 0, but offset)
            sh_x, sh_y = iso_projection(dx, dy, -center_offset - 20)
            ctx.arc(sh_x, sh_y, 1.2, 0, 2 * math.pi)
            ctx.fill()

# 2. CRYSTAL LATTICE CONNECTIONS (The "Information Topography")
ctx.set_line_width(0.4)

for i in range(grid_size):
    for j in range(grid_size):
        for k in range(grid_size):
            x, y, z = i * spacing - center_offset, j * spacing - center_offset, k * spacing - center_offset
            dist = math.sqrt(x*x + y*y + z*z)
            influence = 1.0 - (dist / max_dist)
            
            # Only draw structural elements based on centripetal tension
            if random.random() > influence * 1.8:
                continue

            px, py = iso_projection(x, y, z)
            
            # Connect to neighbors (right, forward, up) to form the grid
            neighbors = [(spacing, 0, 0), (0, spacing, 0), (0, 0, spacing)]
            
            for nx, ny, nz in neighbors:
                # Add a bit of jitter for "glitch" aesthetic
                jitter = (random.uniform(-1, 1) * (1 - influence) * 5)
                
                npx, npy = iso_projection(x + nx, y + ny, z + nz)
                
                # Check if neighbor exists within logic
                n_dist = math.sqrt((x+nx)**2 + (y+ny)**2 + (z+nz)**2)
                if n_dist < max_dist * 0.9:
                    ctx.move_to(px, py)
                    ctx.line_to(npx + jitter, npy + jitter)
                    
                    # Gradient effect through alpha
                    ctx.set_source_rgba(COLOR_LINE[0], COLOR_LINE[1], COLOR_LINE[2], influence * 0.6)
                    ctx.stroke()

# 3. NODES AND HIGH-FREQUENCY DETAILS
for i in range(grid_size):
    for j in range(grid_size):
        for k in range(grid_size):
            x, y, z = i * spacing - center_offset, j * spacing - center_offset, k * spacing - center_offset
            dist = math.sqrt(x*x + y*y + z*z)
            influence = 1.0 - (dist / max_dist)
            
            if influence > 0.6 and random.random() > 0.3:
                # Core density
                draw_lattice_node(ctx, x, y, z, size=2, alpha=influence)
            elif influence > 0.3 and random.random() > 0.8:
                # Sparse periphery
                draw_lattice_node(ctx, x, y, z, size=1, alpha=influence * 0.5)

# 4. OVERLAY: TECHNICAL MEASUREMENT LINES (Brutalist Elements)
ctx.set_source_rgba(COLOR_LINE[0], COLOR_LINE[1], COLOR_LINE[2], 0.15)
ctx.set_line_width(0.3)

# Vertical axis marker
ctx.move_to(0, -height/2)
ctx.line_to(0, height/2)
ctx.stroke()

# Crosshair markers at corners
def draw_crosshair(cx, cy, sz):
    ctx.move_to(cx - sz, cy); ctx.line_to(cx + sz, cy)
    ctx.move_to(cx, cy - sz); ctx.line_to(cx, cy + sz)
    ctx.stroke()

draw_crosshair(-width/2 + 40, -height/2 + 40, 10)
draw_crosshair(width/2 - 40, -height/2 + 40, 10)
draw_crosshair(-width/2 + 40, height/2 - 80, 10)
draw_crosshair(width/2 - 40, height/2 - 80, 10)

# Data bits (randomly placed small rects)
for _ in range(40):
    rx = random.uniform(-width/2, width/2)
    ry = random.uniform(-height/2, height/2)
    ctx.rectangle(rx, ry, 2, 2)
    ctx.fill()

# Final Polish: Focal glow
# Create a subtle radial overlay to focus the center
gradient = cairo.RadialGradient(0, 0, 50, 0, 0, 350)
gradient.add_color_stop_rgba(0, 1, 1, 1, 0.05)
gradient.add_color_stop_rgba(1, 0, 0, 0, 0)
ctx.set_source(gradient)
ctx.mask(gradient)

