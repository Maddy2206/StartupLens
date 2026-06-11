interface Props {
  idea: string;
  executiveSummary: string;
  problemStatement: string;
}

export function ExecutiveSummary({ idea, executiveSummary, problemStatement }: Props) {
  return (
    <section className="space-y-4">
      <div className="inline-block px-3 py-1 rounded-full bg-violet-500/15 border border-violet-500/25 text-violet-300 text-xs font-semibold tracking-wide uppercase">
        Executive Summary
      </div>
      <blockquote className="border-l-2 border-violet-500/40 pl-4 text-white/80 text-base italic leading-relaxed">
        "{idea}"
      </blockquote>
      <p className="text-white/80 text-sm leading-relaxed">{executiveSummary}</p>
      <div className="bg-white/5 rounded-xl p-4 border border-white/8">
        <h3 className="text-xs uppercase tracking-widest text-white/40 mb-2">Problem Statement</h3>
        <p className="text-white/75 text-sm leading-relaxed">{problemStatement}</p>
      </div>
    </section>
  );
}
