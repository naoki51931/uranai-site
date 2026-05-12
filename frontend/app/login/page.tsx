import { redirectToPreferredLocale } from "@/lib/locale-redirect";

export default async function LoginRedirectPage() {
  await redirectToPreferredLocale("/login");
}
