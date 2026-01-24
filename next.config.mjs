/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    unoptimized: true, // For static export if needed
  },
};

export default nextConfig;
```

---

## **File 4: `.gitignore` Updates**

Add to your repo's `.gitignore`:
```
# Gallery uploads (images can be large)
public/gallery/**/*.png

# But keep structure
!public/gallery/**/*.py
!public/gallery/**/*.json
```

Or keep images too (your choice):
```
# Keep everything in gallery
!public/gallery/**/*