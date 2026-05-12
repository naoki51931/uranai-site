import { redirectToPreferredLocale } from "@/lib/locale-redirect";

export default async function RegisterRedirectPage() {
  await redirectToPreferredLocale("/register");
}
