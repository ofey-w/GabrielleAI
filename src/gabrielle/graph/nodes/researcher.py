import asyncio

from gabrielle.graph.state import ResearchState, SourceDict
from gabrielle.services.search.base import SearchProvider


def make_researcher(search_provider: SearchProvider):
    async def gather_sources(state: ResearchState) -> dict:
        sub_questions = state.get("sub_questions", [])
        max_sources = state.get("max_sources", 5)

        if not sub_questions:
            return {"raw_search_results": []}

        results_per_question = max(1, max_sources // len(sub_questions))

        async def search_one(question: str):
            try:
                return await search_provider.search(question, max_results=results_per_question)
            except Exception:
                return []

        search_results = await asyncio.gather(
            *(search_one(question) for question in sub_questions)
        )

        seen_urls: set[str] = set()
        raw_search_results: list[SourceDict] = []

        for results in search_results:
            for result in results:
                if result.url in seen_urls:
                    continue
                seen_urls.add(result.url)
                raw_search_results.append(
                    SourceDict(url=result.url, title=result.title, snippet=result.snippet)
                )

        return {"raw_search_results": raw_search_results[:max_sources]}

    return gather_sources

