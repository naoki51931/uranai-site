import { redirectToPreferredLocale } from "@/lib/locale-redirect";

export default async function AdminRedirectPage() {
  await redirectToPreferredLocale("/admin");
}
