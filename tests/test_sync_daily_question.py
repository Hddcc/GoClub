from contextlib import redirect_stderr
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from scripts.sync_daily_question import (
    main,
    parse_submission_date,
    prepare_submission,
    sanitize_markdown,
    sync_file,
    update_content,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "sync_daily_question.py"


class SubmissionDateTests(unittest.TestCase):
    def test_converts_utc_timestamp_to_shanghai_date(self):
        self.assertEqual(
            parse_submission_date("2026-08-01T16:30:00Z"),
            "2026.08.02",
        )

    def test_converts_timestamp_from_another_offset_at_midnight_boundary(self):
        self.assertEqual(
            parse_submission_date("2026-08-02T00:30:00+09:00"),
            "2026.08.01",
        )

    def test_rejects_invalid_or_timezone_free_timestamp(self):
        for value in ["2026-08-02T09:00:00", "无效时间"]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_submission_date(value)


class SubmissionValidationTests(unittest.TestCase):
    def test_normalizes_question_and_preserves_answer_markdown(self):
        submission = prepare_submission(
            "  Go 的调度器\n如何工作？  ",
            "\n- GMP 模型\n- 工作窃取\n",
            "2026-08-02T09:00:00+08:00",
        )

        self.assertEqual(submission.question, "Go 的调度器 如何工作？")
        self.assertEqual(submission.answer, "- GMP 模型\n- 工作窃取")
        self.assertEqual(submission.date, "2026.08.02")

    def test_rejects_blank_question_or_answer(self):
        cases = [
            ("   ", "有效答案"),
            ("有效题目", "\n\t"),
        ]

        for question, answer in cases:
            with self.subTest(question=question, answer=answer):
                with self.assertRaises(ValueError):
                    prepare_submission(
                        question,
                        answer,
                        "2026-08-02T09:00:00+08:00",
                    )

    def test_enforces_question_and_answer_length_limits(self):
        timestamp = "2026-08-02T09:00:00+08:00"

        prepare_submission("题" * 500, "答" * 20000, timestamp)

        for question, answer in [
            ("题" * 501, "有效答案"),
            ("有效题目", "答" * 20001),
        ]:
            with self.assertRaises(ValueError):
                prepare_submission(question, answer, timestamp)


class MarkdownSafetyTests(unittest.TestCase):
    def test_escapes_raw_html_without_breaking_markdown_code(self):
        source = (
            "<script>alert('x')</script>\n"
            "- [参考](https://example.com?a=1&b=2)\n"
            "- `<span onclick=\"bad()\">示例</span>`\n"
            "```html\n"
            "<button onclick=\"bad()\">按钮</button>\n"
            "```"
        )

        self.assertEqual(
            sanitize_markdown(source),
            "&lt;script&gt;alert('x')&lt;/script&gt;\n"
            "- [参考](https://example.com?a=1&amp;b=2)\n"
            "- `<span onclick=\"bad()\">示例</span>`\n"
            "```html\n"
            "<button onclick=\"bad()\">按钮</button>\n"
            "```",
        )


class DailyQuestionContentTests(unittest.TestCase):
    def test_inserts_new_submission_before_first_existing_date(self):
        existing = (
            "---\r\n"
            'title: "每日一问"\r\n'
            "---\r\n\r\n"
            "# 每日一问\r\n\r\n"
            "记录微信交流群中每天的提问。\r\n\r\n"
            "## 2026.08.01\r\n\r\n"
            "### 历史题目\r\n\r\n"
            "历史答案\r\n"
        )
        submission = prepare_submission(
            "新的 <调度> 题目",
            "- 第一项\n- `x < y`",
            "2026-08-02T09:00:00+08:00",
        )

        updated, changed = update_content(existing, submission)

        self.assertTrue(changed)
        self.assertEqual(
            updated,
            "---\r\n"
            'title: "每日一问"\r\n'
            "---\r\n\r\n"
            "# 每日一问\r\n\r\n"
            "记录微信交流群中每天的提问。\r\n\r\n"
            "## 2026.08.02\r\n\r\n"
            "### 新的 &lt;调度&gt; 题目\r\n\r\n"
            "- 第一项\r\n- `x < y`\r\n\r\n"
            "## 2026.08.01\r\n\r\n"
            "### 历史题目\r\n\r\n"
            "历史答案\r\n",
        )

    def test_returns_original_content_when_date_already_exists(self):
        existing = "说明\n\n## 2026.08.02\n\n### 已有题目\n\n已有答案\n"
        submission = prepare_submission(
            "另一道题",
            "另一个答案",
            "2026-08-02T18:00:00+08:00",
        )

        updated, changed = update_content(existing, submission)

        self.assertFalse(changed)
        self.assertEqual(updated, existing)

    def test_does_not_treat_a_similar_date_heading_as_a_duplicate(self):
        existing = "说明\n\n## 2026.08.020\n\n相似日期\n"
        submission = prepare_submission(
            "有效题目",
            "有效答案",
            "2026-08-02T18:00:00+08:00",
        )

        updated, changed = update_content(existing, submission)

        self.assertTrue(changed)
        self.assertIn("## 2026.08.02\n\n### 有效题目", updated)


class FileSyncTests(unittest.TestCase):
    def test_writes_updated_content_to_file(self):
        with tempfile.TemporaryDirectory() as directory:
            content_path = Path(directory) / "每日一问.md"
            content_path.write_text(
                "说明\n\n## 2026.08.01\n\n### 历史题目\n\n历史答案\n",
                encoding="utf-8",
                newline="",
            )
            submission = prepare_submission(
                "新题目",
                "新答案",
                "2026-08-02T09:00:00+08:00",
            )

            changed = sync_file(content_path, submission)

            self.assertTrue(changed)
            self.assertIn(
                "## 2026.08.02\n\n### 新题目\n\n新答案",
                content_path.read_text(encoding="utf-8"),
            )

    def test_replace_failure_keeps_original_file_and_removes_temporary_file(self):
        with tempfile.TemporaryDirectory() as directory:
            content_path = Path(directory) / "每日一问.md"
            original = "说明\n\n## 2026.08.01\n\n### 历史题目\n\n历史答案\n"
            content_path.write_text(original, encoding="utf-8", newline="")
            submission = prepare_submission(
                "新题目",
                "新答案",
                "2026-08-02T09:00:00+08:00",
            )

            with mock.patch(
                "scripts.sync_daily_question.os.replace",
                side_effect=OSError("模拟替换失败"),
            ):
                with self.assertRaises(OSError):
                    sync_file(content_path, submission)

            self.assertEqual(
                content_path.read_text(encoding="utf-8"),
                original,
            )
            self.assertEqual(list(Path(directory).iterdir()), [content_path])


class CommandBehaviorTests(unittest.TestCase):
    def _run_command(self, payload_path, content_path):
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--payload",
                str(payload_path),
                "--content",
                str(content_path),
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=environment,
            check=False,
        )

    def test_success_then_duplicate_reports_expected_result(self):
        with tempfile.TemporaryDirectory() as directory:
            content_path = Path(directory) / "每日一问.md"
            payload_path = Path(directory) / "event.json"
            original = "说明\n\n## 2026.08.01\n\n### 历史题目\n\n历史答案\n"
            content_path.write_text(original, encoding="utf-8", newline="")
            payload_path.write_text(
                json.dumps(
                    {
                        "inputs": {
                            "question": "比较 <tag>",
                            "answer": "- [链接](https://example.com?a=1&b=2)\n- `x < y`",
                            "submitted_at": "2026-08-02T09:00:00+08:00",
                        }
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            first = self._run_command(payload_path, content_path)
            after_first = content_path.read_text(encoding="utf-8")
            second = self._run_command(payload_path, content_path)

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(first.stdout.strip(), "已更新")
            self.assertIn("### 比较 &lt;tag&gt;", after_first)
            self.assertIn("- `x < y`", after_first)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(second.stdout.strip(), "无变更")
            self.assertEqual(content_path.read_text(encoding="utf-8"), after_first)

    def test_invalid_payload_fails_without_changing_content(self):
        with tempfile.TemporaryDirectory() as directory:
            content_path = Path(directory) / "每日一问.md"
            payload_path = Path(directory) / "event.json"
            original = "说明\n\n## 2026.08.01\n\n历史内容\n"
            content_path.write_text(original, encoding="utf-8", newline="")
            payload_path.write_text(
                json.dumps(
                    {
                        "inputs": {
                            "question": "有效题目",
                            "answer": "   ",
                            "submitted_at": "2026-08-02T09:00:00+08:00",
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = self._run_command(payload_path, content_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("答案不能为空", result.stderr)
            self.assertEqual(content_path.read_text(encoding="utf-8"), original)

    def test_replace_failure_is_reported_without_changing_content(self):
        with tempfile.TemporaryDirectory() as directory:
            content_path = Path(directory) / "每日一问.md"
            payload_path = Path(directory) / "event.json"
            original = "说明\n\n## 2026.08.01\n\n历史内容\n"
            content_path.write_text(original, encoding="utf-8", newline="")
            payload_path.write_text(
                json.dumps(
                    {
                        "inputs": {
                            "question": "有效题目",
                            "answer": "有效答案",
                            "submitted_at": "2026-08-02T09:00:00+08:00",
                        }
                    }
                ),
                encoding="utf-8",
            )
            stderr = io.StringIO()

            with mock.patch(
                "scripts.sync_daily_question.os.replace",
                side_effect=OSError("模拟替换失败"),
            ):
                with redirect_stderr(stderr):
                    exit_code = main(
                        [
                            "--payload",
                            str(payload_path),
                            "--content",
                            str(content_path),
                        ]
                    )

            self.assertNotEqual(exit_code, 0)
            self.assertIn("模拟替换失败", stderr.getvalue())
            self.assertEqual(content_path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
