"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { apiFetch } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";

type AuthResponse = {
  access_token: string;
  token_type: string;
};

type Props = {
  locale: Locale;
  messages: Messages;
};

export function LoginPage({ locale, messages }: Props) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await apiFetch<AuthResponse>("/v1/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      localStorage.setItem("token", response.access_token);
      router.push(localizePath(locale, "/dashboard"));
    } catch (err) {
      setError(err instanceof Error ? err.message : t(messages, "login.error", "Login failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="shell">
      <div className="panel formCard">
        <h1>{t(messages, "login.title", "Log In")}</h1>
        <p>
          {t(messages, "login.no_account", "No account yet?")}{" "}
          <Link href={localizePath(locale, "/register")}>{t(messages, "login.register_link", "Create one")}</Link>
          {" / "}
          <Link href={localizePath(locale, "/admin/login")}>{t(messages, "login.admin_link", "管理ログイン")}</Link>
        </p>
        <form onSubmit={onSubmit}>
          <div className="field">
            <label htmlFor="email">{t(messages, "login.email", "Email")}</label>
            <input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </div>
          <div className="field">
            <label htmlFor="password">{t(messages, "login.password", "Password")}</label>
            <input
              id="password"
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
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
          {error ? <div className="error">{error}</div> : null}
          <button className="button" disabled={loading} type="submit">
            {loading ? t(messages, "login.loading", "Logging in...") : t(messages, "login.submit", "Go to Dashboard")}
          </button>
        </form>
      </div>
    </main>
  );
}
