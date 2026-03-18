from typing import NotRequired, TypedDict


class SourceDict(TypedDict):
    url: str
    title: str
    snippet: str


class FindingDict(TypedDict):
    claim: str
    supporting_sources: list[SourceDict]


class ResearchState(TypedDict):
    # Set by API layer before graph.invoke()
    query: str
    max_sources: int

    # Set by Planner
    sub_questions: list[str]

    # Set by Researcher
    raw_search_results: list[SourceDict]

    # Set by Writer
    draft_report: str
    findings: list[FindingDict]

    # Assembled at END — matches ResearchResponse shape
    final_response: NotRequired[dict]