import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Colors - "Structured Neutral" palette
BG_COLOR = (0.05, 0.05, 0.07)  # Deep charcoal
ACCENT_BLUE = (0.1, 0.2, 0.4)   # Cobalt
ACCENT_CREAM = (0.95, 0.92, 0.88)
ACCENT_VIVID = (0.9, 0.2, 0.1)  # Saturated Red

# Background
ctx.set_source_rgb(*BG_COLOR)
ctx.paint()

# 1. Generate Stochastic Points with Dynamic Asymmetry
# Biasing points towards the right-middle to create a gravitational anchor
num_points = 42
points = []
for _ in range(num_points):
    # Gaussian distribution to create a "cluster" or "tension" point
    px = random.gauss(width * 0.7, width * 0.2)
    py = random.gauss(height * 0.5, height * 0.25)
    points.append((px, py))

def get_closest_points(x, y, points, count=2):
    """Returns the indices and distances of the N closest points."""
    dists = []
    for i, p in enumerate(points):
        d = math.sqrt((x - p[0])**2 + (y - p[1])**2)
        dists.append((d, i))
    dists.sort()
    return dists[:count]

# 2. Additive Density: Rendering Voronoi cells via Micro-lines
# We iterate through a grid and draw lines that flow toward the cell centers
step = 6
for x in range(0, width, step):
    for y in range(0, height, step):
        # Determine Voronoi influence
        nearby = get_closest_points(x, y, points, 2)
        dist1, idx1 = nearby[0]
        dist2, idx2 = nearby[1]
        
        # Calculate a ratio for gradient transitions between cells
        # This creates the "emergence" between rigid cells
        ratio = dist1 / (dist1 + dist2 + 0.1)
        
        # Orientation: vector toward the primary seed point
        target = points[idx1]
        angle = math.atan2(target[1] - y, target[0] - x)
        
        # Line properties
        length = step * 1.8 * (1.0 - ratio) # Lines are longer near centers
        line_weight = 0.5 + (1.0 - ratio) * 1.5
        
        # Color transition based on cell index and distance ratio
        if idx1 % 7 == 0:
            color = ACCENT_VIVID
            alpha = 0.8 * (1.0 - ratio)
        elif idx1 % 3 == 0:
            color = ACCENT_CREAM
            alpha = 0.4 * (1.0 - ratio)
        else:
            color = ACCENT_BLUE
            alpha = 0.2 * (1.0 - ratio)

        ctx.set_source_rgba(color[0], color[1], color[2], alpha)
        ctx.set_line_width(line_weight)
        
        # Draw micro-line
        nx = x + math.cos(angle) * length
        ny = y + math.sin(angle) * length
        ctx.move_to(x, y)
        ctx.line_to(nx, ny)
        ctx.stroke()

# 3. Rigid Structure Overlay (Swiss Design Influence)
# Drawing a precision grid and coordinate markers to contrast the fluid cells
ctx.set_line_width(0.4)
ctx.set_source_rgba(0.95, 0.92, 0.88, 0.15) # Faint cream grid

grid_spacing = 60
for i in range(0, width, grid_spacing):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
for j in range(0, height, grid_spacing):
    ctx.move_to(0, j)
    ctx.line_to(width, j)
    ctx.stroke()

# 4. Connecting Nodes (Point-to-Point Connectivity)
# Drawing thin connections between adjacent Voronoi seeds to show systemic order
ctx.set_line_width(0.2)
for i in range(len(points)):
    # Find nearest neighbors for each point to draw the "graph"
    p1 = points[i]
    dists = []
    for j in range(len(points)):
        if i == j: continue
        d = math.sqrt((p1[0]-points[j][0])**2 + (p1[1]-points[j][1])**2)
        dists.append((d, j))
    dists.sort()
    
    # Connect to 3 nearest neighbors
    for k in range(3):
        p2 = points[dists[k][1]]
        ctx.set_source_rgba(0.95, 0.92, 0.88, 0.2)
        ctx.move_to(p1[0], p1[1])
        ctx.line_to(p2[0], p2[1])
        ctx.stroke()

# 5. Strategic Accents: Circular "Probes"
# Small geometric markers at seed locations
for i, p in enumerate(points):
    if i % 5 == 0:
        ctx.set_source_rgb(*ACCENT_CREAM)
        ctx.arc(p[0], p[1], 1.5, 0, 2*math.pi)
        ctx.fill()
        
        # Structural crosshairs
        size = 8
        ctx.set_line_width(0.5)
        ctx.move_to(p[0]-size, p[1])
        ctx.line_to(p[0]+size, p[1])
        ctx.move_to(p[0], p[1]-size)
        ctx.line_to(p[0], p[1]+size)
        ctx.stroke()

# Border for "Swiss" poster feel
ctx.set_source_rgb(*ACCENT_CREAM)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

