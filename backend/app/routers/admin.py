from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.deps import get_current_admin
from app.models import TarotCard, User
from app.schemas import AdminOverviewResponse, AdminUserResponse, AdminUsersResponse, TarotCardAdminResponse
from app.services.card_catalog import save_card_image, tarot_card_to_dict, tarot_sort_key


router = APIRouter(prefix="/v1/admin", tags=["admin"])


@router.get("/overview", response_model=AdminOverviewResponse)
def admin_overview(_: str = Depends(get_current_admin), db: Session = Depends(get_db)):
    total_cards = db.query(TarotCard).count()
    configured_cards = db.query(TarotCard).filter(TarotCard.image_path.is_not(None)).count()
    return AdminOverviewResponse(
        admin_username=get_settings().admin_username,
        configured_cards=configured_cards,
        total_cards=total_cards,
        functions=[
            "管理ログインを .env の ADMIN_USERNAME / ADMIN_PASSWORD で制御",
            "全カードの画像登録状況を一覧で確認",
            "各カード画像をアップロードして即時プレビュー",
            "占い画面で正位置・逆位置の向きに応じて同じ画像を回転表示",
        ],
    )


@router.get("/cards", response_model=list[TarotCardAdminResponse])
def list_cards(_: str = Depends(get_current_admin), db: Session = Depends(get_db)):
    cards = sorted(db.query(TarotCard).all(), key=tarot_sort_key)
    return [
        TarotCardAdminResponse(
            **tarot_card_to_dict(card),
            has_image=bool(card.image_path),
        )
        for card in cards
    ]


@router.get("/users", response_model=AdminUsersResponse)
def list_users(_: str = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc(), User.id.desc()).all()
    return AdminUsersResponse(
        total_users=len(users),
        users=[
            AdminUserResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                subscription_status=user.subscription_status,
                free_readings_used=user.free_readings_used,
                created_at=user.created_at,
            )
            for user in users
        ],
    )


@router.post("/cards/{slug}/image", response_model=TarotCardAdminResponse)
def upload_card_image(
    slug: str,
    image: UploadFile = File(...),
    _: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    if not (image.content_type or "").startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image file is required")

    card = db.query(TarotCard).filter(TarotCard.slug == slug).first()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")

    try:
        save_card_image(card, image)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    db.add(card)
    db.commit()
    db.refresh(card)
    return TarotCardAdminResponse(
        **tarot_card_to_dict(card),
        has_image=bool(card.image_path),
    )
