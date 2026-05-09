import { redirect } from "next/navigation";

import { DEFAULT_LOCALE } from "@/lib/i18n-core";

type Props = {
  searchParams: Promise<{ token?: string }>;
};

export default async function ResetPasswordRedirectPage({ searchParams }: Props) {
  const { token } = await searchParams;
  const query = token ? `?token=${encodeURIComponent(token)}` : "";
  redirect(`/${DEFAULT_LOCALE}/reset-password${query}`);
}
