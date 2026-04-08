import { redirect } from "next/navigation";

import { DEFAULT_LOCALE } from "@/lib/i18n-core";

export default function LoginRedirectPage() {
  redirect(`/${DEFAULT_LOCALE}/login`);
}
