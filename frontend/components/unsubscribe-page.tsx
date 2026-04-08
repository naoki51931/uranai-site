"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { ApiRequestError, apiFetch } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";

type Profile = {
  subscription_status: string;
  has_paid_access: boolean;
  billing_enabled: boolean;
};

type CheckoutResponse = {
  url: string;
};

type Props = {
  locale: Locale;
  messages: Messages;
};

export function UnsubscribePage({ locale, messages }: Props) {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (!storedToken) {
      router.push(localizePath(locale, "/login"));
      return;
    }
    setToken(storedToken);
  }, [locale, router]);

  useEffect(() => {
    if (!token) {
      return;
    }

    void apiFetch<Profile>("/v1/auth/me", undefined, token)
      .then((nextProfile) => {
        if (!nextProfile.billing_enabled) {
          router.push(localizePath(locale, "/dashboard"));
          return;
        }
        setProfile(nextProfile);
      })
      .catch(() => router.push(localizePath(locale, "/login")));
  }, [locale, router, token]);

  const openPortal = async () => {
    if (!token) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const result = await apiFetch<CheckoutResponse>("/v1/billing/portal-session", { method: "POST" }, token);
      window.location.href = result.url;
    } catch (err) {
      if (err instanceof ApiRequestError) {
        setError(err.message);
      } else {
        setError(t(messages, "unsubscribe.error", "Failed to open the cancellation page."));
      }
      setLoading(false);
    }
  };

  return (
    <main className="shell">
      <div className="panel formCard">
        <h1>{t(messages, "unsubscribe.title", "Cancel subscription")}</h1>
        <p>{t(messages, "unsubscribe.copy", "You can review your subscription and complete cancellation from the billing portal.")}</p>
        <p>
          {t(messages, "unsubscribe.status", "Current status")}: {profile?.subscription_status ?? "..."}
        </p>
        <p>
          {profile?.has_paid_access
            ? t(messages, "unsubscribe.active_hint", "Your paid plan is active. Proceed to the portal to cancel renewal.")
            : t(messages, "unsubscribe.inactive_hint", "If renewal is already stopped, you can still open the portal to confirm your billing details.")}
        </p>
        {error ? <div className="error">{error}</div> : null}
        <div className="ctaRow">
          <button className="button" disabled={loading || !profile} onClick={openPortal} type="button">
            {loading
              ? t(messages, "unsubscribe.loading", "Opening...")
              : t(messages, "unsubscribe.cta", "Open cancellation page")}
          </button>
          <Link className="ghostButton" href={localizePath(locale, "/dashboard")}>
            {t(messages, "unsubscribe.back", "Back to dashboard")}
          </Link>
        </div>
      </div>
    </main>
  );
}
