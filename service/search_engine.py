from aiohttp import ClientSession, TCPConnector

from app.env_validator import settings


class GoogleSearchEngine:
    def __init__(self) -> None:
        self._session = ClientSession(
            base_url="https://www.googleapis.com", connector=TCPConnector(ssl=False)
        )

    async def search(self, keyword: str) -> list[dict]:
        async with self._session.get(
            "/customsearch/v1",
            params={
                "key": settings.GOOGLE_SEARCH_API_KEY,
                "q": keyword,
                "cx": settings.GOOGLE_SEARCH_ENGINE_ID,
            },
        ) as response:
            data = await response.json()
            if "items" not in data:
                return []
            
            return data["items"]
