import { headers } from "next/headers";

function getServerApiBaseUrl(): string {
  const internalBaseUrl = process.env.INTERNAL_API_BASE_URL;
  if (internalBaseUrl) {
    return internalBaseUrl.endsWith("/") ? internalBaseUrl.slice(0, -1) : internalBaseUrl;
  }
  const publicApiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api";
  if (publicApiBaseUrl.startsWith("http://") || publicApiBaseUrl.startsWith("https://")) {
    return publicApiBaseUrl;
  }
  return publicApiBaseUrl;
}

export async function serverApiFetch<T>(path: string): Promise<T> {
  const requestHeaders = await headers();
  const host = requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host") ?? "localhost";
  const proto = requestHeaders.get("x-forwarded-proto") ?? "https";
  const apiBaseUrl = getServerApiBaseUrl();
  const resolvedBaseUrl = apiBaseUrl.startsWith("/")
    ? `${proto}://${host}${apiBaseUrl}`
    : apiBaseUrl;

  const response = await fetch(`${resolvedBaseUrl}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to fetch ${path}`);
  }
  return response.json() as Promise<T>;
}
