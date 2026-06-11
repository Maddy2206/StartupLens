import { IdeaForm } from "@/components/idea-form";
import { Sparkles, Zap, Target, TrendingUp } from "lucide-react";

const FEATURES = [
  { icon: Zap, label: "10 Specialized Agents", desc: "Market research, competitor analysis, community insights, and more" },
  { icon: Target, label: "VC-Grade Report", desc: "Executive summary, personas, business model, MVP plan, and risk analysis" },
  { icon: TrendingUp, label: "Scores & Strategy", desc: "Validation score, differentiation score, and actionable next steps" },
];

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-[#0a0a0f]">
      {/* Subtle background grid */}
      <div
        className="fixed inset-0 pointer-events-none opacity-[0.025]"
        style={{ backgroundImage: "linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)", backgroundSize: "60px 60px" }}
      />
      {/* Glow blob */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] rounded-full bg-violet-700/10 blur-[120px] pointer-events-none" />

      <main className="relative flex-1 flex flex-col items-center justify-center px-4 py-20">
        {/* Hero */}
        <div className="text-center space-y-4 mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-violet-500/25 bg-violet-500/10 text-violet-300 text-sm font-medium">
            <Sparkles className="h-3.5 w-3.5" />
            Multi-agent AI analysis
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-white max-w-2xl mx-auto leading-[1.05]">
            Validate your startup<br />
            <span className="bg-gradient-to-r from-violet-400 to-blue-400 bg-clip-text text-transparent">
              like a VC analyst
            </span>
          </h1>
          <p className="text-white/50 text-lg max-w-xl mx-auto leading-relaxed">
            Enter your idea. Our AI consulting team researches the market, finds competitor gaps, and delivers a VC-grade validation report.
          </p>
        </div>

        {/* Form card */}
        <div className="w-full max-w-2xl bg-white/[0.04] border border-white/10 rounded-2xl p-8 shadow-2xl shadow-black/40 backdrop-blur-sm">
          <IdeaForm />
        </div>

        {/* Feature pills */}
        <div className="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl w-full">
          {FEATURES.map(({ icon: Icon, label, desc }) => (
            <div key={label} className="bg-white/[0.03] border border-white/8 rounded-xl p-4 space-y-1">
              <div className="flex items-center gap-2 text-white/70 font-semibold text-sm">
                <Icon className="h-4 w-4 text-violet-400" />
                {label}
              </div>
              <p className="text-xs text-white/35 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
