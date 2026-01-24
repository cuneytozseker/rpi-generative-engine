from google import genai
from config.settings import GEMINI_API_KEY
from pathlib import Path
import PIL.Image
import random

class InspirationAnalyzer:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = 'gemini-3-flash-preview'
        self.inspiration_dir = Path(__file__).parent.parent / 'inspiration'

    def get_inspiration_images(self):
        """Get list of images from inspiration folder recursively"""
        extensions = ['*.png', ['*.jpg'], ['*.jpeg'], ['*.webp']]
        images = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.webp']:
            images.extend(list(self.inspiration_dir.rglob(ext)))
        return images

    async def get_creative_direction(self):
        """Analyze a random selection of inspiration images and return text direction"""
        image_paths = self.get_inspiration_images()
        if not image_paths:
            return "No inspiration images found. Proceed with standard creative direction."

        # Pick 1-3 random images for this period's inspiration
        selected_paths = random.sample(image_paths, min(len(image_paths), 3))
        
        prompt = """Analyze these reference images to provide creative direction for a generative artist using Python and Cairo.
        
        Identify:
        1. Compositional Principles: (e.g., dynamic symmetry, radial balance, rhythmic repetition)
        2. Geometric Logic: (e.g., recursive subdivisions, intersecting grids, organic flow fields)
        3. Visual Texture: (e.g., density variations, line weight modulation, transparency layering)
        4. Color Interaction: (e.g., high-contrast monochromatic, subtle gradients, accented neutrals)
        
        Output a concise 'Creative Brief' (approx 150 words) that describes these principles as abstract concepts.
        DO NOT provide code. DO NOT suggest reproducing the images exactly. 
        Focus on the underlying SYSTEM and AESTHETIC logic."""

        # Prepare images for Gemini
        images = [PIL.Image.open(p) for p in selected_paths]
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[prompt, *images]
            )
            return response.text
        except Exception as e:
            print(f"Error analyzing inspiration: {e}")
            return "Focus on complex mathematical layering and sophisticated geometric rhythms."
