import { headers } from "next/headers";

import { DEFAULT_LOCALE, type Locale, type Messages, normalizeLocale } from "@/lib/i18n-core";

type MessagesResponse = {
  locale: string;
  messages: Messages;
};

function getServerApiBaseUrl(): string | null {
  const internalBaseUrl = process.env.INTERNAL_API_BASE_URL;
  if (internalBaseUrl) {
    return internalBaseUrl.endsWith("/") ? internalBaseUrl.slice(0, -1) : internalBaseUrl;
  }
  return null;
}

function getApiBaseUrl(host: string | null, proto: string | null) {
  const serverApiBaseUrl = getServerApiBaseUrl();
  if (serverApiBaseUrl) {
    return serverApiBaseUrl;
  }
  const configuredBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api";
  if (configuredBaseUrl.startsWith("http://") || configuredBaseUrl.startsWith("https://")) {
    return configuredBaseUrl;
  }
  const resolvedHost = host ?? "localhost";
  const resolvedProto = proto ?? "http";
  return `${resolvedProto}://${resolvedHost}${configuredBaseUrl}`;
}

export async function getMessages(locale: string): Promise<{ locale: Locale; messages: Messages }> {
  const normalizedLocale = normalizeLocale(locale);
  const requestHeaders = await headers();
  const host = requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host");
  const proto = requestHeaders.get("x-forwarded-proto");
  const apiBaseUrl = getApiBaseUrl(host, proto);

  try {
    const response = await fetch(`${apiBaseUrl}/v1/i18n/messages/${normalizedLocale}`, {
      cache: "no-store",
    });
    if (!response.ok) {
      throw new Error(`Failed to load messages for ${normalizedLocale}`);
    }

    const payload = (await response.json()) as MessagesResponse;
    return {
      locale: normalizeLocale(payload.locale),
      messages: payload.messages,
    };
  } catch {
    return { locale: DEFAULT_LOCALE, messages: {} };
  }
}

export { normalizeLocale } from "@/lib/i18n-core";
