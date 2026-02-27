import random
from typing import Iterable, List, Set

import requests


CRTSH_URL = "https://crt.sh/"


def normalize_domain(domain: str) -> str | None:
    """Normalize a root domain value used by discovery functions."""
    root = (domain or "").strip().lower().rstrip(".")
    return root or None


def normalize_hostname(value: str, domain: str) -> str | None:
    """
    Normalize hostname candidates from crt.sh.

    - trims whitespace
    - lowercases values
    - removes wildcard prefixes ("*.")
    - strips trailing dot
    - returns only names under the requested domain
    """
    root = normalize_domain(domain)
    if not root:
        return None

    name = (value or "").strip().lower().rstrip(".")
    if not name:
        return None

    if name.startswith("*."):
        name = name[2:]

    # malformed name guard: wildcard remnants / whitespace in host token
    if "*" in name or any(ch.isspace() for ch in name):
        return None

    if name == root or name.endswith(f".{root}"):
        return name

    return None


def fetch_subdomains_from_crtsh(domain: str, timeout: float = 8.0) -> List[str]:
    """
    Passive Scraper: ดึง subdomain จาก crt.sh โดยไม่ยิงตรงไปที่เว็บเป้าหมาย
    """
    root = normalize_domain(domain)
    if not root:
        return []

    params = {"q": f"%.{root}", "output": "json"}
    try:
        resp = requests.get(CRTSH_URL, params=params, timeout=timeout)
        resp.raise_for_status()
    except Exception:
        return []

    try:
        data = resp.json()
    except ValueError:
        return []

    results: Set[str] = set()
    for row in data:
        name_value = row.get("name_value") or ""
        for line in str(name_value).split("\n"):
            normalized = normalize_hostname(line, root)
            if normalized:
                results.add(normalized)

    return sorted(results)


DEFAULT_PREFIXES = [
    "m",
    "api",
    "v-static",
    "portal",
    "free",
    "line-api",
    "cdn",
    "edge",
    "ws",
    "wss",
]


def brute_force_subdomains(
    domain: str, prefixes: Iterable[str] | None = None, shuffle: bool = True
) -> List[str]:
    """
    Active Brute-forcer: สร้างรายชื่อ subdomain จาก prefix list
    (ยังไม่ยิง request จริง แค่เตรียม host)
    """
    clean_domain = normalize_domain(domain)
    if not clean_domain:
        return []

    if prefixes is None:
        prefixes = DEFAULT_PREFIXES

    hosts = [f"{p.strip().lower()}.{clean_domain}" for p in prefixes if p and p.strip()]
    if shuffle:
        random.shuffle(hosts)
    return hosts


def build_host_queue(domain: str, use_passive: bool = True, use_bruteforce: bool = True) -> List[str]:
    """
    รวมผลจาก passive + brute force แล้ว unique
    """
    hosts: Set[str] = set()
    if use_passive:
        hosts.update(fetch_subdomains_from_crtsh(domain))
    if use_bruteforce:
        hosts.update(brute_force_subdomains(domain))
    return sorted(hosts)
