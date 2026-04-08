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

export function RegisterPage({ locale, messages }: Props) {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
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
      const response = await apiFetch<AuthResponse>("/v1/auth/register", {
        method: "POST",
        body: JSON.stringify({ full_name: fullName, email, password }),
      });
      localStorage.setItem("token", response.access_token);
      router.push(localizePath(locale, "/dashboard"));
    } catch (err) {
      setError(err instanceof Error ? err.message : t(messages, "register.error", "Registration failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="shell">
      <div className="panel formCard">
        <h1>{t(messages, "register.title", "Create Account")}</h1>
        <p>{t(messages, "register.copy", "Your first 10 readings are free.")}</p>
        <form onSubmit={onSubmit}>
          <div className="field">
            <label htmlFor="name">{t(messages, "register.name", "Name")}</label>
            <input id="name" value={fullName} onChange={(event) => setFullName(event.target.value)} required />
          </div>
          <div className="field">
            <label htmlFor="email">{t(messages, "register.email", "Email")}</label>
            <input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </div>
          <div className="field">
            <label htmlFor="password">{t(messages, "register.password", "Password")}</label>
            <input
              id="password"
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
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
              {t(messages, "register.show_password", "Show password")}
            </label>
          </div>
          {error ? <div className="error">{error}</div> : null}
          <button className="button" disabled={loading} type="submit">
            {loading
              ? t(messages, "register.loading", "Creating account...")
              : t(messages, "register.submit", "Create Account")}
          </button>
        </form>
      </div>
    </main>
  );
}
