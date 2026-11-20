"""Competitor discovery is performed by the LLM in this starter version.

For production-quality competitor validation, connect a search provider (for example,
Bing Web Search, Google Programmable Search, or another licensed search API).
Do not present unverified competitor names as confirmed facts.
"""

def competitor_research_note() -> str:
    return (
        "Competitors are AI-generated hypotheses based on the supplied website content. "
        "Verify their existence, relevance, and claims using reliable external sources."
    )
