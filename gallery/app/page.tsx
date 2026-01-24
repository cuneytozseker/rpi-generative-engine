import fs from 'fs';
import path from 'path';
import Image from 'next/image';
import StatusBanner from './components/StatusBanner';

interface Artwork {
  date: string;
  period: number;
  theme: string;
  score?: string;
  reasoning?: string;
  timestamp: string;
}

async function getArtworks(): Promise<Artwork[]> {
  const galleryPath = path.join(process.cwd(), 'public', 'gallery');
  console.log('=== GALLERY DEBUG ===');
  console.log('CWD:', process.cwd());
  console.log('Gallery path:', galleryPath);
  console.log('Path exists:', fs.existsSync(galleryPath));

  if (fs.existsSync(galleryPath)) {
    const dates = fs.readdirSync(galleryPath);
    console.log('Date folders found:', dates);
  }
  
  if (!fs.existsSync(galleryPath)) {
    return [];
  }

  const artworks: Artwork[] = [];
  const dates = fs.readdirSync(galleryPath);

  for (const date of dates) {
    const datePath = path.join(galleryPath, date);
    if (!fs.statSync(datePath).isDirectory()) continue;

    const files = fs.readdirSync(datePath);
    const jsonFiles = files.filter(f => f.endsWith('.json'));

    for (const jsonFile of jsonFiles) {
      try {
        const content = fs.readFileSync(path.join(datePath, jsonFile), 'utf-8');
        const metadata = JSON.parse(content);
        artworks.push(metadata);
      } catch (e) {
        console.error(`Error reading ${jsonFile}:`, e);
      }
    }
  }

  artworks.sort((a, b) => 
    new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  );

  return artworks;
}

export default async function Gallery() {
  const artworks = await getArtworks();

  return (
    <div className="min-h-screen bg-zinc-900 text-white">
      <StatusBanner />
      
      <div className="p-8 pt-20">
        <div className="max-w-7xl mx-auto">
          <header className="mb-12">
          <h1 className="text-5xl font-bold mb-4">Generative Art Engine</h1>
          <p className="text-zinc-400 text-lg">
            Autonomous artwork generated every 6 hours by AI agents
          </p>
          <div className="mt-4 text-sm text-zinc-500">
            <span>{artworks.length} artworks generated</span>
          </div>
        </header>

        {artworks.length === 0 ? (
          <div className="text-center py-20 text-zinc-500">
            <p className="text-xl">No artworks yet. First generation starts soon...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {artworks.map((art) => (
              <div 
                key={`${art.date}-${art.period}`}
                className="bg-zinc-800 border border-zinc-700 rounded-lg overflow-hidden hover:border-zinc-500 transition-all"
              >
                <div className="relative aspect-[5/4] bg-zinc-950">
                  <Image
                    src={`/gallery/${art.date}/period_${art.period}.png`}
                    alt={art.theme}
                    fill
                    className="object-contain"
                  />
                </div>

                <div className="p-6">
                  <div className="text-xs text-zinc-500 mb-2">
                    {art.date} • Period {art.period}
                  </div>
                  
                  <h3 className="text-lg font-semibold mb-3">
                    {art.theme}
                  </h3>

                  {art.score && (
                    <div className="text-sm text-zinc-400 mb-2">
                      Score: {art.score}/10
                    </div>
                  )}

                  {art.reasoning && (
                    <p className="text-sm text-zinc-500 mb-4 line-clamp-3">
                      {art.reasoning}
                    </p>
                  )}

                  <div className="flex gap-4 text-sm">
                    <a 
                      href={`/gallery/${art.date}/period_${art.period}.py`}
                      className="text-blue-400 hover:text-blue-300"
                      download
                    >
                      View Code
                    </a>
                    <a 
                      href={`/gallery/${art.date}/period_${art.period}.png`}
                      className="text-blue-400 hover:text-blue-300"
                      download
                    >
                      Download
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export const revalidate = 60;