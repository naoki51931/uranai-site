import { redirect } from "next/navigation";

import { DEFAULT_LOCALE } from "@/lib/i18n-core";

export default function PasswordResetRedirectPage() {
  redirect(`/${DEFAULT_LOCALE}/password-reset`);
}
