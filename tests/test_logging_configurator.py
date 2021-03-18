# -*- coding: utf-8 -*-

import logging

from klinic.utils.logging_configurator import LoggingConfigurator


def reset_logging():
    # work around all of the import side-effects.
    logging.root.manager.loggerDict = {}
    logging.root.handlers = []


def test_configurator_adding_handler(mocker):
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
    cfg.configure_logging(mocker.patch('flask.config.Config'), True)

    logging.info("test", extra={"testattr": "foo"})
    assert not handler.received
