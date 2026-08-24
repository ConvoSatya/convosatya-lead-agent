from research_tool import discover_and_research

result = discover_and_research("Find early-stage AI accelerators in New York")

print("SUMMARY:\n", result["summary"])
print("\nSOURCES:")
for s in result["sources"]:
    print("-", s)