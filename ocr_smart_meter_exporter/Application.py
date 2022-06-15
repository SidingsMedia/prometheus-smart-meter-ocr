# SPDX-FileCopyrightText: 2022 Sidings Media <contact@sidingsmedia.com>
# SPDX-License-Identifier: MIT

import sys

from prometheus_client.core import REGISTRY
from prometheus_client import start_http_server

from .__version__ import __title__, __description__, __version__, __copyright__, __license__
from .Logging import log
from .OCRCollector import OCRCollector
from .ocr import OCR


class Application:
    """
    Main entrypoint into application

    This class represents the main entry point into the application and
    only one instance of it should be created per application.
    """

    def __init__(self) -> None:
        """
        __init__ Create instance of Application
        """

        self._ouputInfo()

        self._port = 8000
        self._ocr = OCR(log)

        log.debug("EXPORTER", "Registering OCR Collector")
        REGISTRY.register(OCRCollector(self._ocr))

    def run(self) -> int:
        """
        run Run the application

        Main loop of the application.
        """

        self._startServer()

        try:
            while True:
                pass
        except KeyboardInterrupt as e:
            log.info("APPLICATION", "Keyboard interupt detected, shutting down")
            self._halt()

    def _startServer(self) -> None:
        """
        _startServer Start the prometheus web server
        """

        log.info("WEB SERVER", f"Starting the Prometheus metrics server on port {self._port}")

        try:
            start_http_server(port=self._port)
        except Exception as e:
            log.error("WEB SERVER", f"Unhandled exception: {e}")
            self._halt(1)
        else:
            log.info("WEB SERVER", "Successfully started server")

    def _ouputInfo(self) -> None:
        """
        _ouputInfo Output application info to stdout
        """

        print(__title__)
        print(__description__)
        print(f"Version: {__version__}")
        print(f"Copyright: {__copyright__}")
        print(f"License: {__license__}")

    def _halt(self, status: int = 0) -> None:
        """
        _halt End the program

        Exit the program after cleaning up by using sys.exit()

        :param status: Exit code. 0 = success. Any other value means
            error, defaults to 0
        :type status: int, optional
        """

        log.info("APPLICATION", "Final shutdown message")
        sys.exit(status)