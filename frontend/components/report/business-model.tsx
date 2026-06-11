import type { BusinessModelOutput } from "@/lib/types";

interface Props {
  data: BusinessModelOutput;
}

export function BusinessModel({ data }: Props) {
  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold text-white">Business Model</h2>
      <p className="text-sm text-white/60">{data.summary}</p>
      <p className="text-sm text-white/70">
        Recommended model: <span className="text-violet-300 font-semibold">{data.recommended_model}</span>
      </p>

      {/* Pricing tiers */}
      {data.pricing_tiers.length > 0 && (
        <div className="grid gap-3 sm:grid-cols-3">
          {data.pricing_tiers.map((t, i) => (
            <div key={i} className="bg-white/5 border border-white/8 rounded-xl p-4 space-y-2">
              <div className="flex justify-between items-baseline">
                <p className="font-semibold text-white">{t.name}</p>
                <p className="text-violet-300 font-bold text-sm">{t.price}</p>
              </div>
              <p className="text-xs text-white/40">{t.target_user}</p>
              <ul className="space-y-0.5 mt-2">
                {t.features.map((f, j) => (
                  <li key={j} className="text-xs text-white/60 flex gap-1.5">
                    <span className="text-emerald-400">✓</span> {f}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

      {/* Revenue scenarios */}
      {data.revenue_scenarios.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-2">Revenue Scenarios</h3>
          <div className="grid gap-3 sm:grid-cols-3">
            {data.revenue_scenarios.map((s, i) => (
              <div key={i} className="bg-white/5 border border-white/8 rounded-xl p-3 space-y-1">
                <p className="text-xs uppercase tracking-wide text-white/40 capitalize">{s.label}</p>
                <p className="text-sm font-semibold text-white">Y1: {s.year_1_arr}</p>
                <p className="text-sm text-white/60">Y3: {s.year_3_arr}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <p className="text-xs text-white/40 bg-white/3 rounded-lg px-3 py-2 border border-white/6">
        {data.unit_economics_notes}
      </p>
    </section>
  );
}
