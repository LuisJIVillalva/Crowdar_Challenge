import logging

_logger = logging.getLogger("automation")


class log:
    @staticmethod
    def info(message):
        _logger.info(message)

    @staticmethod
    def test(message):
        _logger.info(f"[TEST] {message}")

    @staticmethod
    def config(message):
        _logger.info(f"[CONFIG] {message}")

    @staticmethod
    def warning(message):
        _logger.warning(message)

    @staticmethod
    def error(message):
        _logger.error(message)
