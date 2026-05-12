import { redirectToPreferredLocale } from "@/lib/locale-redirect";

export default async function AdminLoginRedirectPage() {
  await redirectToPreferredLocale("/admin/login");
}
