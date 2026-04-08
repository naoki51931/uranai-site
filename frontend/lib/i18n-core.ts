export const SUPPORTED_LOCALES = ["ja", "en", "ru", "de", "fr", "it"] as const;
export const DEFAULT_LOCALE = "ja";

export type Locale = (typeof SUPPORTED_LOCALES)[number];
export type Messages = Record<string, string>;

export function isSupportedLocale(locale: string): locale is Locale {
  return SUPPORTED_LOCALES.includes(locale as Locale);
}

export function normalizeLocale(locale: string): Locale {
  return isSupportedLocale(locale) ? locale : DEFAULT_LOCALE;
}

export function t(messages: Messages, key: string, fallback: string): string {
  return messages[key] ?? fallback;
}

export function localizePath(locale: string, path = ""): string {
  const normalizedLocale = normalizeLocale(locale);
  if (!path || path === "/") {
    return `/${normalizedLocale}`;
  }
  return `/${normalizedLocale}${path.startsWith("/") ? path : `/${path}`}`;
}

export function detectPreferredLocale(acceptLanguage: string | null | undefined): Locale {
  if (!acceptLanguage) {
    return DEFAULT_LOCALE;
  }

  const parsed = acceptLanguage
    .split(",")
    .map((entry) => {
      const [rawTag, ...params] = entry.trim().split(";");
      const qParam = params.find((param) => param.trim().startsWith("q="));
      const quality = qParam ? Number.parseFloat(qParam.trim().slice(2)) : 1;
      return {
        tag: rawTag.toLowerCase(),
        quality: Number.isFinite(quality) ? quality : 0,
      };
    })
    .sort((left, right) => right.quality - left.quality);

  for (const candidate of parsed) {
    const primaryTag = candidate.tag.split("-")[0];
    if (isSupportedLocale(candidate.tag)) {
      return candidate.tag;
    }
    if (isSupportedLocale(primaryTag)) {
      return primaryTag;
    }
  }

  return DEFAULT_LOCALE;
}
