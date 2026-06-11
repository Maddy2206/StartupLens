import type { MvpOutput } from "@/lib/types";
import { cn } from "@/lib/utils";

interface Props {
  data: MvpOutput;
}

const priorityStyle = {
  "must-have": "bg-violet-500/15 border-violet-500/25 text-violet-300",
  "nice-to-have": "bg-blue-500/10 border-blue-500/20 text-blue-300",
  "future": "bg-white/5 border-white/10 text-white/40",
};

export function MvpRoadmap({ data }: Props) {
  const mustHaves = data.features.filter((f) => f.priority === "must-have");
  const niceHaves = data.features.filter((f) => f.priority !== "must-have" && f.priority !== "future");
  const future = data.features.filter((f) => f.priority === "future");

  return (
    <section className="space-y-5">
      <h2 className="text-xl font-bold text-white">MVP Plan</h2>
      <p className="text-sm text-white/70 leading-relaxed">{data.mvp_description}</p>

      <div className="grid gap-3 text-sm">
        <p className="text-white/50">
          <span className="text-white/70">Tech Stack:</span> {data.tech_stack_recommendation}
        </p>
        {data.architecture_notes && (
          <p className="text-white/50">
            <span className="text-white/70">Architecture:</span> {data.architecture_notes}
          </p>
        )}
      </div>

      {/* Features */}
      {[mustHaves, niceHaves, future].some((g) => g.length > 0) && (
        <div className="space-y-2">
          <h3 className="text-sm font-semibold text-white/70">Features</h3>
          <div className="space-y-2">
            {data.features.map((f, i) => (
              <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-white/3 border border-white/6">
                <span className={cn("text-xs px-2 py-0.5 rounded-full border shrink-0 capitalize mt-0.5", priorityStyle[f.priority as keyof typeof priorityStyle] ?? "text-white/40 border-white/10")}>
                  {f.priority}
                </span>
                <div>
                  <p className="text-sm text-white/80">{f.feature}</p>
                  <p className="text-xs text-white/40 mt-0.5">{f.rationale}</p>
                </div>
                <span className="ml-auto text-xs text-white/30 capitalize shrink-0">{f.effort}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Roadmap */}
      {data.roadmap.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-3">Roadmap</h3>
          <div className="space-y-3">
            {data.roadmap.map((r, i) => (
              <div key={i} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-6 h-6 rounded-full bg-violet-500/20 border border-violet-500/30 flex items-center justify-center text-xs text-violet-300 font-bold">{i + 1}</div>
                  {i < data.roadmap.length - 1 && <div className="w-px h-full bg-white/10 mt-1" />}
                </div>
                <div className="pb-4">
                  <p className="font-semibold text-white text-sm">{r.phase} <span className="text-white/30 font-normal">· {r.duration}</span></p>
                  <ul className="mt-1 space-y-0.5">
                    {r.goals.map((g, j) => (
                      <li key={j} className="text-xs text-white/55 flex gap-1.5">
                        <span className="text-white/30">·</span> {g}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
