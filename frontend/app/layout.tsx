import type { Metadata } from "next";
import { Cormorant_Garamond, Manrope } from "next/font/google";

import { getSiteUrl } from "@/lib/site";

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

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body className={`${display.variable} ${body.variable}`}>{children}</body>
    </html>
  );
}
