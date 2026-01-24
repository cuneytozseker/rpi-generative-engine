/**
 * Artwork metadata structure for AI-generated art from Raspberry Pi
 */
export interface ArtworkMetadata {
  /** ISO 8601 date string when the artwork was created */
  date: string;

  /** Period of the day (1-4) when artwork was generated */
  period: 1 | 2 | 3 | 4;

  /** Theme or style of the artwork */
  theme: string;

  /** Quality/aesthetic score (typically 0-100 or 0-1) */
  score: number;

  /** AI reasoning or description of the artwork */
  reasoning: string;
}

/**
 * Complete artwork entry with file paths
 */
export interface Artwork {
  /** Unique identifier (typically timestamp or UUID) */
  id: string;

  /** Path to the PNG image (800x800) */
  imagePath: string;

  /** Path to the Python source code */
  codePath: string;

  /** Path to the metadata JSON file */
  metadataPath: string;

  /** Parsed metadata content */
  metadata: ArtworkMetadata;
}

/**
 * Period labels for display purposes
 */
export const PERIOD_LABELS: Record<1 | 2 | 3 | 4, string> = {
  1: "Morning",
  2: "Afternoon",
  3: "Evening",
  4: "Night",
};

/**
 * Helper to parse artwork metadata from JSON
 */
export function parseArtworkMetadata(json: unknown): ArtworkMetadata {
  const data = json as Record<string, unknown>;

  return {
    date: String(data.date || ""),
    period: (data.period as 1 | 2 | 3 | 4) || 1,
    theme: String(data.theme || ""),
    score: Number(data.score || 0),
    reasoning: String(data.reasoning || ""),
  };
}
