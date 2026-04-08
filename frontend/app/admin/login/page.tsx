import { redirect } from "next/navigation";

import { DEFAULT_LOCALE } from "@/lib/i18n-core";

export default function AdminLoginRedirectPage() {
  redirect(`/${DEFAULT_LOCALE}/admin/login`);
}
