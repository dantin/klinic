# -*- coding: utf-8 -*-

import logging
from unittest.mock import MagicMock

from klinic.utils.logging_configurator import LoggingConfigurator


def reset_logging():
    # work around all of the import side-effects in superset
    logging.root.manager.loggerDict = {}
    logging.root.handlers = []


def test_configurator_adding_handler():
    class MyEventHandler(logging.Handler):
        def __init__(self):
            super().__init__(level=logging.DEBUG)
            self.received = False

        def handle(self, record):
            if hasattr(record, "testattr"):
                self.received = True

    class MyConfigurator(LoggingConfigurator):
        def __init__(self, handler):
            self.handler = handler

        def configure_logging(self, app_config, debug_mode):
            super().configure_logging(app_config, debug_mode)
            logging.getLogger().addHandler(self.handler)

    reset_logging()

    handler = MyEventHandler()
    cfg = MyConfigurator(handler)
    cfg.configure_logging(MagicMock(), True)

    logging.info("test", extra={"testattr": "foo"})
    assert not handler.received
