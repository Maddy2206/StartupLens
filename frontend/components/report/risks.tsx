import type { RiskOutput } from "@/lib/types";
import { cn } from "@/lib/utils";

interface Props {
  data: RiskOutput;
}

const severityStyle = {
  high: "text-red-400 bg-red-950/40 border-red-500/20",
  medium: "text-yellow-400 bg-yellow-950/40 border-yellow-500/20",
  low: "text-blue-400 bg-blue-950/40 border-blue-500/20",
};

export function Risks({ data }: Props) {
  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold text-white">Risks & Challenges</h2>
      <p className="text-sm text-white/60">Overall risk level: <span className="text-white/80">{data.overall_risk_level}</span></p>

      <div className="space-y-2">
        {data.risks.map((r, i) => (
          <div key={i} className="bg-white/5 border border-white/8 rounded-xl p-4 space-y-2">
            <div className="flex items-center gap-2">
              <span className={cn("text-xs px-2 py-0.5 rounded-full border capitalize", severityStyle[r.severity as keyof typeof severityStyle] ?? "text-white/50 bg-white/5 border-white/10")}>
                {r.severity}
              </span>
              <span className="text-xs text-white/40 capitalize">{r.category}</span>
            </div>
            <p className="text-sm text-white/75">{r.risk}</p>
            <p className="text-xs text-emerald-400/70 flex gap-1.5">
              <span>Mitigation:</span> {r.mitigation}
            </p>
          </div>
        ))}
      </div>

      {data.devils_advocate.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-2">Devil's Advocate</h3>
          <ul className="space-y-1">
            {data.devils_advocate.map((q, i) => (
              <li key={i} className="text-sm text-white/55 flex gap-2">
                <span className="text-yellow-400 shrink-0">?</span> {q}
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.failure_modes.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-2">Failure Modes</h3>
          <ul className="space-y-1">
            {data.failure_modes.map((f, i) => (
              <li key={i} className="text-xs text-red-300/70 flex gap-1.5">
                <span className="text-red-500">☠</span> {f}
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
