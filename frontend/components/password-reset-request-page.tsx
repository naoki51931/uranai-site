"use client";

import Link from "next/link";
import { useState } from "react";

import { apiFetch } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";

type MessageResponse = {
  message: string;
};

type Props = {
  locale: Locale;
  messages: Messages;
};

export function PasswordResetRequestPage({ locale, messages }: Props) {
  const [email, setEmail] = useState("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setNotice("");

    try {
      await apiFetch<MessageResponse>("/v1/auth/password-reset/request", {
        method: "POST",
        body: JSON.stringify({ email, locale }),
      });
      setNotice(
        t(
          messages,
          "password_reset_request.notice",
          "If the email is registered, a password reset link has been sent.",
        ),
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : t(messages, "password_reset_request.error", "Request failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="shell">
      <div className="panel formCard">
        <h1>{t(messages, "password_reset_request.title", "Reset Password")}</h1>
        <p>{t(messages, "password_reset_request.copy", "Enter your email address and we will send you a reset link.")}</p>
        <form onSubmit={onSubmit}>
          <div className="field">
            <label htmlFor="email">{t(messages, "login.email", "Email")}</label>
            <input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </div>
          {notice ? <div className="notice">{notice}</div> : null}
          {error ? <div className="error">{error}</div> : null}
          <button className="button" disabled={loading} type="submit">
            {loading
              ? t(messages, "password_reset_request.loading", "Sending...")
              : t(messages, "password_reset_request.submit", "Send Reset Link")}
          </button>
        </form>
        <p>
          <Link href={localizePath(locale, "/login")}>{t(messages, "password_reset.back_login", "Back to login")}</Link>
        </p>
      </div>
    </main>
  );
}
