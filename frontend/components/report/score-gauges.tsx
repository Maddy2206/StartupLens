"use client";

import { Progress } from "@/components/ui/progress";
import type { ScoreBreakdown } from "@/lib/types";

interface Props {
  validationScore: number;
  validationRationale: string;
  differentiationScore: number;
  differentiationRationale: string;
  breakdown: ScoreBreakdown[];
}

function ScoreRing({ score, label, color }: { score: number; label: string; color: string }) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className={`relative flex items-center justify-center w-24 h-24 rounded-full border-4 ${color}`}>
        <span className="text-3xl font-bold text-white">{score}</span>
        <span className="absolute bottom-2 text-xs text-white/50">/100</span>
      </div>
      <p className="text-sm font-semibold text-white/80 text-center">{label}</p>
    </div>
  );
}

export function ScoreGauges({ validationScore, validationRationale, differentiationScore, differentiationRationale, breakdown }: Props) {
  return (
    <section className="space-y-6">
      <h2 className="text-xl font-bold text-white">Scores</h2>

      <div className="flex gap-8 justify-center py-4">
        <div className="text-center space-y-2">
          <ScoreRing
            score={validationScore}
            label="Validation Score"
            color={validationScore >= 70 ? "border-emerald-400" : validationScore >= 50 ? "border-yellow-400" : "border-red-400"}
          />
          <p className="text-xs text-white/50 max-w-[160px]">{validationRationale}</p>
        </div>
        <div className="text-center space-y-2">
          <ScoreRing
            score={differentiationScore}
            label="Differentiation Score"
            color={differentiationScore >= 70 ? "border-violet-400" : differentiationScore >= 50 ? "border-blue-400" : "border-slate-400"}
          />
          <p className="text-xs text-white/50 max-w-[160px]">{differentiationRationale}</p>
        </div>
      </div>

      {breakdown.length > 0 && (
        <div className="space-y-3">
          {breakdown.map((b) => (
            <div key={b.label} className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="text-white/70">{b.label}</span>
                <span className="text-white/50 tabular-nums">{b.score}/25</span>
              </div>
              <Progress value={(b.score / 25) * 100} className="h-1.5 bg-white/10" />
              <p className="text-xs text-white/40">{b.rationale}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
