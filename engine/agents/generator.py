import google.generativeai as genai
from config.settings import GEMINI_API_KEY
import re
import asyncio

SYSTEM_PROMPT = """You generate creative Python code using cairo for 2D generative art.

REQUIRED STRUCTURE:
```python
import cairo
import math
import random

# Setup
width, height = 800, 800
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

Be creative but maintain systematic thinking. Each sketch should explore a unique concept.
"""

class GeneratorAgent:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    async def generate_batch(self, n: int, themes: list[str] = None):
        """Generate n sketches"""
        
        if not themes:
            themes = [
                "Swiss grid with bold geometric shapes",
                "Concentric circles with systematic offset",
                "Parametric line pattern with rotation",
                "Modular typography system",
                "Wave interference in black and white",
                "Brutalist composition with rectangles",
                "Nested squares with golden ratio",
                "Radial symmetry with breaking points"
            ]
        
        sketches = []
        
        for i in range(n):
            theme = themes[i % len(themes)]
            
            prompt = f"{SYSTEM_PROMPT}\n\nCreate: {theme}\nMake it visually striking and systematic."
            
            try:
                response = await self.model.generate_content_async(
                    prompt,
                    generation_config={'temperature': 1.0}
                )
                
                code = self._extract_code(response.text)
                
                sketches.append({
                    'id': f"sketch_{i:03d}",
                    'theme': theme,
                    'code': code
                })
                
                # Small delay to respect rate limits
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
