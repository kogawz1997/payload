import random
from typing import Iterable, List, Set

import requests


CRTSH_URL = "https://crt.sh/"


def normalize_hostname(value: str, domain: str) -> str | None:
    """
    Normalize hostname candidates from crt.sh.

    - trims whitespace
    - lowercases values
    - removes wildcard prefixes ("*.")
    - strips trailing dot
    - returns only names under the requested domain
    """
    name = (value or "").strip().lower().rstrip(".")
    if not name:
        return None

    if name.startswith("*."):
        name = name[2:]

    root = domain.strip().lower().rstrip(".")
    if not root:
        return None

    if name == root or name.endswith(f".{root}"):
        return name

    return None


def fetch_subdomains_from_crtsh(domain: str, timeout: float = 8.0) -> List[str]:
    """
    Passive Scraper: ดึง subdomain จาก crt.sh โดยไม่ยิงตรงไปที่เว็บเป้าหมาย
    """
    params = {"q": f"%.{domain}", "output": "json"}
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
            normalized = normalize_hostname(line, domain)
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
    if prefixes is None:
        prefixes = DEFAULT_PREFIXES

    clean_domain = domain.strip().lower().rstrip(".")
    hosts = [f"{p.strip().lower()}.{clean_domain}" for p in prefixes if p]
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

