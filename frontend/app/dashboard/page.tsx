import { redirectToPreferredLocale } from "@/lib/locale-redirect";

export default async function DashboardRedirectPage() {
  await redirectToPreferredLocale("/dashboard");
}
