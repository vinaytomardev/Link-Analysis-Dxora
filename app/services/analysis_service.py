from app.services.website_extractor import extract_website
from app.services.llm_service import analyze_with_llm
from app.schemas import Brand, Analysis

async def run_analysis(url: str) -> tuple[dict, dict]:
    website_data = await extract_website(url)
    result = await analyze_with_llm(website_data)
    # Pydantic validation ensures the model output follows our API contract.
    brand = Brand.model_validate(result["brand"]).model_dump()
    analysis = Analysis.model_validate(result["analysis"]).model_dump()
    return website_data, {"brand": brand, "analysis": analysis}
