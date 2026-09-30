"""Synchronous HTTP client used inside background Qt workers."""

from typing import Any

import httpx


class ApiError(RuntimeError):
    """Raised when the backend request fails or returns an error response."""


class TaskApiClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: float = 8.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            response = httpx.request(
                method, f"{self.base_url}{path}", timeout=self.timeout, **kwargs
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            try:
                detail = exc.response.json().get("detail", str(exc))
            except ValueError:
                detail = str(exc)
            raise ApiError(str(detail)) from exc
        except httpx.HTTPError as exc:
            raise ApiError(f"Cannot connect to TaskFlow API: {exc}") from exc
        return None if response.status_code == 204 else response.json()

    def list_tasks(self, status: str | None = None, search: str | None = None) -> list[dict]:
        params = {k: v for k, v in {"status": status, "search": search}.items() if v}
        return self._request("GET", "/api/v1/tasks", params=params)

    def summary(self) -> dict:
        return self._request("GET", "/api/v1/tasks/summary")

    def create_task(self, payload: dict) -> dict:
        return self._request("POST", "/api/v1/tasks", json=payload)

    def update_task(self, task_id: int, payload: dict) -> dict:
        return self._request("PATCH", f"/api/v1/tasks/{task_id}", json=payload)

    def delete_task(self, task_id: int) -> None:
        self._request("DELETE", f"/api/v1/tasks/{task_id}")
