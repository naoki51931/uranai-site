import type { Metadata } from "next";

import { LegalPage } from "@/components/legal-page";
import { buildLegalMetadata, getLegalPageContent } from "@/lib/compliance";
import { normalizeLocale } from "@/lib/i18n";

type Props = {
  params: Promise<{ lang: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { lang } = await params;
  return buildLegalMetadata("refund-policy", normalizeLocale(lang));
}

export default async function RefundPolicyPage({ params }: Props) {
  const { lang } = await params;
  return <LegalPage content={getLegalPageContent("refund-policy", normalizeLocale(lang))} />;
}
