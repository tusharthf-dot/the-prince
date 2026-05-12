from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import Session as SessionModel
from services.nlp_analyzer import analyze_text
from services.profile_updater import update_profile

router = APIRouter()

class TextInput(BaseModel):
    user_id: str
    situation: str
    response: str = ""

@router.post("/analyze/text")
def analyze_text_input(input: TextInput, db: Session = Depends(get_db)):
    scores = analyze_text(input.situation, input.response)

    session = SessionModel(
        user_id=input.user_id,
        input_type="text",
        raw_input=input.response,
        clarity_score=scores["clarity_score"],
        confidence_score=scores["confidence_score"],
        persuasiveness_score=scores["persuasiveness_score"],
        structure_score=scores["structure_score"],
        overall_score=scores["overall_score"],
        feedback=f"Confidence: {scores['confidence_reason']} | Persuasiveness: {scores['persuasiveness_reason']}"
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    profile = update_profile(db, input.user_id, scores)

    return {
        "session_id": session.id,
        "scores": scores,
        "profile": {
            "total_sessions": profile.total_sessions,
            "avg_clarity": round(profile.avg_clarity, 2),
            "avg_confidence": round(profile.avg_confidence, 2),
            "avg_persuasiveness": round(profile.avg_persuasiveness, 2),
            "weak_areas": profile.weak_areas,
            "improvement_rate": round(profile.improvement_rate, 2)
        },
        "message": "Analysis complete"
    }