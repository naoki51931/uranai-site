"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";
import { SocialAuthButtons } from "@/components/social-auth-buttons";

type AuthResponse = {
  requires_mfa: boolean;
  message: string;
  challenge_id?: string | null;
  expires_in_seconds?: number | null;
  access_token?: string | null;
  token_type: string;
};

type VerifyResponse = {
  access_token: string;
  token_type: string;
};

type Props = {
  locale: Locale;
  messages: Messages;
};

export function RegisterPage({ locale, messages }: Props) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [leadId, setLeadId] = useState<number | null>(null);
  const [password, setPassword] = useState("");
  const [verificationCode, setVerificationCode] = useState("");
  const [challengeId, setChallengeId] = useState<string | null>(null);
  const [challengeNotice, setChallengeNotice] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const initialEmail = searchParams.get("email");
    const initialLeadId = searchParams.get("lead_id");
    if (initialEmail) {
      setEmail(initialEmail);
    }
    if (initialLeadId && !Number.isNaN(Number(initialLeadId))) {
      setLeadId(Number(initialLeadId));
    }
  }, [searchParams]);

  const submitRegistration = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await apiFetch<AuthResponse>("/v1/auth/register", {
        method: "POST",
        body: JSON.stringify({ full_name: fullName, email, password, locale, lead_id: leadId }),
      });
      if (response.access_token) {
        localStorage.setItem("token", response.access_token);
        router.push(localizePath(locale, "/dashboard"));
        return;
      }
      setChallengeId(response.challenge_id ?? null);
      setChallengeNotice(
        response.message ||
          t(messages, "register.mfa_notice", "We sent a verification code to your email. Enter it below to complete registration."),
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : t(messages, "register.error", "Registration failed"));
    } finally {
      setLoading(false);
    }
  };

  const onSubmitRegistration = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await submitRegistration();
  };

  const onSubmitVerification = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!challengeId) {
      return;
    }
    setLoading(true);
    setError("");

    try {
      const response = await apiFetch<VerifyResponse>("/v1/auth/register/verify", {
        method: "POST",
        body: JSON.stringify({ challenge_id: challengeId, code: verificationCode, lead_id: leadId }),
      });
      localStorage.setItem("token", response.access_token);
      router.push(localizePath(locale, "/dashboard"));
    } catch (err) {
      setError(err instanceof Error ? err.message : t(messages, "register.mfa_error", "Verification failed"));
    } finally {
      setLoading(false);
    }
  };

  const resetMfaStep = () => {
    setChallengeId(null);
    setVerificationCode("");
    setChallengeNotice("");
    setError("");
  };

  return (
    <main className="shell">
      <div className="panel formCard">
        <h1>{t(messages, "register.title", "Create Account")}</h1>
        {!challengeId ? (
          <>
            <p>{t(messages, "register.copy", "Your first 10 readings are free.")}</p>
            <form onSubmit={onSubmitRegistration}>
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
            <SocialAuthButtons leadId={leadId} locale={locale} messages={messages} mode="register" />
          </>
        ) : (
          <form onSubmit={onSubmitVerification}>
            <p>
              {challengeNotice ||
                t(messages, "register.mfa_notice", "We sent a verification code to your email. Enter it below to complete registration.")}
            </p>
            <div className="field">
              <label htmlFor="verification-code">{t(messages, "register.mfa_code", "Verification code")}</label>
              <input
                id="verification-code"
                inputMode="numeric"
                maxLength={6}
                pattern="[0-9]{6}"
                type="text"
                value={verificationCode}
                onChange={(event) => setVerificationCode(event.target.value.replace(/\D/g, "").slice(0, 6))}
                required
              />
            </div>
            {error ? <div className="error">{error}</div> : null}
            <div className="ctaRow">
              <button className="button" disabled={loading || verificationCode.length !== 6} type="submit">
                {loading
                  ? t(messages, "register.mfa_loading", "Verifying...")
                  : t(messages, "register.mfa_submit", "Verify and create account")}
              </button>
              <button className="ghostButton" disabled={loading} onClick={resetMfaStep} type="button">
                {t(messages, "register.mfa_back", "Back")}
              </button>
              <button className="ghostButton" disabled={loading} onClick={() => void submitRegistration()} type="button">
                {t(messages, "register.mfa_resend", "Resend code")}
              </button>
            </div>
          </form>
        )}
      </div>
    </main>
  );
}
