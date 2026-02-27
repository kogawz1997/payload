import random
import threading
import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


USER_AGENTS: List[str] = [
    # Android
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36",
    # iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    # Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]


COMMON_HEADERS: Dict[str, str] = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


@dataclass
class StealthConfig:
    min_delay: float = 0.5
    max_delay: float = 3.0
    timeout: float = 4.0
    proxies: Optional[List[str]] = None  # list of "ip:port"


class ProxyRotator:
    def __init__(self, proxies: Iterable[str] | None):
        self._proxies = list(proxies or [])
        self._index = 0
        self._lock = threading.Lock()

    def get_next(self) -> Optional[str]:
        if not self._proxies:
            return None
        with self._lock:
            value = self._proxies[self._index % len(self._proxies)]
            self._index += 1
            return value


def random_user_agent() -> str:
    return random.choice(USER_AGENTS)


def build_headers(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Header Shuffling: ใน requests dict เองจะไม่การันตีลำดับ header
    แต่เราจะสุ่ม User-Agent + merge headers พื้นฐานให้
    """
    headers = dict(COMMON_HEADERS)
    headers["User-Agent"] = random_user_agent()
    if extra:
        headers.update(extra)
    return headers


def jitter_sleep(config: StealthConfig) -> None:
    delay = random.uniform(config.min_delay, config.max_delay)
    time.sleep(delay)

