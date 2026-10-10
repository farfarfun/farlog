import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))


class FarlogTest(unittest.TestCase):
    def test_logger_lifecycle(self):
        from loguru import logger

        previous_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            try:
                logger.remove()
                host_messages = []
                logger.add(host_messages.append, format="{message}")

                import farlog

                self.assertFalse(Path("logs").exists())
                logger.info("host handler preserved")
                self.assertEqual(str(host_messages[0]), "host handler preserved\n")

                first = farlog.get_logger()
                self.assertIs(first, farlog.get_logger("default"))
                self.assertIs(first, farlog.get_logger(name="default"))
                first.info("once")

                updated = farlog.get_logger("default", level="DEBUG")
                self.assertIs(first, updated)
                updated.info("twice")

                named_log = Path("logs/default.log").read_text()
                self.assertEqual(named_log.count("once"), 1)
                self.assertEqual(named_log.count("twice"), 1)

                stderr = io.StringIO()
                with redirect_stderr(stderr):
                    farlog.configure("var/log")
                    logger.info("unbound")
                    updated.info("after configure")

                self.assertIn("unbound", Path("var/log/all.log").read_text())
                self.assertIn(
                    "after configure", Path("var/log/default.log").read_text()
                )
                self.assertNotIn("Logging error", stderr.getvalue())

                with self.assertRaises(ValueError):
                    farlog.get_logger("../escaped")
                self.assertFalse(any(Path(".").rglob("escaped.log")))
            finally:
                logger.remove()
                os.chdir(previous_cwd)

    def test_compatibility_api_and_configure_options(self):
        from loguru import logger

        import farlog
        from farlog import core

        previous_cwd = Path.cwd()
        previous_log_dir = core._log_dir
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                os.chdir(temp_dir)
                logger.remove()
                core._loggers.clear()
                core._log_dir = Path("logs")

                compatibility_logger = farlog.getLogger("compat", formatter="{message}")
                self.assertIs(
                    compatibility_logger,
                    farlog.get_logger("compat", formatter="{message}"),
                )
                compatibility_logger.info("custom format")
                self.assertEqual(Path("logs/compat.log").read_text(), "custom format\n")

                farlog.configure(Path("first"))
                compatibility_logger.info("first configuration")
                farlog.configure(Path("second"))
                compatibility_logger.info("second configuration")

                self.assertIn(
                    "first configuration", Path("first/compat.log").read_text()
                )
                self.assertIn(
                    "second configuration", Path("second/compat.log").read_text()
                )
                self.assertIn(
                    "second configuration", Path("second/all.log").read_text()
                )

                for invalid_name in (None, "", ".", "..", "nested/name"):
                    with self.subTest(name=invalid_name), self.assertRaises(ValueError):
                        farlog.get_logger(invalid_name)
        finally:
            core._loggers.clear()
            core._log_dir = previous_log_dir
            logger.remove()
            os.chdir(previous_cwd)


if __name__ == "__main__":
    unittest.main()
