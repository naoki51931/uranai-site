import { redirectToPreferredLocale } from "@/lib/locale-redirect";

export default async function TranslationsRedirectPage() {
  await redirectToPreferredLocale("/translations");
}
