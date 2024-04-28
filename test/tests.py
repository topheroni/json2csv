import json
import unittest
from typing import Any


def headers(d: dict[str, Any]):
    h = []
    for k, v in d.items():
        h.append(k)
        if isinstance(v, dict):
            h.extend(headers(v))
    return h


with open("test_input.json", "r") as f:
    d_f = json.load(f)


class ConversionTest(unittest.TestCase):
    def test_headers(self):
        self.assertEqual(
            [
                "first_name",
                "last_name",
                "address",
                "street1",
                "street2",
                "city",
                "state",
                "zip",
            ],
            headers(d_f),
        )


if __name__ == "__main__":
    unittest.main()
