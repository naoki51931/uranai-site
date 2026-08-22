"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";

type Props = {
  locale: Locale;
  messages: Messages;
};

type PaymentStatusResponse = {
  payment_id: string;
  status: string;
  has_paid_access: boolean;
};

export function SuccessPage({ locale, messages }: Props) {
  const searchParams = useSearchParams();
  const paymentId = searchParams.get("payment_id");
  const [status, setStatus] = useState<string>(paymentId ? "checking" : "idle");

  useEffect(() => {
    if (!paymentId) {
      return;
    }
    const token = localStorage.getItem("token");
    if (!token) {
      setStatus("idle");
      return;
    }

    apiFetch<PaymentStatusResponse>(`/v1/billing/payments/${encodeURIComponent(paymentId)}`, undefined, token)
      .then((result) => setStatus(result.has_paid_access ? "active" : result.status))
      .catch(() => setStatus("idle"));
  }, [paymentId]);

  const copy =
    status === "checking"
      ? t(messages, "success.checking", "Checking payment status...")
      : status === "active"
        ? t(messages, "success.active", "Payment confirmed. You can return to the dashboard and continue.")
        : t(messages, "success.copy", "You can return to the dashboard and continue.");

  return (
    <main className="shell">
      <div className="panel formCard">
        <h1>{t(messages, "success.title", "Done")}</h1>
        <p>{copy}</p>
        <Link className="button" href={localizePath(locale, "/dashboard")}>
          {t(messages, "success.back", "Back to Dashboard")}
        </Link>
      </div>
    </main>
  );
}
