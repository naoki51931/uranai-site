from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from fastapi import HTTPException, status

from app.config import get_settings

CONTENT_TYPE = "application/json;charset=UTF-8"


@dataclass(frozen=True)
class PayPayCode:
    merchant_payment_id: str
    code_id: str | None
    url: str
    raw: dict


class PayPayClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.paypay_api_key.strip()
        self.api_secret = settings.paypay_api_secret.strip()
        self.merchant_id = settings.paypay_merchant_id.strip()
        self.merchant_alias = settings.paypay_merchant_alias.strip() or self.merchant_id
        self.base_url = settings.paypay_api_base_url.rstrip("/")

    def ensure_configured(self) -> None:
        if not self.api_key or not self.api_secret or not self.merchant_id:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="PayPay is not configured")


    def create_smart_payment_session(self, *, redirect_url: str, nonce: str) -> str:
        payload = {
            "redirectUrl": redirect_url,
            "nonce": nonce,
            "redirectType": "WEB_LINK",
            "userAgent": "chrome",
        }
        raw = self._request("POST", "/v2/smartpayment/qr/sessions", payload)
        data = raw.get("data") or {}
        login_url = data.get("loginUrl")
        if not login_url:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="PayPay did not return a Smart Payment login URL")
        return str(login_url)

    def create_code(
        self,
        *,
        merchant_payment_id: str,
        amount: int,
        description: str,
        redirect_url: str,
        requested_at: int | None = None,
    ) -> PayPayCode:
        payload = {
            "merchantPaymentId": merchant_payment_id,
            "amount": {"amount": amount, "currency": "JPY"},
            "codeType": "ORDER_QR",
            "isAuthorization": False,
            "orderDescription": description[:255],
            "requestedAt": requested_at or int(time.time()),
            "redirectUrl": redirect_url,
            "redirectType": "WEB_LINK",
        }
        raw = self._request("POST", "/v2/codes", payload)
        data = raw.get("data") or {}
        checkout_url = data.get("url") or data.get("deeplink")
        if not checkout_url:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="PayPay did not return a payment URL")
        return PayPayCode(
            merchant_payment_id=str(data.get("merchantPaymentId") or merchant_payment_id),
            code_id=data.get("codeId"),
            url=str(checkout_url),
            raw=raw,
        )

    def get_payment_details(self, merchant_payment_id: str) -> dict:
        escaped_id = quote(merchant_payment_id, safe="")
        return self._request("GET", f"/v2/codes/payments/{escaped_id}", None)

    def _request(self, method: str, path: str, payload: dict | None) -> dict:
        self.ensure_configured()
        body = None if payload is None else json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        headers = {
            "Authorization": self._authorization_header(method, path, body),
            "X-ASSUME-MERCHANT": self.merchant_id,
        }
        if body is not None:
            headers["Content-Type"] = CONTENT_TYPE
        request = Request(f"{self.base_url}{path}", data=body, headers=headers, method=method)
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace") or exc.reason
            raise HTTPException(status_code=exc.code, detail=f"PayPay API error: {detail}") from exc

    def _authorization_header(self, method: str, path: str, body: bytes | None) -> str:
        nonce = secrets.token_hex(4)
        epoch = str(int(time.time()))
        if body is None:
            content_type = "empty"
            body_hash = "empty"
        else:
            content_type = CONTENT_TYPE
            md5 = hashlib.md5()
            md5.update(content_type.encode("utf-8"))
            md5.update(body)
            body_hash = base64.b64encode(md5.digest()).decode("ascii")
        signing_target = "\n".join([path, method.upper(), nonce, epoch, content_type, body_hash]).encode("utf-8")
        mac = hmac.new(self.api_secret.encode("utf-8"), signing_target, hashlib.sha256).digest()
        mac_data = base64.b64encode(mac).decode("ascii")
        return f"hmac OPA-Auth:{self.api_key}:{mac_data}:{nonce}:{epoch}:{body_hash}"
