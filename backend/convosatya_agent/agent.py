from google.adk.agents.llm_agent import Agent
from research_tool import discover_and_research
from pipeline_tool import save_leads

root_agent = Agent(
    model='gemini-3.6-flash',
    name='root_agent',
    description='An agent that discovers and tracks startup opportunities for ConvoSatya.',
    instruction=(
        "You are ConvoSatya's opportunity discovery agent. When asked to "
        "find leads, use discover_and_research to search the web, then "
        "use save_leads to save the results to Firestore. Always call "
        "save_leads after discover_and_research, using the leads and "
        "sources it returned, with discovered_via set to 'founder_guided' "
        "or 'autonomous' depending on how you were triggered."
    ),
    tools=[discover_and_research, save_leads],
)