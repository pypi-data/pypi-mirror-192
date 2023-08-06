from __future__ import annotations

import contextlib
import logging
import pathlib
import re
import threading
from datetime import datetime
from io import TextIOWrapper
from time import sleep
from types import TracebackType
from typing import Any
from typing import Generator
from typing import Literal

from serial import Serial
from serial.threaded import LineReader


logger = logging.getLogger(__name__)


def filter_ansi_escape(line: str) -> str:
    COLOR_ESC = r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
    ESC_CHARS = r"[\x00-\x09]|[\x0B-\x1F]"
    ansi_escape = re.compile(f"{COLOR_ESC}|{ESC_CHARS}")
    return ansi_escape.sub("", line)


def add_line_timestamp(line: str) -> str:
    def timestamp() -> str:
        return datetime.now().strftime("[%H:%M:%S.%f]")

    return f"{timestamp()} {line}"


class Sniffer(LineReader):
    TERMINATOR = b"\n"
    log_file: TextIOWrapper | None

    def __init__(
        self,
        clean_line: bool = True,
        add_timestamp: bool = True,
    ) -> None:
        super().__init__()
        self.clean_line = clean_line
        self.add_timestamp = add_timestamp
        self.log_file = None

    def handle_line(self, data: str) -> None:
        if self.log_file is not None:
            if self.clean_line:
                data = filter_ansi_escape(data)
            if self.add_timestamp:
                data = add_line_timestamp(data)
            self.log_file.write(f"{data}\n")


class ReaderThread(threading.Thread):
    def __init__(self, serial: Serial, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.serial = serial
        self.alive = True

    def stop(self) -> None:
        self.alive = False
        self.serial.cancel_read()
        self.join(5)

    def run(self) -> None:
        while self.alive and self.serial.is_open:
            try:
                self.serial.read(self.serial.in_waiting or 1)
            except self.serial.SerialException:
                break
        self.alive = False

    def __enter__(self) -> ReaderThread:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        self.stop()
        if exc_type or exc or traceback:
            return False
        else:
            return None


class SerialSniffer(Serial):
    sniff_thread: ReaderThread
    timeout: float

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.protocol = Sniffer()
        self._sniffing = False

    def read(self, size: int = 1) -> bytes:
        data = super().read(size)
        self.protocol.data_received(data)
        return data

    @contextlib.contextmanager
    def change_timeout_ctx(
        self,
        timeout: float,
    ) -> Generator[None, None, None]:
        orig_timeout = self.timeout
        try:
            self.timeout = timeout
            yield
        finally:
            self.timeout = orig_timeout

    def start_sniffing(self) -> ReaderThread:
        self.sniff_thread = ReaderThread(self)
        self.sniff_thread.start()
        self._sniffing = True
        return self.sniff_thread

    def stop_sniffing(self) -> None:
        if not self._sniffing:
            return None

        self.sniff_thread.stop()
        self._sniffing = False


class Component:
    def __init__(self, name: str, port: str) -> None:
        self.logger = logging.getLogger(name)
        self.name = name
        self.serial = SerialSniffer(port=port, baudrate=115200, timeout=5)

    @property
    def prompt(self) -> bytes:
        raise NotImplementedError

    @contextlib.contextmanager
    def sniff(
        self,
        log_file: pathlib.Path | str,
        mode: Literal["w", "a"] = "a",
    ) -> Generator[None, None, None]:
        self.config_serial_log_file(log_file, mode)
        try:
            self.serial.start_sniffing()
            self.serial._sniffing = True
            yield
        finally:
            if self.serial._sniffing:
                self.serial.stop_sniffing()
            self.serial._sniffing = False

    def run_serial_cmd(self, cmd: str) -> None:
        self.logger.debug(f"[serial] running cmd: {cmd!r}")
        cmd_b = cmd.encode()
        cmd_b += b"\n"
        for b in cmd_b:
            self.serial.write(bytes([b]))
            sleep(0.01)
        sleep(0.4)

    def config_serial_log_file(
        self,
        log_file: pathlib.Path | str,
        mode: Literal["w", "a"] = "a",
    ) -> None:
        if self.serial._sniffing:
            self.serial.stop_sniffing()
            assert self.serial.protocol.log_file
            self.serial.protocol.log_file.close()

        self.logger.debug(f"configuring log file for serial: {log_file}")
        log_file = pathlib.Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        self.serial.protocol.log_file = log_file.open(mode, buffering=1)

    def wait_for_msg(self, msg: bytes, timeout: float) -> bytes:
        self.logger.debug(f"waiting for msg {msg.decode()!r}")

        restart_sniffing = False
        if self.serial._sniffing:
            restart_sniffing = True
            self.serial.stop_sniffing()

        with self.serial.change_timeout_ctx(timeout):
            if not self.serial.is_open:
                self.serial.open()
            res = self.serial.read_until(msg)

        if restart_sniffing:
            self.serial.start_sniffing()

        return res

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
