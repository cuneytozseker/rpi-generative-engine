import shutil
import subprocess
from pathlib import Path
from config.settings import GALLERY_DIR
from datetime import datetime

class GalleryUploader:
    """GitHub-based uploader that copies files and git pushes"""
    
    def __init__(self):
        self.gallery_dir = GALLERY_DIR
    
    async def post(self, image: Path, code: str, metadata: dict) -> str:
        """Copy artwork to public gallery and push to git"""
        
        date_str = metadata['date']
        period = metadata['period']
        
        # Create directory in public/gallery/YYYY-MM-DD/
        dest_dir = self.gallery_dir / date_str
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Define destination paths
        img_dest = dest_dir / f"period_{period}.png"
        code_dest = dest_dir / f"period_{period}.py"
        json_dest = dest_dir / f"period_{period}.json"
        
        # Copy files
        shutil.copy(image, img_dest)
        code_dest.write_text(code)
        
        # Create metadata with timestamp for frontend sorting
        import json
        metadata_with_ts = {
            **metadata,
            "timestamp": datetime.now().isoformat()
        }
        json_dest.write_text(json.dumps(metadata_with_ts, indent=2))
        
        # Git operations
        try:
            repo_root = self.gallery_dir.parent.parent
            
            # Add files
            subprocess.run(["git", "add", "."], cwd=str(repo_root), check=True)
            
            # Commit
            commit_msg = f"Gallery Update: {date_str} Period {period}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(repo_root), check=True)
            
            # Push
            subprocess.run(["git", "push"], cwd=str(repo_root), check=True)
            
            return f"Successfully pushed to GitHub: Period {period}"
        except Exception as e:
            return f"Git error: {str(e)}"
