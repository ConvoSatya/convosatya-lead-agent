from research_tool import discover_and_research
from pipeline_tool import save_leads

query = (
    "Find 5 real angel investors or people relevant to ConvoSatya "
    "(an AI startup), and 5 real upcoming startup events, hackathons, "
    "or demo nights relevant to ConvoSatya. Mix investor/people and "
    "event categories."
)

result = discover_and_research(query)

print(f"Found {len(result['leads'])} leads:\n")
for lead in result["leads"]:
    print(f"- {lead['name']} ({lead['category']})")

saved = save_leads(
    leads=result["leads"],
    sources=result["sources"],
    discovered_via="founder_guided",
    founder_instruction=query,
)

print(f"\nSaved {len(saved)} new leads to Firestore:")
for name in saved:
    print("-", name)