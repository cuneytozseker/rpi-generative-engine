import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep charcoal for a brutalist foundation
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Constants for Isometric Projection
# We project (x, y, z) into (u, v)
# u = (x - y) * cos(30 deg)
# v = (x + y) * sin(30 deg) - z
ISO_ANGLE = math.radians(30)
COS_A = math.cos(ISO_ANGLE)
SIN_A = math.sin(ISO_ANGLE)
SCALE = 180
OFF_X = width / 2
OFF_Y = height / 2 + 40

def to_iso(x, y, z):
    """Translates 3D coordinates to 2D isometric space."""
    u = (x - y) * COS_A * SCALE
    v = ((x + y) * SIN_A - z) * SCALE
    return OFF_X + u, OFF_Y + v

def draw_lattice_edge(p1, p2, weight, alpha):
    """Draws a single connection in the lattice with specific styling."""
    x1, y1 = to_iso(*p1)
    x2, y2 = to_iso(*p2)
    ctx.set_line_width(weight)
    ctx.set_source_rgba(0.9, 0.9, 1.0, alpha)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

def draw_cube_face(points, color_val, alpha):
    """Draws a semi-transparent face to simulate depth/shadow."""
    ctx.set_source_rgba(color_val, color_val, color_val + 0.1, alpha)
    u, v = to_iso(*points[0])
    ctx.move_to(u, v)
    for p in points[1:]:
        u, v = to_iso(*p)
        ctx.line_to(u, v)
    ctx.close_path()
    ctx.fill()

def recursive_lattice(x, y, z, size, depth):
    """
    Generates a recursive isometric structure.
    Each cube is either subdivided or rendered as a lattice node.
    """
    if depth == 0 or (depth < 3 and random.random() < 0.2):
        # Render the 'Atomic' node of the lattice
        s = size * 0.5
        
        # Define vertices of a sub-cube
        v = [
            (x-s, y-s, z-s), (x+s, y-s, z-s), (x+s, y+s, z-s), (x-s, y+s, z-s),
            (x-s, y-s, z+s), (x+s, y-s, z+s), (x+s, y+s, z+s), (x-s, y+s, z+s)
        ]
        
        # Draw some faces for "earned grey" shading and volume
        # Top face
        draw_cube_face([v[4], v[5], v[6], v[7]], 0.4, 0.05)
        # Right face
        draw_cube_face([v[1], v[2], v[6], v[5]], 0.2, 0.08)
        
        # Draw edges (Lattice connections)
        edges = [
            (0,1), (1,2), (2,3), (3,0), # bottom
            (4,5), (5,6), (6,7), (7,4), # top
            (0,4), (1,5), (2,6), (3,7)  # verticals
        ]
        
        for e in edges:
            w = 0.3 if depth == 0 else 0.8 / (4 - depth)
            draw_lattice_edge(v[e[0]], v[e[1]], w, 0.4 + (depth * 0.1))

    else:
        # Subdivide into 8 octants with systematic variation
        new_size = size / 2
        offsets = [-new_size, new_size]
        for dx in offsets:
            for dy in offsets:
                for dz in offsets:
                    # Deterministic probability based on position to create hierarchy
                    prob = 0.7 - (depth * 0.1)
                    if random.random() < prob:
                        recursive_lattice(x + dx, y + dy, z + dz, new_size, depth - 1)

# Main Execution
random.seed(42) # Ensure consistent geometric elegance

# 1. Background Grid / Network Floor
# Creates a sense of the coordinate field
for i in range(-5, 6):
    draw_lattice_edge((i*0.2, -1, 0), (i*0.2, 1, 0), 0.2, 0.1)
    draw_lattice_edge((-1, i*0.2, 0), (1, i*0.2, 0), 0.2, 0.1)

# 2. Primary Recursive Structure
# Starting at center (0,0,0.5) with size 1.0, 4 levels of recursion
recursive_lattice(0, 0, 0.5, 0.8, 4)

# 3. Floating Data-markers (Swiss aesthetic detail)
# Adds small "nodes" at intersection points
for _ in range(15):
    rx = random.choice([-0.8, -0.4, 0, 0.4, 0.8])
    ry = random.choice([-0.8, -0.4, 0, 0.4, 0.8])
    rz = random.choice([0, 0.4, 0.8, 1.2])
    
    u, v = to_iso(rx, ry, rz)
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.arc(u, v, 1.5, 0, 2 * math.pi)
    ctx.fill()
    
    # Tiny numeric labels (symbolic mapping)
    if random.random() > 0.7:
        ctx.set_source_rgba(1, 1, 1, 0.4)
        ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(6)
        ctx.move_to(u + 5, v)
        ctx.show_text(f"{rx:.1f}:{rz:.1f}")

# 4. Final Global Overlay
# A subtle gradient to provide atmospheric depth
overlay = cairo.LinearGradient(0, 0, 0, height)
overlay.add_color_stop_rgba(0, 0, 0, 0, 0.2)
overlay.add_color_stop_rgba(1, 0, 0, 0, 0.0)
ctx.set_source(overlay)
ctx.rectangle(0, 0, width, height)
ctx.fill()

# Clean structural border for Swiss precision
ctx.set_source_rgb(0.8, 0.8, 0.8)
ctx.set_line_width(10)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

