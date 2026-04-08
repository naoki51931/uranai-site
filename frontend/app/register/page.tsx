import { redirect } from "next/navigation";

import { DEFAULT_LOCALE } from "@/lib/i18n-core";

export default function RegisterRedirectPage() {
  redirect(`/${DEFAULT_LOCALE}/register`);
}
