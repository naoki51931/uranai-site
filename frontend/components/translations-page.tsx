"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { apiFetch } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, SUPPORTED_LOCALES, t } from "@/lib/i18n-core";

type LocaleResponse = {
  default_locale: string;
  supported_locales: string[];
};

type MessagesResponse = {
  locale: string;
  messages: Record<string, string>;
};

type Props = {
  locale: Locale;
  messages: Messages;
};

export function TranslationsPage({ locale, messages }: Props) {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);
  const [availableLocales, setAvailableLocales] = useState<string[]>([...SUPPORTED_LOCALES]);
  const [selectedLocale, setSelectedLocale] = useState(locale);
  const [reloadToken, setReloadToken] = useState(0);
  const [entries, setEntries] = useState<Array<[string, string]>>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (!storedToken) {
      router.push(localizePath(locale, "/login"));
      return;
    }
    setToken(storedToken);
  }, [locale, router]);

  useEffect(() => {
    void apiFetch<LocaleResponse>("/v1/i18n/locales")
      .then((response) => setAvailableLocales(response.supported_locales))
      .catch(() => setAvailableLocales([...SUPPORTED_LOCALES]));
  }, []);

  useEffect(() => {
    setLoading(true);
    setError("");
    setNotice("");

    void apiFetch<MessagesResponse>(`/v1/i18n/messages/${selectedLocale}`)
      .then((response) => {
        const sortedEntries = Object.entries(response.messages).sort(([left], [right]) => left.localeCompare(right));
        setEntries(sortedEntries);
      })
      .catch((err) => setError(err instanceof Error ? err.message : t(messages, "translations.error", "Failed to load translations")))
      .finally(() => setLoading(false));
  }, [messages, reloadToken, selectedLocale]);

  const updateValue = (key: string, value: string) => {
    setEntries((current) => current.map((entry) => (entry[0] === key ? [key, value] : entry)));
  };

  const saveMessages = async () => {
    if (!token) {
      router.push(localizePath(locale, "/login"));
      return;
    }
    setSaving(true);
    setError("");
    setNotice("");

    try {
      await apiFetch<{ updated: number }>(
        `/v1/i18n/messages/${selectedLocale}`,
        {
          method: "PUT",
          body: JSON.stringify({ values: Object.fromEntries(entries) }),
        },
        token,
      );
      setNotice(t(messages, "translations.saved", "Translations saved."));
    } catch (err) {
      setError(err instanceof Error ? err.message : t(messages, "translations.save_error", "Failed to save translations"));
    } finally {
      setSaving(false);
    }
  };

  return (
    <main className="shell dashboard">
      <div className="nav">
        <div>
          <h1>{t(messages, "translations.title", "Translation Manager")}</h1>
          <p>{t(messages, "translations.copy", "Edit locale text stored in MySQL and save it back through the API.")}</p>
        </div>
        <button className="ghostButton" onClick={() => router.push(localizePath(locale, "/dashboard"))} type="button">
          {t(messages, "translations.back", "Back to Dashboard")}
        </button>
      </div>

      <div className="panel readingPanel">
        <div className="translationsToolbar">
          <label className="field translationsLocaleField" htmlFor="translation-locale">
            <span>{t(messages, "translations.locale", "Locale")}</span>
            <select
              id="translation-locale"
              value={selectedLocale}
              onChange={(event) => setSelectedLocale(event.target.value as Locale)}
            >
              {availableLocales.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>
          <div className="ctaRow">
            <button className="ghostButton" disabled={loading} onClick={() => setReloadToken((current) => current + 1)} type="button">
              {t(messages, "translations.refresh", "Refresh")}
            </button>
            <button className="button" disabled={saving || loading} onClick={saveMessages} type="button">
              {saving ? t(messages, "translations.saving", "Saving...") : t(messages, "translations.save", "Save")}
            </button>
          </div>
        </div>

        {error ? <div className="error">{error}</div> : null}
        {notice ? <div className="notice">{notice}</div> : null}

        {loading ? (
          <p>{t(messages, "translations.loading", "Loading translations...")}</p>
        ) : entries.length === 0 ? (
          <p>{t(messages, "translations.empty", "No translations found for this locale.")}</p>
        ) : (
          <div className="translationsList">
            {entries.map(([key, value]) => (
              <label className="field translationsField" key={key}>
                <span className="translationKey">{key}</span>
                <textarea rows={3} value={value} onChange={(event) => updateValue(key, event.target.value)} />
              </label>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
