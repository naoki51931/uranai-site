import type { MetadataRoute } from "next";

import { SUPPORTED_LOCALES } from "@/lib/i18n-core";
import { buildLanguageAlternates, localizedUrl } from "@/lib/site";

export default function sitemap(): MetadataRoute.Sitemap {
  return SUPPORTED_LOCALES.map((locale) => ({
    url: localizedUrl(locale),
    lastModified: new Date(),
    changeFrequency: "weekly",
    priority: 1,
    alternates: {
      languages: buildLanguageAlternates(),
    },
  }));
}
