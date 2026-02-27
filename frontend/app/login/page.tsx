"use client";

import { Button } from "@/components/ui/button";

export default function LoginPage() {
  return (
    <div className="mx-auto mt-20 max-w-sm rounded-lg border p-6">
      <h1 className="mb-4 text-2xl font-semibold">Sign in</h1>
      <p className="mb-6 text-sm text-slate-600">Use your corporate credentials to continue.</p>
      <Button
        onClick={() => {
          document.cookie = "access_token=demo-token; path=/";
          localStorage.setItem("access_token", "demo-token");
          window.location.href = "/dashboard";
        }}
        className="w-full"
      >
        Continue
      </Button>
    </div>
  );
}
