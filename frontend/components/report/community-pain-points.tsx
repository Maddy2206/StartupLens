import type { CommunityOutput } from "@/lib/types";
import { cn } from "@/lib/utils";

interface Props {
  data: CommunityOutput;
}

const freqColor = {
  high: "text-red-400 bg-red-950/40 border-red-500/20",
  medium: "text-yellow-400 bg-yellow-950/40 border-yellow-500/20",
  low: "text-blue-400 bg-blue-950/40 border-blue-500/20",
};

export function CommunityPainPoints({ data }: Props) {
  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold text-white">Community Pain Points</h2>
      <p className="text-sm text-white/60">{data.summary}</p>

      <div className="space-y-2">
        {data.pain_points.map((p, i) => (
          <div key={i} className="bg-white/5 border border-white/8 rounded-xl p-4 space-y-2">
            <div className="flex items-center gap-2">
              <span className={cn("text-xs px-2 py-0.5 rounded-full border capitalize", freqColor[p.frequency as keyof typeof freqColor] ?? "text-white/50 bg-white/5 border-white/10")}>
                {p.frequency}
              </span>
              <span className="text-xs text-white/40">{p.source}</span>
            </div>
            <p className="text-sm text-white/75">{p.pain_point}</p>
            {p.example_quote && (
              <p className="text-xs italic text-white/45 border-l-2 border-white/15 pl-3">
                "{p.example_quote}"
              </p>
            )}
          </div>
        ))}
      </div>

      {data.feature_requests.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-2">Top Feature Requests</h3>
          <ul className="space-y-1">
            {data.feature_requests.map((f, i) => (
              <li key={i} className="flex gap-2 text-sm text-white/60">
                <span className="text-emerald-400">+</span> {f}
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.underserved_segments.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-2">Underserved Segments</h3>
          <div className="flex flex-wrap gap-2">
            {data.underserved_segments.map((s) => (
              <span key={s} className="text-xs px-3 py-1 rounded-full border border-violet-500/20 bg-violet-500/10 text-violet-300">
                {s}
              </span>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
