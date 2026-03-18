from tavily import AsyncTavilyClient

from gabrielle.services.search.base import SearchResult


class TavilySearchProvider:
    def __init__(self, api_key: str) -> None:
        self._client = AsyncTavilyClient(api_key=api_key)

    async def search(self, query: str, max_results: int) -> list[SearchResult]:
        response = await self._client.search(query=query, max_results=max_results)
        return [
            SearchResult(
                url=result["url"],
                title=result["title"],
                snippet=result["content"],
            )
            for result in response["results"]
        ]
