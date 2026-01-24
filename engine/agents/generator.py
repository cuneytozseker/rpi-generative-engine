from google import genai
from config.settings import GEMINI_API_KEY
from agents.inspiration_analyzer import InspirationAnalyzer
import re
import asyncio

SYSTEM_PROMPT = """You generate creative Python code using cairo for 2D generative art.

REQUIRED STRUCTURE:
```python
import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)  # or your choice
ctx.paint()

# YOUR GENERATIVE CODE HERE
# Available methods:
# - ctx.rectangle(x, y, w, h)
# - ctx.arc(x, y, radius, angle1, angle2)
# - ctx.move_to(x, y) / ctx.line_to(x, y)
# - ctx.set_source_rgb(r, g, b)  # values 0.0 to 1.0
# - ctx.set_line_width(width)
# - ctx.stroke() / ctx.fill()

# IMPORTANT: Don't call surface.write_to_png() - that's handled externally
```

AESTHETIC GUIDELINES:
- Swiss design principles: grids, precision, hierarchy
- High contrast (often black/white, minimal color)
- Geometric systems and parametric patterns
- Typography as visual element when relevant
- Systematic repetition with variation
- Brutalist or minimalist approaches

CRITICAL: Create visually rich, mathematically sophisticated compositions.

AVOID basic patterns:
- Plain concentric circles without variation
- Simple uniform grids
- Single geometric shape repeated identically
- Flat colors without depth or interaction

INSTEAD aim for:
- Multiple overlapping layers with transparency
- Mathematical relationships (fibonacci, golden ratio, harmonics)
- Gradual transitions and progressive changes
- Interplay between systematic order and controlled randomness
- Texture through varied repetition
- Strategic use of negative space
- Visual rhythm through modulated spacing/sizing

Draw creative INSPIRATION from reference images (DO NOT copy exactly):
- Adapt compositional principles, not exact forms
- Extract color relationships, not exact palettes  
- Learn from spatial organization, not pixel-by-pixel reproduction
- Use mathematical/algorithmic approaches that achieve similar visual effects

Be creative but maintain systematic thinking. Each sketch should explore a unique concept.
"""

class GeneratorAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = 'gemini-3-flash-preview'
        self.analyzer = InspirationAnalyzer()
    
    async def generate_batch(self, n: int, themes: list[str] = None):
        """Generate n sketches"""
        
        if not themes:
            themes = [
                "Perlin noise flow field with particle trails creating organic movement",
                "Polar coordinate transformation of Swiss grid with radial distortion",
                "Voronoi tessellation with gradient color transitions between cells", 
                "Recursive geometric subdivision using golden ratio proportions",
                "Moiré interference from two slowly rotating angular grids",
                "Isometric crystal lattice structure with simulated depth and shadows",
                "Reaction-diffusion pattern rendered in stark black and white",
                "Truchet tiles arranged with multi-layer transparency effects",
                "Penrose tiling with subtle hue shifts across the composition",
                "Fractal branching structure constrained to geometric forms",
                "Fibonacci spiral with modulated line weights and spacing",
                "Lissajous curves with harmonically related frequencies",
                "Parametric surface projection onto 2D plane with contour lines",
                "Delaunay triangulation with color-coded triangle areas",
                "Bezier curve network forming organic yet systematic patterns"
            ]
        
        # Get visual inspiration for this batch
        inspiration_brief = await self.analyzer.get_creative_direction()
        
        sketches = []
        
        for i in range(n):
            theme = themes[i % len(themes)]
            
            prompt = f"{SYSTEM_PROMPT}\n\nVISUAL INSPIRATION BRIEF:\n{inspiration_brief}\n\nCreate: {theme}\nMake it visually striking, mathematically sophisticated, and systematic."
            
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config={'temperature': 1.0}
                )
                
                code = self._extract_code(response.text)
                
                sketches.append({
                    'id': f"sketch_{i:03d}",
                    'theme': theme,
                    'code': code
                })
                
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Error generating sketch {i}: {e}")
                continue
        
        return sketches
    
    def _extract_code(self, text: str) -> str:
        """Extract Python code from markdown blocks"""
        match = re.search(r'```python\n(.*?)```', text, re.DOTALL)
        if match:
            return match.group(1)
        return text.strip()
