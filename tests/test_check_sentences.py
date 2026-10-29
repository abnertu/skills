"""Check fenced-code exclusion through the sentence checker's CLI."""

import pathlib
import subprocess
import sys
import tempfile
import unittest


SCRIPT = (
    pathlib.Path(__file__).resolve().parents[1]
    / "skills/setup-repo-docs/scripts/check-sentences.py"
)
SENTENCE = " ".join(["word"] * 21) + "."


class CodeFenceTests(unittest.TestCase):
    def assert_reports(self, lines, expected_lines):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "input.md"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True,
                text=True,
                check=True,
            )
            expected = "".join(
                f"{path}:{number}: 21 words: {SENTENCE}\n"
                for number in expected_lines
            )
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.stderr, "")

    def test_nested_fences_stay_inside_the_outer_block(self):
        for marker in ("`", "~"):
            for close_inner in (False, True):
                with self.subTest(marker=marker, close_inner=close_inner):
                    lines = [marker * 4 + "markdown", marker * 3 + "yaml", SENTENCE]
                    if close_inner:
                        lines.append(marker * 3)
                    lines.extend([marker * 4, SENTENCE])
                    self.assert_reports(lines, [len(lines)])

    def test_invalid_closers_leave_the_block_open(self):
        for opening, invalid in (
            ("````", "```"),
            ("~~~~", "~~~"),
            ("```", "~~~"),
            ("~~~", "```"),
            ("```", "```python"),
            ("~~~", "~~~ text"),
        ):
            with self.subTest(opening=opening, invalid=invalid):
                self.assert_reports(
                    [opening, invalid, SENTENCE, opening, SENTENCE], [5]
                )

    def test_matching_or_longer_closers_resume_prose_checks(self):
        for opening, closing in (
            ("```python", "```"),
            ("~~~python", "~~~"),
            ("````", "`````"),
            ("~~~~", "~~~~~"),
            ("```", "``` \t"),
        ):
            with self.subTest(opening=opening, closing=closing):
                self.assert_reports([opening, SENTENCE, closing, SENTENCE], [4])

    def test_backticks_in_backtick_info_do_not_open_a_block(self):
        self.assert_reports(["```example `code`", SENTENCE], [2])

    def test_backticks_in_tilde_info_are_allowed(self):
        self.assert_reports(["~~~example `code`", SENTENCE, "~~~", SENTENCE], [4])

    def test_unclosed_fence_excludes_the_rest_of_the_file(self):
        self.assert_reports([SENTENCE, "```", SENTENCE], [1])


if __name__ == "__main__":
    unittest.main()
