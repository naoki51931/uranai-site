import { DEFAULT_LOCALE, SUPPORTED_LOCALES, type Locale, normalizeLocale } from "@/lib/i18n-core";

export function getSiteUrl(): string {
  const raw = process.env.NEXT_PUBLIC_SITE_URL ?? process.env.APP_BASE_URL ?? "http://localhost";
  return raw.endsWith("/") ? raw.slice(0, -1) : raw;
}

export function localizedUrl(locale: string, path = ""): string {
  const normalizedLocale = normalizeLocale(locale);
  const normalizedPath = !path || path === "/" ? "" : path.startsWith("/") ? path : `/${path}`;
  return `${getSiteUrl()}/${normalizedLocale}${normalizedPath}`;
}

export function buildLanguageAlternates(path = ""): Record<string, string> {
  const alternates = Object.fromEntries(
    SUPPORTED_LOCALES.map((locale) => [locale, localizedUrl(locale, path)]),
  ) as Record<string, string>;
  alternates["x-default"] = localizedUrl(DEFAULT_LOCALE, path);
  return alternates;
}

export function getLocaleLabel(locale: Locale): string {
  const labels: Record<Locale, string> = {
    ja: "日本語",
    en: "English",
    ru: "Русский",
    de: "Deutsch",
    fr: "Français",
    it: "Italiano",
    "zh-cn": "简体中文",
    "zh-tw": "繁體中文",
    hi: "हिन्दी",
    pt: "Português",
    es: "Español",
  };
  return labels[locale];
}
