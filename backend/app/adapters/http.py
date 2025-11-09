from __future__ import annotations

from typing import Any, Dict, Optional

import httpx


class HTTPClient:
    def __init__(self, base_url: str | None = None, headers: Optional[Dict[str, str]] = None) -> None:
        self.base_url = base_url
        self.headers = headers or {}

    async def post(self, url: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        async with httpx.AsyncClient(base_url=self.base_url, headers={**self.headers, **(headers or {})}) as client:
            response = await client.post(url, json=json)
            response.raise_for_status()
            return response

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        async with httpx.AsyncClient(base_url=self.base_url, headers={**self.headers, **(headers or {})}) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response
