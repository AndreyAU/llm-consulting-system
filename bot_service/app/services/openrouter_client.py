import httpx

from app.core.config import settings


async def call_openrouter(prompt: str) -> str:
    url = f"{settings.openrouter_base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "HTTP-Referer": settings.openrouter_site_url,
        "X-Title": settings.openrouter_app_name,
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(url, json=payload, headers=headers)

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except httpx.HTTPError as e:
        raise RuntimeError(f"OpenRouter request failed: {str(e)}")
