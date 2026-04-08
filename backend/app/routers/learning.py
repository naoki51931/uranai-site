from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.services.learning import collect_learning_insights


router = APIRouter(prefix="/v1/learning", tags=["learning"])


@router.get("/insights")
def learning_insights(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return collect_learning_insights(db)
