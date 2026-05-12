import { redirectToPreferredLocale } from "@/lib/locale-redirect";

export default async function PasswordResetRedirectPage() {
  await redirectToPreferredLocale("/password-reset");
}
