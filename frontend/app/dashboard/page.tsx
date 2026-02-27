"use client";

import { AppShell } from "@/components/app-shell";
import { useAuthGuard } from "@/hooks/use-auth-guard";

export default function DashboardPage() {
  useAuthGuard();

  return (
    <AppShell title="Dashboard">
      <p className="text-slate-600">Overview of requisition health, hiring funnel, and team workload.</p>
    </AppShell>
  );
}
