from dataclasses import dataclass
from typing import Protocol


@dataclass
class SearchResult:
    url: str
    title: str
    snippet: str


class SearchProvider(Protocol):
    async def search(self, query: str, max_results: int) -> list[SearchResult]: ...
