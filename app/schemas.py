from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class LinkAnalysisRequest(BaseModel):
    url: HttpUrl

class Competitor(BaseModel):
    name: str
    website: Optional[str] = None
    strengths: List[str] = Field(default_factory=list)
    weaknesses_or_gaps: List[str] = Field(default_factory=list)

class CompetitorAnalysis(BaseModel):
    brand_overview: str
    competitors: List[Competitor] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)

class SearchQuery(BaseModel):
    query: str
    platforms: List[str] = Field(default_factory=list)
    intent: str
    business_relevance: str
    target_audience: str

class SEOImprovements(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str] = Field(default_factory=list)
    long_tail_keywords: List[str] = Field(default_factory=list)
    recommended_title: str
    meta_description: str
    supporting_content: List[str] = Field(default_factory=list)

class ServiceItem(BaseModel):
    service_name: str
    description: str
    target_industry: str
    target_customer: str
    main_benefit: str
    inferred: bool = False

class TargetAudience(BaseModel):
    primary_audience: List[str] = Field(default_factory=list)
    secondary_audience: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)
    business_types: List[str] = Field(default_factory=list)
    customer_profiles: List[str] = Field(default_factory=list)
    geography: List[str] = Field(default_factory=list)
    customer_needs: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    recommended_marketing_segments: List[str] = Field(default_factory=list)

class Brand(BaseModel):
    name: str
    category: str
    summary: str

class Analysis(BaseModel):
    competitor_analysis: CompetitorAnalysis
    target_search_queries: List[SearchQuery]
    seo_improvements: SEOImprovements
    top_services: List[ServiceItem]
    target_audience: TargetAudience

class LinkAnalysisResponse(BaseModel):
    success: bool
    website: str
    brand: Brand
    analysis: Analysis
