from __future__ import annotations

from typing import Any, Dict, Optional

import click
import requests


class DropscanClient:
    def __init__(self, api_key: str, base_url: str = "https://api.dropscan.de/v1") -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            }
        )

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        expect_json: bool = True,
    ) -> Any:
        response = self.session.get(self._url(path), params=self._prune_none(params), timeout=60)
        self._raise_for_status(response)
        if expect_json:
            return response.json()
        return response.text

    def post(
        self,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
        expect_json: bool = True,
    ) -> Any:
        response = self.session.post(self._url(path), json=payload or {}, timeout=60)
        self._raise_for_status(response)
        if expect_json:
            if response.content:
                return response.json()
            return {}
        return response.text

    def delete(self, path: str) -> None:
        response = self.session.delete(self._url(path), timeout=60)
        self._raise_for_status(response)

    def get_binary(self, path: str) -> bytes:
        response = self.session.get(self._url(path), timeout=60)
        self._raise_for_status(response)
        return response.content

    def _url(self, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"

    @staticmethod
    def _prune_none(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not data:
            return {}
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        if response.ok:
            return
        body = response.text.strip()
        raise click.ClickException(f"API error {response.status_code}: {body}")
