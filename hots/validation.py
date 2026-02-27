from __future__ import annotations

import re
from typing import Iterable, List, Tuple

_HOST_RE = re.compile(r"^(?=.{1,253}$)(?!-)[a-z0-9-]+(\.(?!-)[a-z0-9-]+)*\.?$", re.IGNORECASE)
_PROXY_RE = re.compile(r"^(?P<host>[^:\s]+):(?P<port>\d{1,5})$")


def normalize_host(value: str) -> str | None:
    host = (value or "").strip().lower().rstrip(".")
    if not host:
        return None
    if " " in host:
        return None
    if not _HOST_RE.match(host):
        return None
    return host


def normalize_hosts(values: Iterable[str]) -> Tuple[List[str], List[str]]:
    valid: List[str] = []
    invalid: List[str] = []
    seen = set()

    for raw in values:
        normalized = normalize_host(raw)
        if normalized is None:
            if str(raw).strip():
                invalid.append(str(raw).strip())
            continue
        if normalized not in seen:
            seen.add(normalized)
            valid.append(normalized)

    return valid, invalid


def normalize_proxies(raw: str) -> Tuple[List[str], List[str]]:
    valid: List[str] = []
    invalid: List[str] = []
    seen = set()

    for part in (raw or "").replace("\n", ",").split(","):
        token = part.strip()
        if not token:
            continue

        m = _PROXY_RE.match(token)
        if not m:
            invalid.append(token)
            continue

        port = int(m.group("port"))
        if port < 1 or port > 65535:
            invalid.append(token)
            continue

        normalized = f"{m.group('host')}:{port}"
        if normalized not in seen:
            seen.add(normalized)
            valid.append(normalized)

    return valid, invalid
