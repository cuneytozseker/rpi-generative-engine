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

        # Create archive directory for historical records
        archive_dir = dest_dir / "archive"
        archive_dir.mkdir(exist_ok=True)

        # Unique timestamped paths for the archive
        time_str = datetime.now().strftime("%H%M%S")
        img_archive = archive_dir / f"period_{period}_{time_str}.png"
        code_archive = archive_dir / f"period_{period}_{time_str}.py"
        json_archive = archive_dir / f"period_{period}_{time_str}.json"

        # Copy files to archive
        shutil.copy(image, img_archive)
        code_archive.write_text(code)

        # Create/Update "latest" version for the web frontend (this is what Vercel shows)
        latest_img = dest_dir / f"period_{period}.png"
        latest_code = dest_dir / f"period_{period}.py"
        latest_json = dest_dir / f"period_{period}.json"
        
        shutil.copy(image, latest_img)
        latest_code.write_text(code)

        # Create metadata with timestamp
        import json
        metadata_with_ts = {
            **metadata,
            "timestamp": datetime.now().isoformat()
        }
        json_content = json.dumps(metadata_with_ts, indent=2)
        
        # Save to both locations
        json_archive.write_text(json_content)
        latest_json.write_text(json_content)

        # Git operations
        try:
            # Find repo root by looking for .git folder upwards from GALLERY_DIR
            repo_root = self.gallery_dir
            while repo_root != repo_root.parent:
                if (repo_root / '.git').exists():
                    break
                repo_root = repo_root.parent
            
            # Ensure we pull first
            subprocess.run(["git", "pull", "--rebase"], cwd=str(repo_root), check=True)

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