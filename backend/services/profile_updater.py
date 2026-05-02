from sqlalchemy.orm import Session
from models.user import UserProfile, Session as SessionModel
import json

def update_profile(db: Session, user_id: str, new_scores: dict):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if not profile:
        profile = UserProfile(
            user_id=user_id,
            total_sessions=0,
            avg_clarity=0.0,
            avg_confidence=0.0,
            avg_persuasiveness=0.0,
            weak_areas="[]",
            improvement_rate=0.0
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # Update running averages
    n = profile.total_sessions
    profile.avg_clarity = ((profile.avg_clarity * n) + new_scores["clarity_score"]) / (n + 1)
    profile.avg_confidence = ((profile.avg_confidence * n) + new_scores["confidence_score"]) / (n + 1)
    profile.avg_persuasiveness = ((profile.avg_persuasiveness * n) + new_scores["persuasiveness_score"]) / (n + 1)
    profile.total_sessions = n + 1

    # Detect weak areas
    weak = []
    if profile.avg_clarity < 5:
        weak.append("clarity")
    if profile.avg_confidence < 4:
        weak.append("confidence")
    if profile.avg_persuasiveness < 4:
        weak.append("persuasiveness")
    profile.weak_areas = json.dumps(weak)

    # Calculate improvement rate
    all_sessions = db.query(SessionModel).filter(
        SessionModel.user_id == user_id
    ).order_by(SessionModel.created_at).all()

    if len(all_sessions) >= 2:
        first_score = all_sessions[0].overall_score
        latest_score = all_sessions[-1].overall_score
        if first_score > 0:
            profile.improvement_rate = ((latest_score - first_score) / first_score) * 100

    db.commit()
    db.refresh(profile)
    return profile