"use client";

interface Source {
  text: string;
  source: string;
  distance: number;
}

interface CitationPanelProps {
  sources: Source[];
}

export default function CitationPanel({
  sources,
}: CitationPanelProps) {
  return (
    <div className="rounded-2xl border border-gray-800 bg-[#111827] p-6">
      <h2 className="mb-4 text-xl font-semibold text-white">
        Sources
      </h2>

      {sources.length === 0 ? (
        <p className="text-gray-400">
          No citations yet.
        </p>
      ) : (
        <div className="space-y-4">
          {sources.map((source, index) => (
            <div
              key={index}
              className="rounded-xl border border-gray-700 bg-[#1F2937] p-4"
            >
              <h3 className="font-semibold text-purple-400">
                📄 {source.source}
              </h3>

              <p className="mt-2 text-sm text-gray-300">
                {source.text}
              </p>

              <p className="mt-3 text-xs text-gray-500">
                Similarity Score: {source.distance.toFixed(3)}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}