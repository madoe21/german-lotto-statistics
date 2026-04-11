from __future__ import annotations

import json
from typing import Any
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class LottoBrandenburgApiClient:
    BASE_URL = "https://www.lotto-brandenburg.de"

    def __init__(self, locale: str = "de", timeout: int = 20) -> None:
        self.locale = locale
        self.timeout = timeout
        self.default_headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }

    def _fetch_json(self, path: str, params: dict[str, Any]) -> Any:
        query = urlencode(params)
        url = f"{self.BASE_URL}{path}?{query}"
        request = Request(url, headers=self.default_headers)

        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = response.read().decode("utf-8")
        except URLError as exc:
            raise RuntimeError(f"Request failed: {url}: {exc}") from exc

        try:
            return json.loads(payload)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON from API: {url}") from exc

    def get_draw_years(self, game_type: str) -> list[str]:
        data = self._fetch_json("/app/getDrawResultYears", {"gameType": game_type})
        if not isinstance(data, list):
            return []
        return [str(item) for item in data]

    def get_draw_dates(self, game_type: str, year: str) -> dict[str, str]:
        data = self._fetch_json(
            "/app/getDrawResultDates",
            {"locale": self.locale, "gameType": game_type, "year": str(year)},
        )
        if not isinstance(data, dict):
            return {}
        return {str(k): str(v) for k, v in data.items()}

    def get_draw_result(self, game_type: str, date_key: str) -> dict[str, Any] | None:
        data = self._fetch_json(
            "/app/getDrawResults",
            {"locale": self.locale, "gameType": game_type, "date": date_key},
        )
        if not isinstance(data, list):
            return None

        for row in data:
            if isinstance(row, dict) and row.get("gameType") == game_type:
                return row
        return None
