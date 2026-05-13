"use client";

import type { Locale, Messages } from "@/lib/i18n-core";
import { t } from "@/lib/i18n-core";

type Props = {
  locale: Locale;
  messages: Messages;
  mode: "login" | "register";
  leadId?: number | null;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api";

const PROVIDERS = [
  { id: "google", label: "Google" },
  { id: "line", label: "LINE" },
  { id: "apple", label: "Apple" },
] as const;

export function SocialAuthButtons({ locale, messages, mode, leadId }: Props) {
  const modeLabel = mode === "login" ? t(messages, "login.submit", "Log In") : t(messages, "register.submit", "Create Account");

  return (
    <div className="socialAuthBlock">
      <p className="socialAuthLabel">{t(messages, "auth.social_label", "Or continue with social login")}</p>
      <div className="socialAuthGrid">
        {PROVIDERS.map((provider) => {
          const params = new URLSearchParams({
            locale,
            mode,
          });
          if (leadId) {
            params.set("lead_id", String(leadId));
          }
          const href = `${API_BASE_URL}/v1/auth/oauth/${provider.id}/redirect?${params.toString()}`;
          return (
            <a className="ghostButton socialAuthButton" href={href} key={provider.id}>
              {provider.label} {modeLabel}
            </a>
          );
        })}
      </div>
    </div>
  );
}
