"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";

type Props = {
  locale: Locale;
  messages: Messages;
};

export function OauthCallbackPage({ locale, messages }: Props) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState("");

  useEffect(() => {
    const token = searchParams.get("token");
    const oauthError = searchParams.get("error");
    if (token) {
      localStorage.setItem("token", token);
      router.replace(localizePath(locale, "/dashboard"));
      return;
    }
    if (oauthError) {
      setError(oauthError);
      return;
    }
    setError("oauth_login_failed");
  }, [locale, router, searchParams]);

  return (
    <main className="shell">
      <div className="panel formCard">
        <h1>{t(messages, "auth.callback_title", "Signing you in")}</h1>
        {error ? <p className="error">{error}</p> : <p>{t(messages, "auth.callback_copy", "Completing social login...")}</p>}
      </div>
    </main>
  );
}
