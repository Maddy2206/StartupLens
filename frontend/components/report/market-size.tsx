import type { MarketResearchOutput } from "@/lib/types";

interface Props {
  data: MarketResearchOutput;
}

export function MarketSizeSection({ data }: Props) {
  const { market_size, key_trends, market_drivers, market_barriers, supporting_stats, summary } = data;

  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold text-white">Market Research</h2>
      <p className="text-sm text-white/60">{summary}</p>

      {/* TAM/SAM/SOM */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "TAM", value: market_size.tam, color: "text-violet-300" },
          { label: "SAM", value: market_size.sam, color: "text-blue-300" },
          { label: "SOM", value: market_size.som, color: "text-cyan-300" },
        ].map((m) => (
          <div key={m.label} className="bg-white/5 rounded-xl p-4 border border-white/8 text-center space-y-1">
            <p className="text-xs uppercase tracking-widest text-white/40">{m.label}</p>
            <p className={`text-sm font-semibold ${m.color}`}>{m.value}</p>
          </div>
        ))}
      </div>
      <p className="text-xs text-white/40">Growth rate: {market_size.growth_rate}</p>

      {key_trends.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-2">Key Trends</h3>
          <ul className="space-y-1">
            {key_trends.map((t, i) => (
              <li key={i} className="flex gap-2 text-sm text-white/60">
                <span className="text-violet-400 mt-0.5">→</span> {t}
              </li>
            ))}
          </ul>
        </div>
      )}

      {supporting_stats.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-2">Supporting Stats</h3>
          <ul className="space-y-1">
            {supporting_stats.map((s, i) => (
              <li key={i} className="text-xs text-white/50 bg-white/3 rounded px-3 py-1.5 border border-white/6">
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
