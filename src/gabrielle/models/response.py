from datetime import datetime

from pydantic import BaseModel


class Source(BaseModel):
    url: str
    title: str
    snippet: str


class Finding(BaseModel):
    claim: str
    supporting_sources: list[Source]


class ResponseMetadata(BaseModel):
    created_at: datetime
    duration_seconds: float
    llm_provider: str
    llm_model: str
    sources_found: int
    sub_questions: list[str]


class ResearchResponse(BaseModel):
    query: str
    report: str
    findings: list[Finding]
    sources: list[Source]
    metadata: ResponseMetadata
