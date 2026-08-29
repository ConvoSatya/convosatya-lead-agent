import json
import re
from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True,
    project="convosatya-lead-agent",
    location="global",
)

LEAD_SCHEMA = {
    "type": "object",
    "properties": {
        "leads": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "category": {
                        "type": "string",
                        "enum": [
                            "investor",
                            "accelerator",
                            "hackathon",
                            "event",
                            "demo_night",
                            "startup_program",
                        ],
                    },
                    "relevance_note": {"type": "string"},
                    "contact_email": {"type": "string"},
                    "linkedin_url": {"type": "string"},
                },
                "required": ["name", "category", "relevance_note"],
            },
        }
    },
    "required": ["leads"],
}


def _clean_json_text(text: str) -> str:
    text = text.strip()
    match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
    if match:
        text = match.group(1)
    return text.strip()


def discover_and_research(query: str) -> dict:
    print("Calling Gemini with search grounding...")
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=(
            "Research the following for ConvoSatya, an AI startup: "
            f"{query}\n\n"
            "Find real, currently active people, organizations, or events "
            "matching this. Leave contact_email or linkedin_url as an "
            "empty string if you don't have one. Keep relevance_note to "
            "1-2 sentences."
        ),
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            response_mime_type="application/json",
            response_json_schema=LEAD_SCHEMA,
        ),
    )
    print("Got response, parsing...")

    cleaned = _clean_json_text(response.text)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        print("RAW RESPONSE (failed to parse):", repr(response.text))
        raise

    leads = parsed.get("leads", [])

    sources = []
    try:
        grounding = response.candidates[0].grounding_metadata
        for chunk in grounding.grounding_chunks:
            if chunk.web and chunk.web.uri:
                sources.append(chunk.web.uri)
    except Exception:
        pass

    return {"leads": leads, "sources": sources}