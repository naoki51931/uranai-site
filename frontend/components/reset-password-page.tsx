"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
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

export function ResetPasswordPage({ locale, messages }: Props) {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") ?? "";
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setNotice("");

    if (!token) {
      setError(t(messages, "password_reset.invalid_token", "Invalid or expired password reset link"));
      setLoading(false);
      return;
    }
    if (password !== passwordConfirmation) {
      setError(t(messages, "password_reset.password_mismatch", "Passwords do not match"));
      setLoading(false);
      return;
    }

    try {
      await apiFetch<MessageResponse>("/v1/auth/password-reset/confirm", {
        method: "POST",
        body: JSON.stringify({ token, password }),
      });
      setNotice(t(messages, "password_reset.notice", "Password has been reset. You can now log in."));
      setPassword("");
      setPasswordConfirmation("");
    } catch (err) {
      setError(err instanceof Error ? err.message : t(messages, "password_reset.error", "Password reset failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="shell">
      <div className="panel formCard">
        <h1>{t(messages, "password_reset.title", "Set New Password")}</h1>
        <p>{t(messages, "password_reset.copy", "Enter a new password for your account.")}</p>
        <form onSubmit={onSubmit}>
          <div className="field">
            <label htmlFor="password">{t(messages, "password_reset.password", "New password")}</label>
            <input
              id="password"
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              minLength={8}
            />
          </div>
          <div className="field">
            <label htmlFor="password-confirmation">
              {t(messages, "password_reset.password_confirmation", "Confirm new password")}
            </label>
            <input
              id="password-confirmation"
              type={showPassword ? "text" : "password"}
              value={passwordConfirmation}
              onChange={(event) => setPasswordConfirmation(event.target.value)}
              required
              minLength={8}
            />
            <label className="checkboxRow" htmlFor="show-password">
              <input
                id="show-password"
                type="checkbox"
                checked={showPassword}
                onChange={(event) => setShowPassword(event.target.checked)}
              />
              {t(messages, "login.show_password", "Show password")}
            </label>
          </div>
          {notice ? <div className="notice">{notice}</div> : null}
          {error ? <div className="error">{error}</div> : null}
          <button className="button" disabled={loading || Boolean(notice)} type="submit">
            {loading
              ? t(messages, "password_reset.loading", "Resetting...")
              : t(messages, "password_reset.submit", "Reset Password")}
          </button>
        </form>
        <p>
          <Link href={localizePath(locale, "/login")}>{t(messages, "password_reset.back_login", "Back to login")}</Link>
        </p>
      </div>
    </main>
  );
}
