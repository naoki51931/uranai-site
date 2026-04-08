import { redirect } from "next/navigation";

import { DEFAULT_LOCALE } from "@/lib/i18n-core";

export default function SuccessRedirectPage() {
  redirect(`/${DEFAULT_LOCALE}/success`);
}
