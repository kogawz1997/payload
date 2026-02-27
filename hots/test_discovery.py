import unittest
from unittest.mock import Mock, patch

from discovery import (
    brute_force_subdomains,
    fetch_subdomains_from_crtsh,
    normalize_domain,
    normalize_hostname,
)


class DiscoveryTests(unittest.TestCase):
    def test_normalize_domain(self) -> None:
        self.assertEqual(normalize_domain(" Example.COM. "), "example.com")
        self.assertIsNone(normalize_domain("   "))

    def test_normalize_hostname_filters_invalid_and_unrelated(self) -> None:
        self.assertEqual(normalize_hostname("*.Api.Example.com", "example.com"), "api.example.com")
        self.assertEqual(normalize_hostname("sub.example.com.", "example.com"), "sub.example.com")
        self.assertIsNone(normalize_hostname("evil-example.com", "example.com"))
        self.assertIsNone(normalize_hostname("foo*.example.com", "example.com"))
        self.assertIsNone(normalize_hostname("bad host.example.com", "example.com"))

    def test_bruteforce_empty_domain_returns_empty(self) -> None:
        self.assertEqual(brute_force_subdomains("", prefixes=["api"], shuffle=False), [])

    @patch("discovery.requests.get")
    def test_fetch_subdomains_filters_crtsh_values(self, get_mock: Mock) -> None:
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = [
            {"name_value": "*.api.example.com\nsub.example.com.\nnotexample.com"},
            {"name_value": "EXAMPLE.COM"},
        ]
        get_mock.return_value = response

        result = fetch_subdomains_from_crtsh("Example.com.")
        self.assertEqual(result, ["api.example.com", "example.com", "sub.example.com"])


if __name__ == "__main__":
    unittest.main()
