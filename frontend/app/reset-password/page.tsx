import { redirectToPreferredLocale } from "@/lib/locale-redirect";

type Props = {
  searchParams: Promise<{ token?: string }>;
};

export default async function ResetPasswordRedirectPage({ searchParams }: Props) {
  const { token } = await searchParams;
  const query = token ? `?token=${encodeURIComponent(token)}` : "";
  await redirectToPreferredLocale("/reset-password", query);
}
