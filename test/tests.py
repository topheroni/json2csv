import json
import pathlib
import unittest
from typing import Any

CWD = pathlib.Path(__file__).resolve().parent
with open(f"{CWD}/test_input.json", "r") as f:
    d_f = json.load(f)
print(CWD)


def headers(d: dict[str, Any]):
    h = []
    for k, v in d.items():
        h.append(k)
        if isinstance(v, dict):
            h.extend(headers(v))
    return h


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
