"use client";

import { cn } from "@/lib/utils";
import { AGENT_LABELS, AGENT_ORDER, type SSEEvent } from "@/lib/types";
import { CheckCircle2, Circle, Loader2, XCircle } from "lucide-react";

type AgentStatus = "pending" | "running" | "completed" | "failed";

function deriveStatuses(events: SSEEvent[]): Record<string, AgentStatus> {
  const statuses: Record<string, AgentStatus> = {};
  for (const ev of events) {
    if (!ev.agent) continue;
    if (ev.event === "agent_started") statuses[ev.agent] = "running";
    if (ev.event === "agent_completed") statuses[ev.agent] = "completed";
    if (ev.event === "agent_failed") statuses[ev.agent] = "failed";
  }
  return statuses;
}

interface Props {
  events: SSEEvent[];
  done: boolean;
}

export function AgentTimeline({ events, done }: Props) {
  const statuses = deriveStatuses(events);

  return (
    <div className="space-y-1">
      {AGENT_ORDER.map((key, i) => {
        const status = statuses[key] ?? "pending";
        const label = AGENT_LABELS[key];

        return (
          <div
            key={key}
            className={cn(
              "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300",
              status === "running" && "bg-violet-500/10 border border-violet-500/20",
              status === "completed" && "bg-emerald-500/5 border border-emerald-500/10",
              status === "failed" && "bg-red-500/5 border border-red-500/10",
              status === "pending" && "border border-transparent opacity-40",
            )}
          >
            {/* Icon */}
            <span className="shrink-0">
              {status === "pending" && <Circle className="h-4 w-4 text-white/30" />}
              {status === "running" && <Loader2 className="h-4 w-4 text-violet-400 animate-spin" />}
              {status === "completed" && <CheckCircle2 className="h-4 w-4 text-emerald-400" />}
              {status === "failed" && <XCircle className="h-4 w-4 text-red-400" />}
            </span>

            {/* Label */}
            <span
              className={cn(
                "text-sm font-medium",
                status === "running" && "text-violet-300",
                status === "completed" && "text-emerald-300",
                status === "failed" && "text-red-300",
                status === "pending" && "text-white/40",
              )}
            >
              {label}
            </span>

            {/* Step number badge */}
            <span className="ml-auto text-xs text-white/20 tabular-nums">{i + 1}</span>
          </div>
        );
      })}

      {done && (
        <div className="mt-4 px-4 py-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-sm text-emerald-300 font-medium text-center">
          Analysis complete ✓
        </div>
      )}
    </div>
  );
}
