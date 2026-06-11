import type { PersonaOutput } from "@/lib/types";

interface Props {
  data: PersonaOutput;
}

export function Personas({ data }: Props) {
  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold text-white">Customer Personas</h2>
      <p className="text-sm text-white/60">{data.target_segment_summary}</p>

      <div className="grid gap-4 sm:grid-cols-2">
        {data.personas.map((p, i) => (
          <div
            key={i}
            className={`bg-white/5 border rounded-xl p-4 space-y-3 ${p.name === data.primary_persona ? "border-violet-500/30 shadow-lg shadow-violet-900/20" : "border-white/8"}`}
          >
            {p.name === data.primary_persona && (
              <span className="text-xs px-2 py-0.5 rounded-full bg-violet-500/20 text-violet-300 border border-violet-500/20">
                Primary Persona
              </span>
            )}
            <div>
              <p className="font-semibold text-white">{p.name}</p>
              <p className="text-xs text-white/50">{p.role} · {p.age_range}</p>
            </div>
            <blockquote className="text-xs italic text-white/50 border-l-2 border-white/15 pl-3">
              "{p.quote}"
            </blockquote>
            <div>
              <p className="text-xs text-white/40 uppercase tracking-wide mb-1">Pain Points</p>
              <ul className="space-y-0.5">
                {p.pain_points.map((pp, j) => (
                  <li key={j} className="text-xs text-white/60 flex gap-1.5">
                    <span className="text-red-400">·</span> {pp}
                  </li>
                ))}
              </ul>
            </div>
            <p className="text-xs text-emerald-400/80 bg-emerald-950/30 rounded px-2 py-1 border border-emerald-500/10">
              WTP: {p.willingness_to_pay}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
