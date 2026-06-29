import unittest

from click.testing import CliRunner

from context import AppContext
import commands.mailings as mailings


class _FakeClient:
    def __init__(self, mailing_name: str, pdf_name: str | None = None) -> None:
        self.mailing_name = mailing_name
        self.pdf_name = pdf_name
        self.get_calls: list[tuple[str, bool]] = []

    def get(self, path: str, params=None, expect_json: bool = True):
        self.get_calls.append((path, expect_json))
        if path.endswith("/plaintext"):
            return "hello world"
        if "/mailings/" in path:
            return {"name": self.mailing_name, "pdf_name": self.pdf_name}
        raise AssertionError(f"Unexpected GET path: {path}")

    def get_binary(self, path: str):
        if path.endswith("/pdf") or path.endswith("/zip"):
            return b"binary"
        raise AssertionError(f"Unexpected binary path: {path}")


class _OutputCapture:
    def __init__(self) -> None:
        self.binary_calls: list[tuple[str | None, str]] = []
        self.text_calls: list[tuple[str | None, str]] = []

    def save_binary(self, data: bytes, path: str | None, default_name: str) -> str:
        self.binary_calls.append((path, default_name))
        return default_name

    def save_text(self, text: str, path: str | None, default_name: str) -> str:
        self.text_calls.append((path, default_name))
        return default_name


class MailingsExportFilenameTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()
        self.original_output = mailings.output

    def tearDown(self) -> None:
        mailings.output = self.original_output

    def _invoke(self, command: str, args: list[str], name: str = "Invoice 01", pdf_name: str | None = None):
        fake_client = _FakeClient(name, pdf_name=pdf_name)
        app = AppContext(client=fake_client, scanbox_id=77)
        capture = _OutputCapture()
        mailings.output = capture

        result = self.runner.invoke(mailings.mailings_group, [command, "abc-123", *args], obj=app)
        self.assertEqual(result.exit_code, 0, result.output)
        return fake_client, capture

    def test_default_uses_show_pdf_name_with_matching_extension(self) -> None:
        cases = [
            ("pdf", ".pdf", "binary"),
            ("plaintext", ".txt", "text"),
            ("zip", ".zip", "binary"),
        ]

        for command, extension, mode in cases:
            with self.subTest(command=command):
                fake_client, capture = self._invoke(
                    command,
                    ["--scanbox", "123"],
                    name="Ignored Name",
                    pdf_name="My/Letter.pdf",
                )

                if mode == "binary":
                    self.assertEqual(capture.binary_calls, [(None, f"My_Letter{extension}")])
                    self.assertEqual(capture.text_calls, [])
                else:
                    self.assertEqual(capture.text_calls, [(None, f"My_Letter{extension}")])
                    self.assertEqual(capture.binary_calls, [])

                self.assertIn(("/scanboxes/123/mailings/abc-123", True), fake_client.get_calls)

    def test_default_falls_back_to_show_name_when_pdf_name_missing(self) -> None:
        fake_client, capture = self._invoke("pdf", ["--scanbox", "123"], name="My/Letter", pdf_name=None)

        self.assertEqual(capture.binary_calls, [(None, "My_Letter.pdf")])
        self.assertEqual(capture.text_calls, [])
        self.assertIn(("/scanboxes/123/mailings/abc-123", True), fake_client.get_calls)

    def test_uuid_flag_uses_uuid_filename(self) -> None:
        cases = [
            ("pdf", ".pdf", "binary"),
            ("plaintext", ".txt", "text"),
            ("zip", ".zip", "binary"),
        ]

        for command, extension, mode in cases:
            with self.subTest(command=command):
                fake_client, capture = self._invoke(command, ["--scanbox", "123", "--uuid"])

                if mode == "binary":
                    self.assertEqual(capture.binary_calls, [(None, f"abc-123{extension}")])
                    self.assertEqual(capture.text_calls, [])
                else:
                    self.assertEqual(capture.text_calls, [(None, f"abc-123{extension}")])
                    self.assertEqual(capture.binary_calls, [])

                self.assertNotIn(("/scanboxes/123/mailings/abc-123", True), fake_client.get_calls)

    def test_output_path_overrides_default_filename(self) -> None:
        cases = [
            ("pdf", "binary"),
            ("plaintext", "text"),
            ("zip", "binary"),
        ]

        for command, mode in cases:
            with self.subTest(command=command):
                fake_client, capture = self._invoke(command, ["--scanbox", "123", "-o", "out.custom"])

                if mode == "binary":
                    self.assertEqual(capture.binary_calls, [("out.custom", "abc-123." + command if command != "zip" else "abc-123.zip")])
                    self.assertEqual(capture.text_calls, [])
                else:
                    self.assertEqual(capture.text_calls, [("out.custom", "abc-123.txt")])
                    self.assertEqual(capture.binary_calls, [])

                self.assertNotIn(("/scanboxes/123/mailings/abc-123", True), fake_client.get_calls)


if __name__ == "__main__":
    unittest.main()
