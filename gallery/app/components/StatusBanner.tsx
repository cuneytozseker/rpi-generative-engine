'use client';

import { useEffect, useState } from 'react';

interface Status {
  agent: string;
  task: string;
  progress?: string;
  timestamp: string;
  next_cycle?: string;
}

export default function StatusBanner() {
  const [status, setStatus] = useState<Status | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch('https://iXd015wZzy3Iv6mg.public.blob.vercel-storage.com/status.json', {
          cache: 'no-store'
        });
        
        if (res.ok) {
          const data = await res.json();
          setStatus(data);
          setIsLoading(false);
        }
      } catch (e) {
        console.error('Failed to fetch status:', e);
        setIsLoading(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);

    return () => clearInterval(interval);
  }, []);

  if (isLoading || !status) {
    return null;
  }

  const isActive = status.agent !== 'Idle';
  const timestamp = new Date(status.timestamp);
  const timeSince = timestamp.toLocaleTimeString();

  return (
    <div className={`fixed top-0 left-0 right-0 z-50 transition-colors ${
      isActive 
        ? 'bg-blue-900/90 backdrop-blur text-blue-100' 
        : 'bg-zinc-800/90 backdrop-blur text-zinc-400'
    }`}>
      <div className="max-w-7xl mx-auto px-8 py-3">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-3">
            {isActive && (
              <div className="relative">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" />
                <div className="absolute inset-0 w-2 h-2 bg-blue-400 rounded-full animate-ping" />
              </div>
            )}
            <span className="font-semibold">{status.agent}</span>
            <span className="opacity-50">•</span>
            <span>{status.task}</span>
            {status.progress && (
              <>
                <span className="opacity-50">•</span>
                <span className="font-mono">{status.progress}</span>
              </>
            )}
          </div>

          <div className="flex items-center gap-4 text-xs opacity-70">
            <span>Updated: {timeSince}</span>
            {status.next_cycle && status.agent === 'Idle' && (
              <>
                <span>•</span>
                <span>Next cycle: {status.next_cycle}</span>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
