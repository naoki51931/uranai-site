#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import random
import secrets
import sys
import time
from datetime import date, datetime
from pathlib import Path
from urllib import error, parse, request

PROJECT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.tarot_data import TAROT_CARDS  # noqa: E402

POST_URL = "https://api.x.com/2/tweets"
MAX_POST_LENGTH = 280

JAPANESE_CARD_NAMES = {
    "the-fool": "愚者",
    "the-magician": "魔術師",
    "the-high-priestess": "女教皇",
    "the-empress": "女帝",
    "the-emperor": "皇帝",
    "the-hierophant": "教皇",
    "the-lovers": "恋人",
    "the-chariot": "戦車",
    "strength": "力",
    "the-hermit": "隠者",
    "wheel-of-fortune": "運命の輪",
    "justice": "正義",
    "the-hanged-man": "吊るされた男",
    "death": "死神",
    "temperance": "節制",
    "the-devil": "悪魔",
    "the-tower": "塔",
    "the-star": "星",
    "the-moon": "月",
    "the-sun": "太陽",
    "judgement": "審判",
    "the-world": "世界",
}

REVERSED_CARD_MEANINGS = {
    "the-fool": "勢いだけで飛び込むより、準備不足や現実逃避を見直す段階です。",
    "the-magician": "力はあるのに焦点が散り、言葉や計画が空回りしやすい局面です。",
    "the-high-priestess": "直感と不安が混ざりやすく、秘密や思い込みを整理する必要があります。",
    "the-empress": "与えすぎや甘えが成長を鈍らせているため、境界線を整える時です。",
    "the-emperor": "支配や頑固さが強まりやすく、柔軟な運用に戻すことが課題です。",
    "the-hierophant": "常識や他人の正解に寄りすぎず、自分に合う型へ組み替える段階です。",
    "the-lovers": "気持ちと選択が一致せず、関係性や優先順位を再確認する必要があります。",
    "the-chariot": "前に進みたい気持ちに対して方向が定まらず、制御を取り戻す時です。",
    "strength": "我慢が限界に近づいているため、優しさと自己防衛のバランスが必要です。",
    "the-hermit": "内省が孤立や考えすぎに傾いており、外からの視点を少し入れる時です。",
    "wheel-of-fortune": "流れが読みにくい時期なので、無理に動かずタイミングを待つ判断が合います。",
    "justice": "事実確認や責任の線引きが曖昧で、公平さを取り戻すことが先決です。",
    "the-hanged-man": "待つ理由が見えなくなり、停滞を受け入れすぎている可能性があります。",
    "death": "終わらせるべきものに未練が残り、変化への抵抗が次の展開を遅らせています。",
    "temperance": "無理に合わせようとして調和が崩れているため、配分を見直す必要があります。",
    "the-devil": "執着の正体は見え始めていますが、手放すには具体的な距離の取り方が必要です。",
    "the-tower": "大きな崩壊を避けたいなら、小さな違和感の段階で修正することが重要です。",
    "the-star": "希望は残っていますが、期待だけで進まず回復の時間を確保する局面です。",
    "the-moon": "不安が判断を曇らせやすく、確かな情報と曖昧な想像を分ける必要があります。",
    "the-sun": "喜びや成果が見えにくくても、素直な確認と小さな成功の積み直しが効きます。",
    "judgement": "過去の評価に縛られ、今の呼びかけを聞き逃していないか見直す時です。",
    "the-world": "完成目前で詰めが甘くなりやすく、未完了の一点を仕上げる段階です。",
}

def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def percent_encode(value: str) -> str:
    return parse.quote(value, safe="~-._")


def build_oauth_header(
    method: str,
    url: str,
    api_key: str,
    api_key_secret: str,
    access_token: str,
    access_token_secret: str,
) -> str:
    oauth_params = {
        "oauth_consumer_key": api_key,
        "oauth_nonce": secrets.token_urlsafe(24),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": access_token,
        "oauth_version": "1.0",
    }
    signature_params = sorted(oauth_params.items())
    parameter_string = "&".join(
        f"{percent_encode(key)}={percent_encode(value)}" for key, value in signature_params
    )
    base_string = "&".join(
        [
            method.upper(),
            percent_encode(url),
            percent_encode(parameter_string),
        ]
    )
    signing_key = f"{percent_encode(api_key_secret)}&{percent_encode(access_token_secret)}"
    digest = hmac.new(signing_key.encode("utf-8"), base_string.encode("utf-8"), hashlib.sha1).digest()
    oauth_params["oauth_signature"] = base64.b64encode(digest).decode("ascii")

    return "OAuth " + ", ".join(
        f'{percent_encode(key)}="{percent_encode(value)}"' for key, value in sorted(oauth_params.items())
    )


def draw_daily_card(target_date: date, seed_salt: str) -> dict:
    rng = random.Random(f"{target_date.isoformat()}:{seed_salt}")
    card = rng.choice(TAROT_CARDS)
    orientation = rng.choice(["upright", "reversed"])
    meaning = card["meaning"] if orientation == "upright" else REVERSED_CARD_MEANINGS[card["slug"]]
    return {
        "slug": card["slug"],
        "name": card["name"],
        "ja_name": JAPANESE_CARD_NAMES.get(card["slug"], card["name"]),
        "orientation": orientation,
        "meaning": meaning,
    }


def build_post_text(card: dict, target_date: date, app_base_url: str) -> str:
    orientation_label = "正位置" if card["orientation"] == "upright" else "逆位置"
    lines = [
        f"{target_date.strftime('%Y/%m/%d')} 今日の一枚",
        f"{card['ja_name']}（{orientation_label}）",
        "",
        card["meaning"],
        "",
        app_base_url.rstrip("/"),
        "#今日の占い #タロット",
    ]
    text = "\n".join(lines)
    if len(text) > MAX_POST_LENGTH:
        raise ValueError(f"post text is too long: {len(text)} characters")
    return text


def post_to_x(text: str) -> dict:
    api_key = require_env("X_API_KEY")
    api_key_secret = require_env("X_API_KEY_SECRET")
    access_token = require_env("X_ACCESS_TOKEN")
    access_token_secret = require_env("X_ACCESS_TOKEN_SECRET")

    body = json.dumps({"text": text}, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": build_oauth_header(
            "POST",
            POST_URL,
            api_key,
            api_key_secret,
            access_token,
            access_token_secret,
        ),
        "Content-Type": "application/json",
    }
    req = request.Request(POST_URL, data=body, headers=headers, method="POST")

    try:
        with request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"X API returned HTTP {exc.code}: {response_body}") from exc


def require_env(key: str) -> str:
    value = os.environ.get(key, "").strip()
    if not value:
        raise RuntimeError(f"missing required environment variable: {key}")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post the daily single-card tarot draw to X.")
    parser.add_argument("--env-file", default=str(PROJECT_DIR / ".env"))
    parser.add_argument("--date", help="Target date in YYYY-MM-DD. Defaults to today.")
    parser.add_argument("--dry-run", action="store_true", help="Print the post text without posting.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_env_file(Path(args.env_file))

    target_date = (
        datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else datetime.now().date()
    )
    seed_salt = os.environ.get("X_DAILY_TAROT_SEED", "uranai-site-ai")
    app_base_url = os.environ.get("APP_BASE_URL", "http://localhost")

    card = draw_daily_card(target_date, seed_salt)
    text = build_post_text(card, target_date, app_base_url)

    if args.dry_run:
        print(text)
        return 0

    result = post_to_x(text)
    post_id = result.get("data", {}).get("id", "")
    print(f"posted to X: {post_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
