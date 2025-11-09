from __future__ import annotations

from typing import Optional

import httpx

from app.core.config import settings


async def generate_with_openai(prompt: str) -> Optional[str]:
    if not settings.openai_api_key:
        return None
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a concise contract negotiation assistant."},
            {"role": "user", "content": prompt},
        ],
    }
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
