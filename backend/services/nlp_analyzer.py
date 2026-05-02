import textstat
from groq import Groq
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from rag.rag_pipeline import retrieve_principles

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_text(text: str) -> dict:
    clarity = min(textstat.flesch_reading_ease(text) / 10, 10)
    clarity = max(clarity, 0)

    sentence_count = textstat.sentence_count(text)
    word_count = textstat.lexicon_count(text)
    avg_words = word_count / max(sentence_count, 1)
    structure = 10 if 10 <= avg_words <= 20 else max(0, 10 - abs(avg_words - 15) * 0.3)

    principles = retrieve_principles(text, k=2)
    principles_text = "\n".join(principles)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a Machiavellian communication analyst. Analyze the given text and return ONLY a JSON object with these exact keys:
                {
                    "confidence_score": <float 0-10>,
                    "persuasiveness_score": <float 0-10>,
                    "confidence_reason": "<one line>",
                    "persuasiveness_reason": "<one line>",
                    "machiavelli_feedback": "<2-3 sentences of strategic communication advice based on Machiavelli>",
                    "rewritten": "<rewrite the text more powerfully and strategically>"
                }
                No extra text, just the JSON."""
            },
            {
                "role": "user",
                "content": f"Text to analyze: {text}\n\nRelevant Machiavelli principles:\n{principles_text}"
            }
        ]
    )

    import json
    import re
    content = response.choices[0].message.content
    # Extract JSON even if model adds extra text
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in response: {content}")
    result = json.loads(match.group())


    overall = (clarity + structure + result["confidence_score"] + result["persuasiveness_score"]) / 4

    return {
        "clarity_score": round(clarity, 2),
        "structure_score": round(structure, 2),
        "confidence_score": round(result["confidence_score"], 2),
        "persuasiveness_score": round(result["persuasiveness_score"], 2),
        "overall_score": round(overall, 2),
        "confidence_reason": result["confidence_reason"],
        "persuasiveness_reason": result["persuasiveness_reason"],
        "machiavelli_feedback": result["machiavelli_feedback"],
        "rewritten": result["rewritten"],
        "principles_used": principles
    }