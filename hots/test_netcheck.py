import unittest
from unittest.mock import Mock, patch

from netcheck import check_endpoint, run_basic_network_checks


class NetcheckTests(unittest.TestCase):
    @patch("netcheck.requests.get")
    def test_check_endpoint_ok(self, get_mock: Mock) -> None:
        resp = Mock()
        resp.status_code = 204
        get_mock.return_value = resp

        result = check_endpoint("Google", "https://www.google.com/generate_204", timeout=1)
        self.assertTrue(result.ok)
        self.assertEqual(result.status_code, 204)
        self.assertIsNotNone(result.latency_ms)

    @patch("netcheck.requests.get", side_effect=RuntimeError("boom"))
    def test_check_endpoint_error(self, _get_mock: Mock) -> None:
        result = check_endpoint("X", "https://example.com", timeout=1)
        self.assertFalse(result.ok)
        self.assertIsNone(result.status_code)
        self.assertIn("boom", result.error or "")

    @patch("netcheck.check_endpoint")
    def test_run_basic_network_checks(self, check_mock: Mock) -> None:
        check_mock.return_value = Mock(ok=True)
        results = run_basic_network_checks(timeout=2)
        self.assertEqual(len(results), 3)
        self.assertEqual(check_mock.call_count, 3)


if __name__ == "__main__":
    unittest.main()
