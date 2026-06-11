"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { submitIdea } from "@/lib/api";
import { Sparkles, Loader2 } from "lucide-react";

const EXAMPLES = [
  "An AI platform that unifies and categorizes all UPI expenses across multiple bank accounts.",
  "A marketplace connecting independent fitness coaches with clients for live online sessions.",
  "An AI-powered legal document review tool for small businesses and freelancers.",
  "A SaaS tool that automatically converts Figma designs to production-ready React components.",
];

export function IdeaForm() {
  const router = useRouter();
  const [idea, setIdea] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!idea.trim()) return;
    setLoading(true);
    setError("");
    try {
      const project = await submitIdea(idea.trim());
      router.push(`/validate/${project.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Is the backend running?");
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full space-y-5">
      <Textarea
        value={idea}
        onChange={(e) => setIdea(e.target.value)}
        placeholder="Describe your startup idea in 1-2 sentences…"
        className="min-h-[120px] resize-none text-base bg-white/5 border-white/10 text-white placeholder:text-white/30 focus-visible:ring-violet-500/50 focus-visible:border-violet-500/50"
        disabled={loading}
      />

      {/* Example chips */}
      <div className="space-y-2">
        <p className="text-xs text-white/40 uppercase tracking-widest">Try an example</p>
        <div className="flex flex-wrap gap-2">
          {EXAMPLES.map((ex) => (
            <button
              key={ex}
              type="button"
              onClick={() => setIdea(ex)}
              className="text-xs px-3 py-1.5 rounded-full border border-white/10 bg-white/5 text-white/60 hover:bg-white/10 hover:text-white/90 transition-colors truncate max-w-[280px]"
            >
              {ex.slice(0, 55)}…
            </button>
          ))}
        </div>
      </div>

      {error && (
        <p className="text-sm text-red-400 bg-red-950/40 border border-red-500/20 rounded-lg px-4 py-2">
          {error}
        </p>
      )}

      <Button
        type="submit"
        disabled={loading || !idea.trim()}
        className="w-full h-12 text-base font-semibold bg-violet-600 hover:bg-violet-500 text-white shadow-lg shadow-violet-900/40 transition-all disabled:opacity-40"
      >
        {loading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Launching agents…
          </>
        ) : (
          <>
            <Sparkles className="mr-2 h-4 w-4" />
            Validate My Idea
          </>
        )}
      </Button>
    </form>
  );
}
