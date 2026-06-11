interface Props {
  goToMarket: string[];
  nextSteps: string[];
}

export function NextSteps({ goToMarket, nextSteps }: Props) {
  return (
    <section className="space-y-5">
      <h2 className="text-xl font-bold text-white">Go-to-Market & Next Steps</h2>

      {goToMarket.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-2">Go-to-Market Strategy</h3>
          <ol className="space-y-2">
            {goToMarket.map((step, i) => (
              <li key={i} className="flex gap-3 text-sm text-white/70">
                <span className="shrink-0 w-6 h-6 rounded-full bg-violet-500/15 border border-violet-500/20 text-violet-300 text-xs flex items-center justify-center font-semibold">
                  {i + 1}
                </span>
                {step}
              </li>
            ))}
          </ol>
        </div>
      )}

      {nextSteps.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-white/70 mb-2">Your 30-Day Action Items</h3>
          <div className="grid gap-2">
            {nextSteps.map((step, i) => (
              <div key={i} className="flex gap-3 bg-white/5 border border-white/8 rounded-xl px-4 py-3 text-sm text-white/75">
                <span className="text-emerald-400 shrink-0">→</span> {step}
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
