from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stdout

from hello_provenance.cli import main


class CliTests(unittest.TestCase):
    def test_text_output(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            status = main(["--name", "team"])
        self.assertEqual(status, 0)
        self.assertIn("Hello, team", buffer.getvalue())

    def test_json_output(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            status = main(["--name", "team", "--json"])
        self.assertEqual(status, 0)
        payload = json.loads(buffer.getvalue())
        self.assertEqual(payload["app"], "hello-provenance-demo")
        self.assertIn("team", payload["message"])


if __name__ == "__main__":
    unittest.main()
