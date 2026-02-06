import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Void
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Isometric Projection Parameters
ISO_SCALE = 35
OFFSET_X = width / 2
OFFSET_Y = height / 2 + 50

def project(x, y, z):
    """Converts 3D coordinates to 2D Isometric projection."""
    # Standard isometric transformation
    u = (x - y) * math.cos(math.radians(30))
    v = (x + y) * math.sin(math.radians(30)) - z
    return u * ISO_SCALE + OFFSET_X, v * ISO_SCALE + OFFSET_Y

def draw_cube_face(p1, p2, p3, p4, color, alpha=1.0):
    """Draws a single projected face for simulated depth."""
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.line_to(*p3)
    ctx.line_to(*p4)
    ctx.close_path()
    r, g, b = color
    ctx.set_source_rgba(r, g, b, alpha)
    ctx.fill()

# Geometric Logic: Systematic Lattice with Entropy
nodes = []
grid_size = 7
entropy_factor = 0.15

# 1. Generate jittered lattice nodes
for x in range(-grid_size, grid_size + 1):
    for y in range(-grid_size, grid_size + 1):
        for z in range(-grid_size, grid_size + 1):
            # Create a "Core" density: higher probability of nodes near center
            dist = math.sqrt(x**2 + y**2 + z**2)
            prob = math.exp(-dist**2 / (grid_size * 2))
            
            if random.random() < prob:
                # Add systematic entropy (jitter)
                jx = x + random.uniform(-entropy_factor, entropy_factor)
                jy = y + random.uniform(-entropy_factor, entropy_factor)
                jz = z + random.uniform(-entropy_factor, entropy_factor)
                nodes.append((jx, jy, jz))

# 2. Draw Simulated Shadows (Faces) to create depth
# Sorting by depth (approximate z-order for isometric)
nodes.sort(key=lambda n: n[0] + n[1] + n[2])

for n in nodes:
    x, y, z = n
    p_top = project(x, y, z + 0.5)
    p_left = project(x - 0.5, y, z)
    p_right = project(x, y - 0.5, z)
    p_bottom = project(x, y, z - 0.5)
    
    # Draw faint volumetric silhouettes
    if random.random() > 0.8:
        ctx.set_line_width(0.2)
        ctx.set_source_rgba(1, 1, 1, 0.05)
        ctx.arc(*project(x,y,z), 2, 0, 2*math.pi)
        ctx.stroke()

# 3. Draw Point-to-Point Connectivity (Structural Vectors)
ctx.set_line_width(0.4)
for i, n1 in enumerate(nodes):
    for n2 in nodes[i+1:]:
        # Only connect neighbors within a certain Euclidean distance
        d_sq = (n1[0]-n2[0])**2 + (n1[1]-n2[1])**2 + (n1[2]-n2[2])**2
        if 0.8 < d_sq < 1.5:
            p1 = project(*n1)
            p2 = project(*n2)
            
            # Line modulation based on height (Z)
            avg_z = (n1[2] + n2[2]) / 2
            alpha = max(0.1, (avg_z + grid_size) / (grid_size * 2))
            
            ctx.set_source_rgba(0.8, 0.9, 1.0, alpha * 0.4)
            ctx.move_to(*p1)
            ctx.line_to(*p2)
            ctx.stroke()

# 4. Sparse Chromatic Vocabulary (Jewel-toned "Signal" nodes)
jewel_cyan = (0.0, 1.0, 0.8)
jewel_magenta = (1.0, 0.0, 0.4)

for n in nodes:
    dist = math.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
    # Highlight specific mathematical nodes
    if 2.0 < dist < 2.5 and random.random() > 0.6:
        p = project(*n)
        
        # Glow effect
        for r in range(1, 6):
            ctx.set_source_rgba(0, 1, 0.8, 0.15 / r)
            ctx.arc(p[0], p[1], r * 1.5, 0, 2 * math.pi)
            ctx.fill()
            
        # Core node
        ctx.set_source_rgb(*jewel_cyan)
        ctx.arc(p[0], p[1], 1.2, 0, 2 * math.pi)
        ctx.fill()
        
        # Crosshairs / Swiss Markers
        ctx.set_line_width(0.5)
        ctx.move_to(p[0] - 8, p[1])
        ctx.line_to(p[0] + 8, p[1])
        ctx.move_to(p[0], p[1] - 8)
        ctx.line_to(p[0], p[1] + 8)
        ctx.set_source_rgba(0, 1, 0.8, 0.5)
        ctx.stroke()

# 5. Stochastic Dithering / Technical Background Texture
for _ in range(1500):
    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.05, 0.2))
    ctx.rectangle(tx, ty, 0.7, 0.7)
    ctx.fill()

# 6. Fine-gauge vector fan (Mathematical Moiré)
ctx.set_line_width(0.1)
ctx.set_source_rgba(1, 1, 1, 0.1)
anchor_node = nodes[0]
p_anchor = project(*anchor_node)
for i in range(0, 360, 2):
    angle = math.radians(i)
    ctx.move_to(p_anchor[0], p_anchor[1])
    ctx.line_to(p_anchor[0] + math.cos(angle) * 800, p_anchor[1] + math.sin(angle) * 800)
    ctx.stroke()

# 7. Marginalia (Swiss Design Precision)
ctx.set_source_rgb(0.5, 0.5, 0.6)
ctx.set_line_width(1)
# Top border frame piece
ctx.move_to(40, 40)
ctx.line_to(140, 40)
ctx.stroke()
# Bottom right "data" block
ctx.rectangle(width-60, height-60, 20, 20)
ctx.set_source_rgb(*jewel_magenta)
ctx.fill()

# Cleanup
# surface.write_to_png("systematic_entropy.png")
