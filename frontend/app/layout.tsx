import type { Metadata } from "next";
import { Cormorant_Garamond, Manrope } from "next/font/google";
import { headers } from "next/headers";
import Script from "next/script";

import { DEFAULT_LOCALE, isSupportedLocale } from "@/lib/i18n-core";
import { getSiteUrl, localeToLanguageTag } from "@/lib/site";

import "./globals.css";

const display = Cormorant_Garamond({
  variable: "--font-display",
  subsets: ["latin"],
  weight: ["500", "700"],
});

const body = Manrope({
  variable: "--font-body",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL(getSiteUrl()),
  title: "Moon Arcana",
  description: "Card-based digital entertainment with AI-generated text and online premium content",
};

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const requestHeaders = await headers();
  const currentPath = requestHeaders.get("x-current-path") ?? "/";
  const firstSegment = currentPath.split("/").filter(Boolean)[0];
  const locale = firstSegment && isSupportedLocale(firstSegment) ? firstSegment : DEFAULT_LOCALE;

  return (
    <html lang={localeToLanguageTag(locale)}>
      <body className={`${display.variable} ${body.variable}`}>
        <Script async src="https://www.googletagmanager.com/gtag/js?id=G-YJ1D3YGK3W" />
        <Script id="google-analytics">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag("js", new Date());

            gtag("config", "G-YJ1D3YGK3W");
          `}
        </Script>
        {children}
      </body>
    </html>
  );
}
