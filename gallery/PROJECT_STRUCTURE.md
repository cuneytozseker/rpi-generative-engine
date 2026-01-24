# AI Generative Art Gallery - Project Structure

## Project Overview
This Next.js 15 application serves as a web gallery for AI-generated artworks created by a Raspberry Pi running autonomous generative algorithms.

## Directory Structure

```
gallery/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout with metadata
│   ├── page.tsx                 # Home page (gallery view)
│   ├── globals.css              # Global styles with Tailwind
│   └── favicon.ico              # Site favicon
├── public/                       # Static assets
│   ├── gallery/                 # Artwork storage directory
│   │   └── README.md            # Gallery directory documentation
│   └── *.svg                    # Default Next.js icons
├── types/                        # TypeScript type definitions
│   └── artwork.ts               # Artwork metadata interfaces
├── next.config.ts               # Next.js configuration
├── tsconfig.json                # TypeScript configuration
├── package.json                 # Dependencies and scripts
├── postcss.config.mjs           # PostCSS with Tailwind v4
├── eslint.config.mjs            # ESLint configuration
└── .gitignore                   # Git ignore rules
```

## Technology Stack

### Core Framework
- **Next.js 16.1.4** - React framework with App Router
- **React 19.2.3** - UI library
- **TypeScript 5.x** - Type safety

### Styling
- **Tailwind CSS 4.x** - Utility-first CSS framework
- **PostCSS** - CSS processing with @tailwindcss/postcss plugin
- **Geist Fonts** - Next.js default fonts (Sans & Mono)

### Development Tools
- **ESLint 9.x** - Code linting with Next.js config
- **TypeScript** - Static type checking

## Configuration Files

### next.config.ts
- **Image Optimization**: Configured for AVIF/WebP formats
- **Remote Patterns**: Allows images from any HTTPS source
- **Standalone Output**: Ready for containerized deployment
- **Device Sizes**: Optimized for responsive images (640px to 3840px)

### tsconfig.json
- **Target**: ES2017 for modern browser compatibility
- **Module**: ESNext with bundler resolution
- **Strict Mode**: Enabled for type safety
- **Path Aliases**: `@/*` maps to root directory

### postcss.config.mjs
- Uses Tailwind CSS v4 PostCSS plugin
- No separate tailwind.config file needed (v4 approach)

## Artwork Structure

Each artwork in `public/gallery/` consists of:

1. **Image** - `artwork_id.png` (800x800 pixels)
2. **Source Code** - `artwork_id.py` (Python generation script)
3. **Metadata** - `artwork_id.json` with structure:

```json
{
  "date": "2026-01-24T10:30:00Z",
  "period": 1,
  "theme": "abstract geometric",
  "score": 85,
  "reasoning": "High contrast composition with balanced color harmony"
}
```

### Metadata Fields
- `date`: ISO 8601 timestamp of creation
- `period`: Time period (1=Morning, 2=Afternoon, 3=Evening, 4=Night)
- `theme`: Artwork theme/style description
- `score`: Quality/aesthetic score
- `reasoning`: AI evaluation or description

## TypeScript Types

Located in `types/artwork.ts`:

- **ArtworkMetadata**: Interface for metadata JSON structure
- **Artwork**: Complete artwork entry with file paths
- **PERIOD_LABELS**: Mapping of period numbers to readable labels
- **parseArtworkMetadata()**: Helper function for parsing JSON

## Available Scripts

```bash
npm run dev       # Start development server (http://localhost:3000)
npm run build     # Build for production
npm run start     # Start production server
npm run lint      # Run ESLint
```

## Next Steps

1. **Gallery Page**: Implement artwork listing in `app/page.tsx`
2. **Artwork Component**: Create reusable artwork card component
3. **File Scanning**: Add server-side logic to scan `public/gallery/` directory
4. **Artwork Detail Page**: Create `app/artwork/[id]/page.tsx` for individual views
5. **Filtering**: Add filters by period, theme, score
6. **API Routes**: Create API endpoints for Raspberry Pi uploads

## Deployment Considerations

- **Standalone Output**: Configured for Docker/containerized deployment
- **Image Optimization**: Next.js Image component optimizes PNG files
- **Static Export**: Can be converted to static export if needed
- **Environment Variables**: Consider adding for gallery path configuration

## Missing Dependencies Check

All required dependencies are installed:
- ✅ Next.js 16 with App Router
- ✅ TypeScript 5.x
- ✅ Tailwind CSS 4.x
- ✅ React 19
- ✅ ESLint with Next.js config

No additional dependencies needed for basic gallery functionality.

## Project Health Status

✅ **All Next.js files present and configured**
✅ **App directory structure correct**
✅ **TypeScript configured properly**
✅ **Tailwind CSS v4 setup complete**
✅ **Image optimization configured**
✅ **Gallery directory created**
✅ **Type definitions created**
✅ **Metadata structure defined**

**Ready for implementation of gallery features!**
