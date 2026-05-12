import { redirectToPreferredLocale } from "@/lib/locale-redirect";

export default async function UnsubscribeRedirectPage() {
  await redirectToPreferredLocale("/unsubscribe");
}
