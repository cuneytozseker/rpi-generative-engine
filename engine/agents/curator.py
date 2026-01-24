from anthropic import AsyncAnthropic
from config.settings import ANTHROPIC_API_KEY
from pathlib import Path
import base64
import json

class CuratorAgent:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        self.taste_profile = self._load_taste_profile()
    
    def _load_taste_profile(self) -> str:
        """Load learned preferences"""
        profile_path = Path('taste_profile.md')
        if profile_path.exists():
            return profile_path.read_text()
        return "No preferences learned yet. Building taste profile from selections."
    
    async def select_best(self, rendered_sketches: list[dict]) -> dict:
        """Evaluate sketches visually and select best"""
        
        # Build message with all images
        content = [{
            "type": "text",
            "text": f"""Evaluate these generative artworks based on learned preferences:

{self.taste_profile}

For each image:
1. Score 0-10
2. What works aesthetically
3. What doesn't work

Then select the BEST ONE and explain your reasoning in detail."""
        }]
        
        # Add all images
        for sketch in rendered_sketches:
            with open(sketch['image'], 'rb') as f:
                image_data = base64.b64encode(f.read()).decode()
            
            content.extend([
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": f"SKETCH {sketch['id']}: {sketch['theme']}"
                }
            ])
        
        # Get evaluation
        response = await self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": content}]
        )
        
        evaluation_text = response.content[0].text
        
        # Parse best selection
        best_id = self._extract_best_id(evaluation_text, rendered_sketches)
        best_sketch = next(s for s in rendered_sketches if s['id'] == best_id)
        
        # Add evaluation metadata
        best_sketch['evaluation'] = evaluation_text
        best_sketch['score'] = self._extract_score(evaluation_text)
        best_sketch['reasoning'] = self._extract_reasoning(evaluation_text)
        
        return best_sketch
    
    def _extract_best_id(self, evaluation: str, sketches: list) -> str:
        """Parse which sketch was selected"""
        import re
        # Look for patterns like "SKETCH sketch_003" or "best is sketch_012"
        matches = re.findall(r'sketch_\d{3}', evaluation.lower())
        if matches:
            return matches[-1]  # Last mentioned is usually the selection
        return sketches[0]['id']  # Fallback
    
    def _extract_score(self, evaluation: str) -> str:
        """Extract score if mentioned"""
        import re
        match = re.search(r'(\d+)/10', evaluation)
        return match.group(1) if match else "N/A"
    
    def _extract_reasoning(self, evaluation: str) -> str:
        """Extract key reasoning points"""
        # Simple extraction - take last paragraph usually
        paragraphs = evaluation.split('\n\n')
        return paragraphs[-1][:200] if paragraphs else "See full evaluation"
    
    def update_taste(self, selected_sketch: dict):
        """Append selection to taste profile"""
        from datetime import datetime
        
        entry = f"""
## {datetime.now().date()} - Period Selection

**Selected**: {selected_sketch['id']}  
**Theme**: {selected_sketch['theme']}  
**Score**: {selected_sketch.get('score', 'N/A')}/10  
**Reasoning**: {selected_sketch.get('reasoning', 'N/A')}

---
"""
        
        with open('taste_profile.md', 'a') as f:
            f.write(entry)
