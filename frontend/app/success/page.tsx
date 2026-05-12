import { redirectToPreferredLocale } from "@/lib/locale-redirect";

export default async function SuccessRedirectPage() {
  await redirectToPreferredLocale("/success");
}
