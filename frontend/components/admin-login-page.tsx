"use client";

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

export function AdminLoginPage({ locale, messages }: Props) {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await apiFetch<AuthResponse>("/v1/auth/admin/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
      localStorage.setItem("admin_token", response.access_token);
      router.push(localizePath(locale, "/admin/users"));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Admin login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="shell">
      <div className="panel formCard">
        <h1>{t(messages, "admin.login.title", "Admin Login")}</h1>
        <p className="notice">この画面はメールアドレスではなく、管理アカウント名でログインします。</p>
        <form onSubmit={onSubmit}>
          <div className="field">
            <label htmlFor="admin-username">{t(messages, "admin.login.username", "Admin Account")}</label>
            <input
              id="admin-username"
              autoCapitalize="none"
              autoCorrect="off"
              autoComplete="username"
              type="text"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
            />
          </div>
          <div className="field">
            <label htmlFor="admin-password">{t(messages, "admin.login.password", "Password")}</label>
            <input
              id="admin-password"
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
            <label className="checkboxRow" htmlFor="admin-show-password">
              <input
                id="admin-show-password"
                type="checkbox"
                checked={showPassword}
                onChange={(event) => setShowPassword(event.target.checked)}
              />
              {t(messages, "login.show_password", "Show password")}
            </label>
          </div>
          {error ? <div className="error">{error}</div> : null}
          <button className="button" disabled={loading} type="submit">
            {loading ? t(messages, "admin.login.loading", "Logging in...") : t(messages, "admin.login.submit", "Open Admin")}
          </button>
        </form>
      </div>
    </main>
  );
}
