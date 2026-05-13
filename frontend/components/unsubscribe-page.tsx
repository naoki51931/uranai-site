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
  daily_lucky_opt_in: boolean;
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
  const [notificationSaving, setNotificationSaving] = useState(false);

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

  const updateDailyNotificationPreference = async (nextValue: boolean) => {
    if (!token) {
      return;
    }
    setNotificationSaving(true);
    setError("");
    try {
      const nextProfile = await apiFetch<Profile>(
        "/v1/auth/notification-preferences",
        {
          method: "PATCH",
          body: JSON.stringify({ daily_lucky_opt_in: nextValue }),
        },
        token,
      );
      setProfile(nextProfile);
    } catch (err) {
      setError(err instanceof Error ? err.message : t(messages, "unsubscribe.error", "Failed to update daily delivery setting."));
    } finally {
      setNotificationSaving(false);
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
        <div className="notificationPreferenceBox">
          <strong>{t(messages, "unsubscribe.notifications_title", "Daily lucky action email")}</strong>
          <p>
            {t(
              messages,
              "unsubscribe.notifications_copy",
              "You can stop the daily lucky action email here without canceling your paid plan.",
            )}
          </p>
          <label className="checkboxRow" htmlFor="unsubscribe-daily-lucky-opt-in">
            <input
              checked={Boolean(profile?.daily_lucky_opt_in)}
              disabled={!profile || notificationSaving}
              id="unsubscribe-daily-lucky-opt-in"
              onChange={(event) => void updateDailyNotificationPreference(event.target.checked)}
              type="checkbox"
            />
            {profile?.daily_lucky_opt_in
              ? t(messages, "unsubscribe.notifications_on", "Daily lucky action email is enabled")
              : t(messages, "unsubscribe.notifications_off", "Daily lucky action email is disabled")}
          </label>
        </div>
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
