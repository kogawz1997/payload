import unittest
from unittest.mock import Mock, patch

import requests

from scanner import build_requests_proxy, scan_single_host
from stealth import ProxyRotator, StealthConfig


class ScannerTests(unittest.TestCase):
    def test_build_requests_proxy(self) -> None:
        self.assertIsNone(build_requests_proxy(None))
        self.assertEqual(
            build_requests_proxy("1.2.3.4:8080"),
            {"http": "http://1.2.3.4:8080", "https": "http://1.2.3.4:8080"},
        )

    @patch("scanner.jitter_sleep")
    @patch("scanner.requests.get")
    def test_scan_single_host_success(self, get_mock: Mock, _sleep_mock: Mock) -> None:
        response = Mock()
        response.status_code = 200
        response.headers = {}
        get_mock.return_value = response

        res = scan_single_host("api.example.com", StealthConfig(timeout=1), ProxyRotator([]), "https")
        self.assertEqual(res.status, "ok")
        self.assertEqual(res.http_status, 200)

    @patch("scanner.jitter_sleep")
    @patch("scanner.requests.get")
    def test_scan_single_host_timeout_then_error(self, get_mock: Mock, _sleep_mock: Mock) -> None:
        get_mock.side_effect = requests.Timeout("timeout")
        res = scan_single_host("api.example.com", StealthConfig(timeout=1), ProxyRotator([]), "https")
        self.assertEqual(res.status, "timeout")


if __name__ == "__main__":
    unittest.main()
