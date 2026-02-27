from typing import Dict

from stealth import random_user_agent


CRLF = "\r\n"


TEMPLATES: Dict[str, str] = {
    # WebSocket แบบที่คุณขอ (GET + HTML title)
    "websocket": (
        "GET /<h5><font color=\"red\"> Zero X Net <p style=\"text-align:center\"/ HTTP/1.1[crlf]"
        "Host: [host_port][crlf]"
        "Upgrade: Websocket[crlf]"
        "Connection: Keep-Alive[crlf]"
        "[crlf]"
    ),
    # PATCH แบบที่คุณขอ (มี User-Agent และ Upgrade)
    "direct_patch": (
        "PATCH /<h5><font color=\"red\"> Zero X Net <p style=\"text-align:center\"/ HTTP/1.1[crlf]"
        "Host: [host][crlf]"
        "Host: -[crlf]"
        "Connection: Upgrade[crlf]"
        "User-Agent: [ua][crlf]"
        "Upgrade: websocket[crlf]"
        "[crlf]"
    ),
    # สำหรับกรณีใช้งานผ่าน proxy (เช่น 104.18.5.238:8880)
    "cloudflare_proxy": (
        "GET / HTTP/1.1[crlf]"
        "Host: [host][crlf]"
        "Connection: Keep-Alive[crlf]"
        "[crlf]"
    ),
}


def format_payload(template_key: str, host: str) -> str:
    raw = TEMPLATES[template_key]

    # host_port ตอนนี้ใช้ host ตรง ๆ (ถ้าต้องการต่อพอร์ตสามารถเพิ่มเองได้ เช่น host:8880)
    host_port = host
    ua = random_user_agent()

    return (
        raw.replace("[host_port]", host_port)
        .replace("[host]", host)
        .replace("[ua]", ua)
        .replace("[crlf]", CRLF)
        .strip()
        + CRLF
    )


def build_all_payloads_for_host(host: str) -> Dict[str, str]:
    return {name: format_payload(name, host) for name in TEMPLATES}

