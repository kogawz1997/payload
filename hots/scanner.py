from __future__ import annotations

import threading
from dataclasses import dataclass
from queue import Queue, Empty
from typing import Callable, Dict, Iterable, List, Optional

import requests

from stealth import StealthConfig, ProxyRotator, build_headers, jitter_sleep


@dataclass
class HostScanResult:
    host: str
    status: str
    http_status: Optional[int] = None
    port: Optional[int] = None
    is_websocket_like: bool = False
    is_redirect: bool = False
    redirect_location: Optional[str] = None
    error: Optional[str] = None


def build_requests_proxy(proxy_str: Optional[str]) -> Optional[Dict[str, str]]:
    if not proxy_str:
        return None
    return {
        "http": f"http://{proxy_str}",
        "https": f"http://{proxy_str}",
    }


def scan_single_host(
    host: str,
    config: StealthConfig,
    proxy_rotator: ProxyRotator,
    scheme: str = "https",
) -> HostScanResult:
    url = f"{scheme}://{host}"
    jitter_sleep(config)

    proxy = proxy_rotator.get_next()
    proxies = build_requests_proxy(proxy)

    # Multi-Port Scanner ตามสเปก: 80, 443, 8080, 8880
    ports = [80, 443, 8080, 8880]

    last_error: Optional[str] = None
    saw_timeout = False

    for port in ports:
        # ใส่พอร์ตเฉพาะกรณีไม่ใช่ค่า default เพื่อให้ URL ดูสั้นลง
        if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
            url = f"{scheme}://{host}"
        else:
            url = f"{scheme}://{host}:{port}"

        try:
            resp = requests.get(
                url,
                headers=build_headers(),
                timeout=config.timeout,
                allow_redirects=False,
                proxies=proxies,
            )
            code = resp.status_code
            is_ws = code == 101
            is_redirect = 300 <= code < 400
            location = resp.headers.get("Location")

            status = "ok"
            if is_redirect:
                status = "redirect"
            if is_ws:
                status = "websocket"

            return HostScanResult(
                host=host,
                status=status,
                http_status=code,
                port=port,
                is_websocket_like=is_ws,
                is_redirect=is_redirect,
                redirect_location=location,
            )
        except requests.Timeout as exc:
            last_error = str(exc)
            saw_timeout = True
            # ลองพอร์ตถัดไปต่อไป
            continue
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
            # ลองพอร์ตถัดไปต่อไป
            continue

    if saw_timeout:
        return HostScanResult(host=host, status="timeout", error=last_error)
    return HostScanResult(host=host, status="error", error=last_error)


def worker_thread(
    q: Queue,
    results: List[HostScanResult],
    lock: threading.Lock,
    config: StealthConfig,
    proxy_rotator: ProxyRotator,
    scheme: str,
    on_progress: Optional[Callable[[HostScanResult], None]] = None,
) -> None:
    while True:
        try:
            host = q.get_nowait()
        except Empty:
            return

        result = scan_single_host(host, config=config, proxy_rotator=proxy_rotator, scheme=scheme)

        with lock:
            results.append(result)
        if on_progress:
            on_progress(result)

        q.task_done()


def scan_hosts_parallel(
    hosts: Iterable[str],
    config: Optional[StealthConfig] = None,
    scheme: str = "https",
    max_workers: int = 10,
    proxies: Optional[List[str]] = None,
    on_progress: Optional[Callable[[HostScanResult], None]] = None,
) -> List[HostScanResult]:
    """
    Multi-thread scanner: ส่ง worker หลายเส้นไปตรวจ host พร้อมกัน
    """
    cfg = config or StealthConfig()
    if proxies is None:
        proxies = cfg.proxies

    proxy_rotator = ProxyRotator(proxies)

    q: Queue = Queue()
    for h in hosts:
        q.put(h)

    results: List[HostScanResult] = []
    lock = threading.Lock()

    workers: List[threading.Thread] = []
    for _ in range(max_workers):
        t = threading.Thread(
            target=worker_thread,
            kwargs={
                "q": q,
                "results": results,
                "lock": lock,
                "config": cfg,
                "proxy_rotator": proxy_rotator,
                "scheme": scheme,
                "on_progress": on_progress,
            },
            daemon=True,
        )
        t.start()
        workers.append(t)

    for t in workers:
        t.join()

    return results

