from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from gabrielle.graph.state import FindingDict, ResearchState


class WriterOutput(BaseModel):
    """Structured output schema for the Writer LLM call."""

    report: str
    findings: list[FindingDict]


def make_writer(llm: BaseChatModel):
    async def write_report(state: ResearchState) -> dict:
        query = state["query"]
        sources = state["raw_search_results"]

        if not sources:
            return {
                "draft_report": "No relevant sources were found, so a source-grounded report could not be generated.",
                "findings": [],
            }

        sources_text = "\n\n".join(
            f"[{i + 1}] {s['title']}\n    URL: {s['url']}\n    {s['snippet']}"
            for i, s in enumerate(sources)
        )

        prompt = f"""
You are a research writer.

Write a concise, source-grounded research brief that answers the user's query using only the sources below. These sources are search-result summaries, not full documents, so do not assume facts beyond what is stated in the titles and snippets.

User query:
{query}

Sources:
{sources_text}

Report requirements:
- Write a markdown report in 3 to 6 paragraphs.
- Answer the query directly and synthesize the strongest available evidence.
- Cite sources inline with bracketed numbers like [1], [2].
- Use only claims supported by the provided sources.
- Do not fabricate information, additional context, or extra sources.
- If evidence is incomplete, limited, or mixed, state that clearly.
- If sources disagree, note the disagreement.

Findings requirements:
- Provide 3 to 5 key findings.
- Each finding must be a specific, non-duplicative claim supported by the provided sources.
- Do not include vague, generic, or speculative findings.
- For each finding, include supporting sources drawn only from the list above.

Return output that matches the required schema.
""".strip()

        structured_llm = llm.with_structured_output(WriterOutput)
        result: WriterOutput = await structured_llm.ainvoke([HumanMessage(content=prompt)])  # type: ignore[assignment]

        return {
            "draft_report": result.report,
            "findings": result.findings,
        }

    return write_report

