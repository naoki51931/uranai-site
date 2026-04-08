"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { apiFetch } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";

type AdminProfile = {
  username: string;
};

type AdminOverview = {
  admin_username: string;
  configured_cards: number;
  total_cards: number;
  functions: string[];
};

type AdminCard = {
  slug: string;
  name: string;
  keywords: string[];
  meaning: string;
  image_url: string | null;
  has_image: boolean;
};

type AdminUser = {
  id: number;
  email: string;
  full_name: string;
  subscription_status: string;
  free_readings_used: number;
  created_at: string;
};

type AdminUsersResponse = {
  total_users: number;
  users: AdminUser[];
};

type Props = {
  locale: Locale;
  messages: Messages;
};

export function AdminPage({ locale, messages }: Props) {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);
  const [profile, setProfile] = useState<AdminProfile | null>(null);
  const [overview, setOverview] = useState<AdminOverview | null>(null);
  const [cards, setCards] = useState<AdminCard[]>([]);
  const [usersResponse, setUsersResponse] = useState<AdminUsersResponse | null>(null);
  const [pendingFiles, setPendingFiles] = useState<Record<string, File | null>>({});
  const [uploadingSlug, setUploadingSlug] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  useEffect(() => {
    const storedToken = localStorage.getItem("admin_token");
    if (!storedToken) {
      router.push(localizePath(locale, "/admin/login"));
      return;
    }
    setToken(storedToken);
  }, [locale, router]);

  useEffect(() => {
    if (!token) {
      return;
    }

    void Promise.all([
      apiFetch<AdminProfile>("/v1/auth/admin/me", undefined, token),
      apiFetch<AdminOverview>("/v1/admin/overview", undefined, token),
      apiFetch<AdminCard[]>("/v1/admin/cards", undefined, token),
      apiFetch<AdminUsersResponse>("/v1/admin/users", undefined, token),
    ])
      .then(([profileResponse, overviewResponse, cardsResponse, users]) => {
        setProfile(profileResponse);
        setOverview(overviewResponse);
        setCards(cardsResponse);
        setUsersResponse(users);
      })
      .catch(() => {
        localStorage.removeItem("admin_token");
        router.push(localizePath(locale, "/admin/login"));
      });
  }, [locale, router, token]);

  const refreshCards = async () => {
    if (!token) {
      return;
    }
    const [overviewResponse, cardsResponse, users] = await Promise.all([
      apiFetch<AdminOverview>("/v1/admin/overview", undefined, token),
      apiFetch<AdminCard[]>("/v1/admin/cards", undefined, token),
      apiFetch<AdminUsersResponse>("/v1/admin/users", undefined, token),
    ]);
    setOverview(overviewResponse);
    setCards(cardsResponse);
    setUsersResponse(users);
  };

  const uploadImage = async (slug: string) => {
    if (!token) {
      return;
    }
    const file = pendingFiles[slug];
    if (!file) {
      setError("アップロードする画像を選択してください。");
      return;
    }

    setUploadingSlug(slug);
    setError("");
    setNotice("");

    const formData = new FormData();
    formData.append("image", file);

    try {
      await apiFetch<AdminCard>(
        `/v1/admin/cards/${slug}/image`,
        {
          method: "POST",
          body: formData,
        },
        token,
      );
      setPendingFiles((current) => ({ ...current, [slug]: null }));
      await refreshCards();
      setNotice("カード画像を更新しました。占い画面でもこの画像が使われます。");
    } catch (err) {
      setError(err instanceof Error ? err.message : "画像の登録に失敗しました。");
    } finally {
      setUploadingSlug(null);
    }
  };

  const logout = () => {
    localStorage.removeItem("admin_token");
    router.push(localizePath(locale, "/admin/login"));
  };

  return (
    <main className="shell dashboard">
      <div className="nav">
        <div>
          <h1>{t(messages, "admin.title", "Admin Dashboard")}</h1>
          <p>ログイン中: {profile?.username ?? overview?.admin_username ?? "..."}</p>
        </div>
        <div className="ctaRow">
          <button className="ghostButton" onClick={() => router.push(localizePath(locale, "/admin/users"))} type="button">
            ユーザー一覧
          </button>
          <button className="ghostButton" onClick={() => router.push(localizePath(locale, "/dashboard"))} type="button">
            {t(messages, "admin.to_user", "User Dashboard")}
          </button>
          <button className="ghostButton" onClick={logout} type="button">
            {t(messages, "admin.logout", "Log out")}
          </button>
        </div>
      </div>

      <div className="summaryCards">
        <div className="panel summaryCard">
          <strong>{overview ? `${overview.configured_cards} / ${overview.total_cards}` : "..."}</strong>
          <p>画像登録済みカード</p>
        </div>
        <div className="panel summaryCard">
          <strong>{usersResponse?.total_users ?? "..."}</strong>
          <p>登録ユーザー数</p>
        </div>
        <div className="panel summaryCard">
          <strong>{overview?.admin_username ?? "..."}</strong>
          <p>.env で管理する管理者アカウント</p>
        </div>
      </div>

      <section className="panel readingPanel">
        <h2>{t(messages, "admin.functions", "Management Functions")}</h2>
        <div className="adminFeatureGrid">
          {(overview?.functions ?? []).map((item) => (
            <div className="adminFeatureItem" key={item}>
              <strong>{item}</strong>
            </div>
          ))}
        </div>
        <p className="adminRule">
          表示ルール: 正位置はそのまま表示、逆位置は同じ画像を回転して表示します。別画像を管理する必要はありません。
        </p>
      </section>

      <section className="panel readingPanel">
        <div className="nav">
          <div>
            <h2>{t(messages, "admin.users.list", "Registered Users")}</h2>
            <p>管理トップから最新ユーザーを確認できます。</p>
          </div>
          <button className="ghostButton" onClick={() => router.push(localizePath(locale, "/admin/users"))} type="button">
            ユーザー一覧ページ
          </button>
        </div>
        <div className="usersList">
          {(usersResponse?.users ?? []).slice(0, 5).map((user) => (
            <article className="userListItem" key={user.id}>
              <div className="userListHeader">
                <strong>{user.full_name}</strong>
                <span>#{user.id}</span>
              </div>
              <p>{user.email}</p>
              <div className="userMetaRow">
                <span>Subscription: {user.subscription_status}</span>
                <span>Free readings used: {user.free_readings_used}</span>
                <span>Created: {new Date(user.created_at).toLocaleString()}</span>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="panel readingPanel">
        <h2>{t(messages, "admin.cards", "Card Artwork Registration")}</h2>
        <p>各カードごとに画像を登録できます。推奨形式は `png`, `jpg`, `webp`, `gif` です。</p>
        {error ? <div className="error">{error}</div> : null}
        {notice ? <div className="notice">{notice}</div> : null}
        <div className="adminCardGrid">
          {cards.map((card) => (
            <article className="adminCardItem" key={card.slug}>
              <div className="adminCardPreview">
                {card.image_url ? (
                  <img alt={card.name} className="adminCardImage" src={card.image_url} />
                ) : (
                  <div className="adminCardPlaceholder">No image</div>
                )}
              </div>
              <div className="adminCardBody">
                <strong>{card.name}</strong>
                <p>{card.keywords.join(" / ")}</p>
                <p>{card.meaning}</p>
                <div className="adminUploadActions">
                  <input
                    accept="image/png,image/jpeg,image/webp,image/gif"
                    onChange={(event) =>
                      setPendingFiles((current) => ({
                        ...current,
                        [card.slug]: event.target.files?.[0] ?? null,
                      }))
                    }
                    type="file"
                  />
                  <button
                    className="button"
                    disabled={uploadingSlug === card.slug || !pendingFiles[card.slug]}
                    onClick={() => void uploadImage(card.slug)}
                    type="button"
                  >
                    {uploadingSlug === card.slug ? "Uploading..." : card.has_image ? "画像を更新" : "画像を登録"}
                  </button>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
