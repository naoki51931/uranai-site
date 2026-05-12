import { headers } from "next/headers";
import { redirect } from "next/navigation";

import { detectPreferredLocale, localizePath } from "@/lib/i18n-core";

export async function redirectToPreferredLocale(path = "", search = ""): Promise<never> {
  const requestHeaders = await headers();
  const locale = detectPreferredLocale(requestHeaders.get("accept-language"));
  redirect(`${localizePath(locale, path)}${search}`);
}
