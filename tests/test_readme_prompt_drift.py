from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCALIZED_READMES = (
    "README.ko.md",
    "README.ja.md",
    "README.zh-CN.md",
)
PROMPT_MARKERS = (
    "Ask an agent:",
    "Read ./harness-starter-kit",
    "Requirements:",
)


def agent_prompt_blocks(readme: Path) -> list[str]:
    text = readme.read_text(encoding="utf-8")
    blocks = re.findall(r"```text\n(.*?)\n```", text, flags=re.DOTALL)
    return [
        block
        for block in blocks
        if any(marker in block for marker in PROMPT_MARKERS)
    ]


class ReadmePromptDriftTests(unittest.TestCase):
    def test_localized_readmes_are_valid_utf8(self) -> None:
        for filename in LOCALIZED_READMES:
            with self.subTest(readme=filename):
                path = REPO_ROOT / filename
                try:
                    path.read_bytes().decode("utf-8")
                except UnicodeDecodeError as exc:
                    self.fail(
                        f"{filename} is not valid UTF-8 at byte {exc.start}: "
                        f"{exc.reason}"
                    )

    def test_first_localized_readme_agent_prompt_stays_english(self) -> None:
        expected_blocks = agent_prompt_blocks(REPO_ROOT / "README.md")
        self.assertGreaterEqual(len(expected_blocks), 1)
        expected = expected_blocks[0]

        for filename in LOCALIZED_READMES:
            with self.subTest(readme=filename):
                actual = agent_prompt_blocks(REPO_ROOT / filename)
                self.assertGreaterEqual(len(actual), 1)
                self.assertEqual(expected, actual[0])


if __name__ == "__main__":
    unittest.main()
