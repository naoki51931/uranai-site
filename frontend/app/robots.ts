import type { MetadataRoute } from "next";

import { getSiteUrl } from "@/lib/site";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "Mediapartners-Google",
        allow: "/",
      },
      {
        userAgent: "*",
        allow: "/",
        disallow: [
          "/admin",
          "/admin/login",
          "/dashboard",
          "/login",
          "/register",
          "/success",
          "/translations",
          "/*/admin",
          "/*/admin/login",
          "/*/dashboard",
          "/*/login",
          "/*/register",
          "/*/success",
          "/*/translations",
        ],
      },
    ],
    sitemap: `${getSiteUrl()}/sitemap.xml`,
  };
}
