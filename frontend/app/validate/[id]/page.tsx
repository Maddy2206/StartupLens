"use client";

import { use, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useEventStream, getValidation } from "@/lib/api";
import { AgentTimeline } from "@/components/agent-timeline";
import { ScoreGauges } from "@/components/report/score-gauges";
import { ExecutiveSummary } from "@/components/report/executive-summary";
import { MarketSizeSection } from "@/components/report/market-size";
import { CompetitorTable } from "@/components/report/competitor-table";
import { CommunityPainPoints } from "@/components/report/community-pain-points";
import { GapAndUVP } from "@/components/report/gap-and-uvp";
import { Personas } from "@/components/report/personas";
import { BusinessModel } from "@/components/report/business-model";
import { MvpRoadmap } from "@/components/report/mvp-roadmap";
import { Risks } from "@/components/report/risks";
import { NextSteps } from "@/components/report/next-steps";
import type { ValidationReport } from "@/lib/types";
import { ArrowLeft, Loader2 } from "lucide-react";
import { Separator } from "@/components/ui/separator";

interface Props {
  params: Promise<{ id: string }>;
}

export default function ValidatePage({ params }: Props) {
  const { id } = use(params);
  const router = useRouter();
  const { events, report: streamReport, done } = useEventStream(id);
  const [report, setReport] = useState<ValidationReport | null>(null);

  // On stream completion, use the streamed report; otherwise poll for it
  useEffect(() => {
    if (streamReport) {
      setReport(streamReport);
    }
  }, [streamReport]);

  // If stream closed but no report yet (e.g. page was refreshed), fetch from DB
  useEffect(() => {
    if (done && !report) {
      getValidation(id).then(({ report: r }) => {
        if (r) setReport(r);
      }).catch(() => {});
    }
  }, [done, report, id]);

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <div
        className="fixed inset-0 pointer-events-none opacity-[0.02]"
        style={{ backgroundImage: "linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)", backgroundSize: "60px 60px" }}
      />
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[300px] rounded-full bg-violet-700/8 blur-[120px] pointer-events-none" />

      <div className="relative max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <button
            onClick={() => router.push("/")}
            className="flex items-center gap-1.5 text-sm text-white/40 hover:text-white/70 transition-colors"
          >
            <ArrowLeft className="h-4 w-4" /> Back
          </button>
          <Separator orientation="vertical" className="h-4 bg-white/10" />
          <span className="text-sm text-white/40 font-mono truncate max-w-xs">{id}</span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[300px,1fr] gap-8">
          {/* Left: Agent timeline (sticky) */}
          <div className="lg:sticky lg:top-8 lg:self-start">
            <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-5">
              <h2 className="text-sm font-semibold text-white/70 mb-4 uppercase tracking-widest">
                Agent Pipeline
              </h2>
              <AgentTimeline events={events} done={done} />
            </div>
          </div>

          {/* Right: Report or loading state */}
          <div className="space-y-8">
            {!report && (
              <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-12 flex flex-col items-center justify-center gap-4 text-center">
                {done ? (
                  <p className="text-white/50">Report not found.</p>
                ) : (
                  <>
                    <Loader2 className="h-8 w-8 text-violet-400 animate-spin" />
                    <p className="text-white/60 text-sm">Agents are researching your idea…</p>
                    <p className="text-white/30 text-xs">This typically takes 1–3 minutes</p>
                  </>
                )}
              </div>
            )}

            {report && (
              <>
                {/* Scores — most prominent */}
                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <ScoreGauges
                    validationScore={report.validation_score}
                    validationRationale={report.validation_score_rationale}
                    differentiationScore={report.differentiation_score}
                    differentiationRationale={report.differentiation_score_rationale}
                    breakdown={report.score_breakdown}
                  />
                </div>

                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <ExecutiveSummary
                    idea={report.idea}
                    executiveSummary={report.executive_summary}
                    problemStatement={report.problem_statement}
                  />
                </div>

                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <GapAndUVP data={report.gap} />
                </div>

                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <MarketSizeSection data={report.market_research} />
                </div>

                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <CompetitorTable data={report.competitors} />
                </div>

                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <CommunityPainPoints data={report.community} />
                </div>

                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <Personas data={report.personas} />
                </div>

                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <BusinessModel data={report.business_model} />
                </div>

                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <MvpRoadmap data={report.mvp} />
                </div>

                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <Risks data={report.risks} />
                </div>

                <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-6">
                  <NextSteps
                    goToMarket={report.go_to_market}
                    nextSteps={report.next_steps}
                  />
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
