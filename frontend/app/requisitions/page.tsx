"use client";

import { AppShell } from "@/components/app-shell";
import { useAuthGuard } from "@/hooks/use-auth-guard";

export default function RequisitionsPage() {
  useAuthGuard();

  return (
    <AppShell title="Requisitions">
      <p className="text-slate-600">Manage open roles, owners, priorities, and hiring stages.</p>
    </AppShell>
  );
}
