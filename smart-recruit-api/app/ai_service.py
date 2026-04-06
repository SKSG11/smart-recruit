import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview").strip()

GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)

def _extract_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)

def analyser_compatibilite(description_offre, bio_candidat):
    if not GEMINI_API_KEY:
        return None, "GEMINI_API_KEY manquante"

    prompt = f"""
Analyse la compatibilité entre cette offre et ce candidat.

Offre :
{description_offre}

Candidat :
{bio_candidat}

Réponds exclusivement au format JSON avec :
- score : entier de 0 à 100
- justification : texte de 200 caractères max
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }

    try:
        response = requests.post(
            GEMINI_URL,
            headers={
                "x-goog-api-key": GEMINI_API_KEY,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=20
        )
        response.raise_for_status()

        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        resultat = _extract_json(text)

        return resultat, None

    except requests.Timeout:
        return None, "Timeout lors de l'appel Gemini"

    except (requests.RequestException, KeyError, IndexError, ValueError, json.JSONDecodeError) as e:
        return None, f"Erreur Gemini : {str(e)}"