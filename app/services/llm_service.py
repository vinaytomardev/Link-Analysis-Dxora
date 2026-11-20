import json
from openai import AsyncOpenAI
from app.config import settings

SYSTEM_PROMPT = """
You are a careful business, SEO, and market research analyst.
Analyze only the supplied website information. Do not pretend that you browsed other sites.
If information is missing, state that it is unknown or make a clearly labeled inference.
Competitors must be plausible candidates, not claimed as verified. Include at least 3 only
when reasonably supportable; otherwise return fewer and explain the limitation.
Return valid JSON only, matching the requested schema exactly.
Create exactly 5 search query ideas and up to 5 important services.
For every service, set inferred=true if it is not explicitly supported by the page.
Do not invent search volume, rankings, traffic, market share, or performance metrics.
"""

JSON_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "brand": {
            "type": "object", "additionalProperties": False,
            "properties": {
                "name": {"type": "string"},
                "category": {"type": "string"},
                "summary": {"type": "string"}
            }, "required": ["name", "category", "summary"]
        },
        "analysis": {
            "type": "object", "additionalProperties": False,
            "properties": {
                "competitor_analysis": {
                    "type": "object", "additionalProperties": False,
                    "properties": {
                        "brand_overview": {"type": "string"},
                        "competitors": {"type": "array", "items": {
                            "type": "object", "additionalProperties": False,
                            "properties": {
                                "name": {"type": "string"},
                                "website": {"type": ["string", "null"]},
                                "strengths": {"type": "array", "items": {"type": "string"}},
                                "weaknesses_or_gaps": {"type": "array", "items": {"type": "string"}}
                            }, "required": ["name", "website", "strengths", "weaknesses_or_gaps"]
                        }},
                        "strengths": {"type": "array", "items": {"type": "string"}},
                        "opportunities": {"type": "array", "items": {"type": "string"}}
                    }, "required": ["brand_overview", "competitors", "strengths", "opportunities"]
                },
                "target_search_queries": {"type": "array", "items": {
                    "type": "object", "additionalProperties": False,
                    "properties": {
                        "query": {"type": "string"},
                        "platforms": {"type": "array", "items": {"type": "string"}},
                        "intent": {"type": "string"},
                        "business_relevance": {"type": "string"},
                        "target_audience": {"type": "string"}
                    }, "required": ["query", "platforms", "intent", "business_relevance", "target_audience"]
                }},
                "seo_improvements": {
                    "type": "object", "additionalProperties": False,
                    "properties": {
                        "primary_keyword": {"type": "string"},
                        "secondary_keywords": {"type": "array", "items": {"type": "string"}},
                        "long_tail_keywords": {"type": "array", "items": {"type": "string"}},
                        "recommended_title": {"type": "string"},
                        "meta_description": {"type": "string"},
                        "supporting_content": {"type": "array", "items": {"type": "string"}}
                    }, "required": ["primary_keyword", "secondary_keywords", "long_tail_keywords", "recommended_title", "meta_description", "supporting_content"]
                },
                "top_services": {"type": "array", "items": {
                    "type": "object", "additionalProperties": False,
                    "properties": {
                        "service_name": {"type": "string"},
                        "description": {"type": "string"},
                        "target_industry": {"type": "string"},
                        "target_customer": {"type": "string"},
                        "main_benefit": {"type": "string"},
                        "inferred": {"type": "boolean"}
                    }, "required": ["service_name", "description", "target_industry", "target_customer", "main_benefit", "inferred"]
                }},
                "target_audience": {
                    "type": "object", "additionalProperties": False,
                    "properties": {
                        "primary_audience": {"type": "array", "items": {"type": "string"}},
                        "secondary_audience": {"type": "array", "items": {"type": "string"}},
                        "industries": {"type": "array", "items": {"type": "string"}},
                        "business_types": {"type": "array", "items": {"type": "string"}},
                        "customer_profiles": {"type": "array", "items": {"type": "string"}},
                        "geography": {"type": "array", "items": {"type": "string"}},
                        "customer_needs": {"type": "array", "items": {"type": "string"}},
                        "interests": {"type": "array", "items": {"type": "string"}},
                        "recommended_marketing_segments": {"type": "array", "items": {"type": "string"}}
                    }, "required": ["primary_audience", "secondary_audience", "industries", "business_types", "customer_profiles", "geography", "customer_needs", "interests", "recommended_marketing_segments"]
                }
            }, "required": ["competitor_analysis", "target_search_queries", "seo_improvements", "top_services", "target_audience"]
        }
    }, "required": ["brand", "analysis"]
}

async def analyze_with_llm(website_data: dict) -> dict:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    payload = {
        "website_url": website_data["final_url"],
        "page_title": website_data["title"],
        "meta_description": website_data["meta_description"],
        "headings": website_data["headings"],
        "page_content": website_data["content"],
    }

    response = await client.chat.completions.create(
        model=settings.openai_model,
        temperature=0.2,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "website_link_analysis",
                "strict": True,
                "schema": JSON_SCHEMA
            }
        },
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}
        ],
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The AI provider returned an empty response.")
    return json.loads(content)
