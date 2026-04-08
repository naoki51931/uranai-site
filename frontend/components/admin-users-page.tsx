"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { apiFetch } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";

type AdminProfile = {
  username: string;
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

export function AdminUsersPage({ locale, messages }: Props) {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);
  const [profile, setProfile] = useState<AdminProfile | null>(null);
  const [usersResponse, setUsersResponse] = useState<AdminUsersResponse | null>(null);
  const [error, setError] = useState("");

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
      apiFetch<AdminUsersResponse>("/v1/admin/users", undefined, token),
    ])
      .then(([profileResponse, users]) => {
        setProfile(profileResponse);
        setUsersResponse(users);
      })
      .catch((err) => {
        localStorage.removeItem("admin_token");
        setError(err instanceof Error ? err.message : "ユーザー一覧の取得に失敗しました。");
        router.push(localizePath(locale, "/admin/login"));
      });
  }, [locale, router, token]);

  const logout = () => {
    localStorage.removeItem("admin_token");
    router.push(localizePath(locale, "/admin/login"));
  };

  return (
    <main className="shell dashboard">
      <div className="nav">
        <div>
          <h1>{t(messages, "admin.users.title", "Admin Users")}</h1>
          <p>ログイン中: {profile?.username ?? "..."}</p>
        </div>
        <div className="ctaRow">
          <button className="ghostButton" onClick={() => router.push(localizePath(locale, "/admin"))} type="button">
            {t(messages, "admin.back", "Back to Admin")}
          </button>
          <button className="ghostButton" onClick={logout} type="button">
            {t(messages, "admin.logout", "Log out")}
          </button>
        </div>
      </div>

      <div className="summaryCards">
        <div className="panel summaryCard">
          <strong>{usersResponse?.total_users ?? "..."}</strong>
          <p>登録ユーザー数</p>
        </div>
        <div className="panel summaryCard">
          <strong>{usersResponse?.users.filter((user) => user.subscription_status === "active").length ?? "..."}</strong>
          <p>有効サブスクリプション</p>
        </div>
        <div className="panel summaryCard">
          <strong>{usersResponse?.users[0]?.created_at ? new Date(usersResponse.users[0].created_at).toLocaleString() : "..."}</strong>
          <p>最新登録日時</p>
        </div>
      </div>

      <section className="panel readingPanel">
        <h2>{t(messages, "admin.users.list", "Registered Users")}</h2>
        <p>現在の登録ユーザーを新しい順で表示します。</p>
        {error ? <div className="error">{error}</div> : null}
        <div className="usersList">
          {(usersResponse?.users ?? []).map((user) => (
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
    </main>
  );
}
