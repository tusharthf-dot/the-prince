from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from groq import Groq
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from rag.rag_pipeline import retrieve_principles

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
router = APIRouter()

class SocraticInput(BaseModel):
    user_id: str
    situation: str
    user_answers: list[str] = []

@router.post("/socratic/start")
def start_socratic(input: SocraticInput, db: Session = Depends(get_db)):
    principles = retrieve_principles(input.situation, k=2)
    principles_text = "\n".join(principles)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a Machiavellian coach who uses the Socratic method. 
                Given a situation, ask 2 deep questions that make the person reflect on:
                1. What they actually wanted from the situation
                2. What their communication revealed about their mindset
                
                Return ONLY a JSON object:
                {
                    "questions": ["question1", "question2"],
                    "context": "one line about what Machiavelli would observe about this situation"
                }
                No extra text, just JSON."""
            },
            {
                "role": "user",
                "content": f"Situation: {input.situation}\n\nMachiavelli principles:\n{principles_text}"
            }
        ]
    )

    import json, re
    content = response.choices[0].message.content
    match = re.search(r'\{.*\}', content, re.DOTALL)
    result = json.loads(match.group())

    return {
        "questions": result["questions"],
        "machiavelli_context": result["context"],
        "principles": principles
    }

@router.post("/socratic/complete")
def complete_socratic(input: SocraticInput, db: Session = Depends(get_db)):
    principles = retrieve_principles(input.situation, k=2)
    principles_text = "\n".join(principles)
    answers_text = "\n".join([f"Answer {i+1}: {a}" for i, a in enumerate(input.user_answers)])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a Machiavellian communication coach. 
                Based on the situation and the person's reflective answers, give deep strategic advice.
                
                Return ONLY a JSON object:
                {
                    "diagnosis": "what your answers reveal about your communication mindset",
                    "strategic_advice": "what Machiavelli would tell you to do",
                    "rewritten": "how to handle this situation with strategic communication",
                    "principle": "the key Machiavellian principle that applies here",
                    "exercise": "one practical exercise to improve this specific weakness"
                }
                No extra text, just JSON."""
            },
            {
                "role": "user",
                "content": f"Situation: {input.situation}\n\nUser's reflective answers:\n{answers_text}\n\nMachiavelli principles:\n{principles_text}"
            }
        ]
    )

    import json, re
    content = response.choices[0].message.content
    match = re.search(r'\{.*\}', content, re.DOTALL)
    result = json.loads(match.group())

    return {
        "diagnosis": result["diagnosis"],
        "strategic_advice": result["strategic_advice"],
        "rewritten": result["rewritten"],
        "principle": result["principle"],
        "exercise": result["exercise"]
    }