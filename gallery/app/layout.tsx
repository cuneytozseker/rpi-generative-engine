import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Generative Engine",
  description: "A curated collection of AI-generated artworks created by a Raspberry Pi running autonomous generative algorithms",
  keywords: ["AI art", "generative art", "Raspberry Pi", "algorithmic art", "creative coding"],
  authors: [{ name: "Agentic RPi GenArt" }],
  openGraph: {
    title: "Generative Engine",
    description: "Autonomous AI-generated artworks from a Raspberry Pi",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
