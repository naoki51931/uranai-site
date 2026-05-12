import { redirectToPreferredLocale } from "@/lib/locale-redirect";

export default async function AdminUsersRedirectPage() {
  await redirectToPreferredLocale("/admin/users");
}
