from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True,
    project="convosatya-lead-agent",
    location="global",
)


def discover_and_research(query: str) -> dict:
    """
    Searches the public web for information related to the given query
    (e.g. an investor name, accelerator, or an instruction like
    "find AI investors in New York") and returns a research summary.

    Args:
        query: What to search for and research.

    Returns:
        A dictionary with the research summary text and the source URLs used.
    """
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=(
            "Research the following for ConvoSatya, an AI startup: "
            f"{query}\n\n"
            "Find real, currently active people, organizations, or events "
            "matching this. For each one, note their name, category "
            "(investor, accelerator, hackathon, event, demo_night, or "
            "startup_program), and why they might be relevant to "
            "ConvoSatya. Be concise."
        ),
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        ),
    )

    sources = []
    try:
        grounding = response.candidates[0].grounding_metadata
        for chunk in grounding.grounding_chunks:
            if chunk.web and chunk.web.uri:
                sources.append(chunk.web.uri)
    except Exception:
        pass  # source extraction is best-effort; summary text is still valid

    return {
        "summary": response.text,
        "sources": sources,
    }