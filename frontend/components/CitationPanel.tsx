"use client";

interface Source {
  text: string;
  source: string;
  page: number;
  distance: number;
}

interface CitationPanelProps {
  sources: Source[];
}

export default function CitationPanel({
  sources,
}: CitationPanelProps) {
  return (
    <div className="rounded-2xl bg-[#111827] p-6">
      <h2 className="mb-6 text-xl font-semibold text-white">
        📚 Sources
      </h2>

      {sources.length === 0 ? (
        <p className="text-gray-400">
          No citations available.
        </p>
      ) : (
        <div className="space-y-4">
          {sources.map((source, index) => {
            const relevance = Math.max(
              0,
              Math.min(
                100,
                Math.round((1 - source.distance / 2) * 100)
              )
            );

            let badgeColor = "text-red-400";

            if (relevance >= 90) {
              badgeColor = "text-green-400";
            } else if (relevance >= 70) {
              badgeColor = "text-yellow-400";
            }

            return (
              <div
                key={index}
                className="rounded-xl border border-gray-700 bg-[#1F2937] p-5"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-purple-400">
                    📄 {source.source}
                  </h3>

                  <span
                    className={`text-sm font-semibold ${badgeColor}`}
                  >
                    {relevance}% Match
                  </span>
                </div>

                <div className="mt-2 text-sm text-blue-300">
                  📖 Page {source.page}
                </div>

                <p className="mt-4 rounded-lg bg-[#111827] p-4 text-sm leading-7 text-gray-300">
                  {source.text}
                </p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}