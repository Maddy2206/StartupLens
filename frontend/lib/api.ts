import { useEffect, useRef, useState, useCallback } from "react";
import type { ProjectResponse, SSEEvent, ValidationReport } from "./types";

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function submitIdea(idea: string): Promise<ProjectResponse> {
  const res = await fetch(`${BASE}/api/validate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ idea }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `Request failed: ${res.status}`);
  }
  return res.json();
}

export async function getValidation(id: string): Promise<{ project: ProjectResponse; report: ValidationReport | null }> {
  const res = await fetch(`${BASE}/api/validate/${id}`);
  if (!res.ok) throw new Error(`Not found: ${res.status}`);
  return res.json();
}

export async function listValidations(): Promise<{ projects: ProjectResponse[] }> {
  const res = await fetch(`${BASE}/api/validate`);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

export function useEventStream(runId: string | null) {
  const [events, setEvents] = useState<SSEEvent[]>([]);
  const [report, setReport] = useState<ValidationReport | null>(null);
  const [done, setDone] = useState(false);
  const esRef = useRef<EventSource | null>(null);

  const reset = useCallback(() => {
    setEvents([]);
    setReport(null);
    setDone(false);
  }, []);

  useEffect(() => {
    if (!runId) return;
    reset();

    const es = new EventSource(`${BASE}/api/validate/${runId}/stream`);
    esRef.current = es;

    es.onmessage = (e) => {
      try {
        const ev: SSEEvent = JSON.parse(e.data);
        if (ev.event === "keepalive") return;

        setEvents((prev) => [...prev, ev]);

        if (ev.event === "run_completed") {
          if (ev.data) setReport(ev.data as ValidationReport);
          setDone(true);
          es.close();
        }
        if (ev.event === "error" || ev.event === "run_not_found") {
          setDone(true);
          es.close();
        }
      } catch {
        // ignore malformed frames
      }
    };

    es.onerror = () => {
      setDone(true);
      es.close();
    };

    return () => es.close();
  }, [runId, reset]);

  return { events, report, done };
}
