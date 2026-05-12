from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1, max_length=255)
    locale: str = Field(default="ja", min_length=2, max_length=8, pattern="^[a-zA-Z0-9-]+$")


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    locale: str = Field(default="ja", min_length=2, max_length=8, pattern="^[a-zA-Z0-9-]+$")


class PasswordResetRequest(BaseModel):
    email: EmailStr
    locale: str = Field(default="ja", min_length=2, max_length=8, pattern="^[a-zA-Z0-9-]+$")


class PasswordResetConfirm(BaseModel):
    token: str = Field(min_length=20, max_length=255)
    password: str = Field(min_length=8, max_length=255)


class MessageResponse(BaseModel):
    message: str


class AdminLogin(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginChallengeResponse(BaseModel):
    requires_mfa: bool
    message: str
    challenge_id: str | None = None
    expires_in_seconds: int | None = None
    access_token: str | None = None
    token_type: str = "bearer"


class LoginVerifyRequest(BaseModel):
    challenge_id: str = Field(min_length=20, max_length=255)
    code: str = Field(min_length=6, max_length=6, pattern="^[0-9]{6}$")


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    free_readings_used: int
    monthly_reading_limit: int
    monthly_reading_limit_label: str
    monthly_limit_exempt: bool
    subscription_status: str
    has_paid_access: bool
    billing_enabled: bool


class ReadingRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)
    spread_name: str = Field(default="three-card", pattern="^(three-card)$")
    locale: str = Field(default="ja", min_length=2, max_length=8)


class ReadingCard(BaseModel):
    position: str
    slug: str
    name: str
    orientation: str
    keywords: list[str]
    meaning: str
    image_url: str | None = None


class ReadingResponse(BaseModel):
    id: int
    spread_name: str
    question: str
    cards: list[ReadingCard]
    interpretation: str
    created_at: datetime
    free_readings_used: int
    has_paid_access: bool


class PremiumReadingExplanationResponse(BaseModel):
    explanation: str | None = None
    cached: bool = False


class PalmReadingResponse(BaseModel):
    id: int
    model: str
    locale: str
    focus: str
    left_hand_image_url: str
    right_hand_image_url: str
    interpretation: str
    created_at: datetime


class PalmReadingRerunRequest(BaseModel):
    reading_id: int
    locale: str = Field(default="ja", min_length=2, max_length=8)
    model: str = Field(min_length=1, max_length=100)
    focus: str = Field(default="", max_length=500)


class FollowupStatusResponse(BaseModel):
    reading_id: int
    due_at: datetime
    sent_at: datetime | None = None
    responded_at: datetime | None = None


class FollowupFeedbackResponse(BaseModel):
    status: str
    learning_note: str
    llm_summary: str | None = None


class CheckoutSessionResponse(BaseModel):
    url: str


class AdminProfile(BaseModel):
    username: str


class TarotCardAdminResponse(BaseModel):
    slug: str
    name: str
    keywords: list[str]
    meaning: str
    image_url: str | None = None
    has_image: bool


class AdminDeckAssetsResponse(BaseModel):
    card_back_image_url: str | None = None
    has_card_back_image: bool


class AdminOverviewResponse(BaseModel):
    admin_username: str
    configured_cards: int
    total_cards: int
    functions: list[str]


class AdminUserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    subscription_status: str
    free_readings_used: int
    created_at: datetime


class AdminUsersResponse(BaseModel):
    total_users: int
    users: list[AdminUserResponse]
