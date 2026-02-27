import unittest

from validation import normalize_host, normalize_hosts, normalize_proxies


class ValidationTests(unittest.TestCase):
    def test_normalize_host(self) -> None:
        self.assertEqual(normalize_host(" Example.COM. "), "example.com")
        self.assertIsNone(normalize_host("bad host"))

    def test_normalize_hosts_dedupe_and_invalid(self) -> None:
        valid, invalid = normalize_hosts(["A.com", "a.com.", "bad host", ""])
        self.assertEqual(valid, ["a.com"])
        self.assertEqual(invalid, ["bad host"])

    def test_normalize_proxies(self) -> None:
        valid, invalid = normalize_proxies("1.1.1.1:80, bad,2.2.2.2:70000,1.1.1.1:80")
        self.assertEqual(valid, ["1.1.1.1:80"])
        self.assertEqual(invalid, ["bad", "2.2.2.2:70000"])


if __name__ == "__main__":
    unittest.main()
