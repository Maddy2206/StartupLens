import type { CompetitorOutput } from "@/lib/types";
import { Badge } from "@/components/ui/badge";

interface Props {
  data: CompetitorOutput;
}

export function CompetitorTable({ data }: Props) {
  const all = [...data.direct_competitors, ...data.indirect_competitors];

  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold text-white">Competitor Analysis</h2>
      <p className="text-sm text-white/60">{data.summary}</p>

      {all.length > 0 && (
        <div className="space-y-3">
          {all.map((c, i) => (
            <div key={i} className="bg-white/5 border border-white/8 rounded-xl p-4 space-y-2">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-semibold text-white">{c.name}</p>
                  <p className="text-xs text-white/50">{c.description}</p>
                </div>
                <Badge variant="outline" className="shrink-0 text-xs border-white/15 text-white/50">
                  {c.pricing}
                </Badge>
              </div>
              <div className="flex flex-wrap gap-1">
                {c.key_features.map((f) => (
                  <span key={f} className="text-xs px-2 py-0.5 rounded-full bg-white/8 text-white/55 border border-white/8">
                    {f}
                  </span>
                ))}
              </div>
              <p className="text-xs text-red-400/80 bg-red-950/30 border border-red-500/10 rounded-lg px-3 py-1.5">
                ⚠ {c.weakness}
              </p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
