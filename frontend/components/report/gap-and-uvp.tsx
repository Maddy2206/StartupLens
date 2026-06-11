import type { GapOutput } from "@/lib/types";

interface Props {
  data: GapOutput;
}

export function GapAndUVP({ data }: Props) {
  return (
    <section className="space-y-5">
      <h2 className="text-xl font-bold text-white">Gap & Opportunity ⭐</h2>

      {/* UVP highlight */}
      <div className="bg-gradient-to-br from-violet-600/20 to-blue-600/10 border border-violet-500/30 rounded-2xl p-5 space-y-1">
        <p className="text-xs uppercase tracking-widest text-violet-400/70">Unique Value Proposition</p>
        <p className="text-lg font-semibold text-white leading-snug">{data.unique_value_proposition}</p>
        <p className="text-sm text-white/50">{data.differentiation_angle}</p>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <h3 className="text-sm font-semibold text-white/70">Incumbent Shortcomings</h3>
          <ul className="space-y-1.5">
            {data.incumbent_shortcomings.map((s, i) => (
              <li key={i} className="flex gap-2 text-sm text-red-300/80">
                <span className="text-red-500 mt-0.5 shrink-0">✗</span> {s}
              </li>
            ))}
          </ul>
        </div>

        <div className="space-y-2">
          <h3 className="text-sm font-semibold text-white/70">How to Win</h3>
          <ul className="space-y-1.5">
            {data.how_to_win.map((w, i) => (
              <li key={i} className="flex gap-2 text-sm text-emerald-300/80">
                <span className="text-emerald-500 mt-0.5 shrink-0">✓</span> {w}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {data.market_gaps.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-2">Market Gaps</h3>
          <ul className="space-y-1">
            {data.market_gaps.map((g, i) => (
              <li key={i} className="flex gap-2 text-sm text-blue-300/80">
                <span className="text-blue-400">→</span> {g}
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
