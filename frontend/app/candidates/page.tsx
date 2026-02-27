"use client";

import { AppShell } from "@/components/app-shell";
import { useAuthGuard } from "@/hooks/use-auth-guard";

export default function CandidatesPage() {
  useAuthGuard();

  return (
    <AppShell title="Candidates">
      <p className="text-slate-600">Track candidate pipeline, interviews, and feedback.</p>
    </AppShell>
  );
}
