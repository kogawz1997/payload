from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List

import requests

from stealth import build_headers


@dataclass
class NetCheckResult:
    name: str
    url: str
    ok: bool
    status_code: int | None
    latency_ms: float | None
    error: str | None = None


DEFAULT_ENDPOINTS: list[tuple[str, str]] = [
    ("Cloudflare", "https://1.1.1.1/cdn-cgi/trace"),
    ("Google", "https://www.google.com/generate_204"),
    ("GitHub", "https://github.com"),
]


def check_endpoint(name: str, url: str, timeout: float = 4.0) -> NetCheckResult:
    started = time.perf_counter()
    try:
        resp = requests.get(url, timeout=timeout, headers=build_headers(), allow_redirects=True)
        latency_ms = (time.perf_counter() - started) * 1000.0
        return NetCheckResult(
            name=name,
            url=url,
            ok=True,
            status_code=resp.status_code,
            latency_ms=latency_ms,
        )
    except Exception as exc:  # noqa: BLE001
        latency_ms = (time.perf_counter() - started) * 1000.0
        return NetCheckResult(
            name=name,
            url=url,
            ok=False,
            status_code=None,
            latency_ms=latency_ms,
            error=str(exc),
        )


def run_basic_network_checks(timeout: float = 4.0) -> List[NetCheckResult]:
    return [check_endpoint(name, url, timeout=timeout) for name, url in DEFAULT_ENDPOINTS]
