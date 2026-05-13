"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { t } from "@/lib/i18n-core";

type ActivityFeedItem = {
  id: number;
  message: string;
  card_name: string;
  created_at: string;
};

type Props = {
  locale: Locale;
  messages: Messages;
};

export function ActivityFeed({ locale, messages }: Props) {
  const [items, setItems] = useState<ActivityFeedItem[]>([]);

  useEffect(() => {
    void apiFetch<ActivityFeedItem[]>(`/v1/readings/activity-feed?locale=${encodeURIComponent(locale)}`)
      .then(setItems)
      .catch(() => undefined);
  }, [locale]);

  if (items.length === 0) {
    return null;
  }

  return (
    <section className="panel activityPanel">
      <div className="eyebrow">{t(messages, "activity.eyebrow", "Social Proof")}</div>
      <h2>{t(messages, "activity.title", "いま動いている鑑定の流れ")}</h2>
      <div className="activityList">
        {items.map((item) => (
          <div className="activityItem" key={item.id}>
            <strong>{item.card_name}</strong>
            <p>{item.message}</p>
            <span>
              {new Date(item.created_at).toLocaleTimeString(locale, {
                hour: "2-digit",
                minute: "2-digit",
                hour12: false,
              })}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
