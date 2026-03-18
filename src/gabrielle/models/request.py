from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    max_sources: int = Field(default=10, ge=1, le=15)
