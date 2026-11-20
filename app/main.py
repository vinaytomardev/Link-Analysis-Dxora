from fastapi import FastAPI, HTTPException
from app.schemas import LinkAnalysisRequest, LinkAnalysisResponse
from app.services.analysis_service import run_analysis
from app.utils.validators import validate_public_http_url

app = FastAPI(
    title="AI-Powered Website Link Analysis API",
    description="Extracts website content and generates business, competitor, SEO and audience insights.",
    version="1.0.0",
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/link-analysis", response_model=LinkAnalysisResponse)
async def link_analysis(request: LinkAnalysisRequest):
    url = str(request.url)
    try:
        validate_public_http_url(url)
        _, result = await run_analysis(url)
        return {
            "success": True,
            "website": url,
            "brand": result["brand"],
            "analysis": result["analysis"],
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        # Avoid returning API keys, stack traces, or internal provider details.
        message = str(exc)
        if "OPENAI_API_KEY" in message:
            raise HTTPException(status_code=503, detail="AI service is not configured. Set OPENAI_API_KEY.")
        if "timeout" in message.lower():
            raise HTTPException(status_code=504, detail="The website or AI service timed out.")
        if "404" in message or "403" in message or "429" in message:
            raise HTTPException(status_code=502, detail="The website could not be fetched or the AI provider rejected the request.")
        raise HTTPException(status_code=502, detail="Website analysis failed. Check the URL and server logs.")
