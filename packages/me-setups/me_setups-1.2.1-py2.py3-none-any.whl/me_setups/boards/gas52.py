from __future__ import annotations

import contextlib
import functools
import logging
import pathlib
import time
from concurrent.futures import ThreadPoolExecutor
from subprocess import CompletedProcess
from typing import Generator
from typing import Literal

from me_setups.boards.types import BoardType
from me_setups.components import const as C
from me_setups.components.eqs import EyeQ5
from me_setups.components.eqs import OSType
from me_setups.components.mcs import Mcs
from me_setups.components.mcu import Mcu
from me_setups.components.mcu import McuType


class Gas52Board:
    eqs: list[EyeQ5]
    mcu: Mcu

    def __init__(
        self,
        eqs: dict[str, str] = C.GAS52_EQS,
        mcu: tuple[str, str] = C.GAS52_MCU,
        board_type: BoardType = BoardType.GAS52,
        board_rev: str = "0x3",
        os_type: OSType | None = None,
        mcu_type: McuType | None = None,
        mcs: Mcs | None = None,
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.eqs = self._generate_eqs(eqs, os_type)
        self.mcu = Mcu(mcu[0], mcu[1], board_type, mcu_type)
        self.board_type = board_type
        self.os_type = os_type
        self.mcu_type = mcu_type
        self.board_rev = board_rev
        self._mcs = mcs
        self._sniffing = False

    @functools.cached_property
    def conns(self) -> list[EyeQ5 | Mcu | Mcs] | list[EyeQ5 | Mcu]:
        conns: list[EyeQ5 | Mcu | Mcs] | list[EyeQ5 | Mcu]
        conns = self.eqs + [self.mcu]
        if self.mcs is not None:
            conns = conns + [self.mcs]
        return conns

    @functools.cached_property
    def shiq(self) -> EyeQ5:
        return self.eqs[1]

    @functools.cached_property
    def mcs(self) -> Mcs | None:
        if self._mcs is None:
            if pathlib.Path("/dev/MCS").exists():
                self._mcs = Mcs(C.MCS[0], C.MCS[1])

        return self._mcs

    @property
    def board_name(self) -> str:
        if self.board_type == BoardType.GAS52:
            return "GAS52-B4"
        elif self.board_type == BoardType.EVO:
            if self.board_rev == "0x1":
                return "GAS52-EVO_B-B1"
            elif self.board_rev == "0x2":
                return "GAS52-EVO_B-C1"
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    @contextlib.contextmanager
    def sniff(
        self,
        log_folder: pathlib.Path | str,
        mode: Literal["a", "w"] = "a",
    ) -> Generator[None, None, None]:
        self.config_log_files(log_folder, mode)
        try:
            self.start_sniffing()
            yield
        finally:
            if self._sniffing:
                self.stop_sniffing()

    def start_sniffing(self) -> None:
        if self._sniffing:
            return None

        self._sniffing = True
        for conn in self.conns:
            conn.serial.start_sniffing()

    def stop_sniffing(self) -> None:
        if not self._sniffing:
            return None

        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            executor.map(
                lambda conn: conn.serial.stop_sniffing(),
                self.conns,
            )
        self._sniffing = False

    def get_eyeq(self, chip: int, mid: int) -> EyeQ5:
        return self.eqs[chip * 2 + mid]

    def config_log_files(
        self,
        log_folder: pathlib.Path | str,
        mode: Literal["w", "a"] = "a",
    ) -> None:
        self.logger.debug(f"configuring log folder {log_folder}")
        log_folder = pathlib.Path(log_folder)
        for conn in self.conns:
            conn.config_serial_log_file(log_folder / f"{conn.name}.log", mode)

    def close_serials(self) -> None:
        for conn in self.conns:
            conn.logger.debug("closing serial")
            conn.serial.close()

    def open_serials(self) -> None:
        for conn in self.conns:
            if not conn.serial.is_open:
                conn.logger.debug("opening serial")
                conn.serial.open()

    def restart_serials(self) -> None:
        self.close_serials()
        self.open_serials()

    def run_ssh_cmd_all(self, cmd: str) -> list[CompletedProcess[str]]:
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            results = executor.map(
                lambda eq: eq.run_ssh_cmd(cmd),
                self.eqs,
            )
        return list(results)

    def wait_for_msg_all(self, msg: bytes, timeout: float) -> bool:
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            results = executor.map(
                lambda eq: eq.wait_for_msg(msg, timeout),
                self.eqs,
            )
        return all(results)

    def wait_for_linux_boot(self) -> bool:
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            results = executor.map(
                lambda eq: eq.wait_for_linux_boot(),
                self.eqs,
            )
        return all(results)

    def reboot(self, *, sleep_after: int = 0) -> None:
        if self.board_type == BoardType.EVO:
            raise NotImplementedError("reboot is not support on EVO")

        self.logger.info("rebooting platform...")

        if self.mcs is not None:
            self.logger.debug("rebooting MCS")
            self.mcs.run_serial_cmd("reboot")

        self.logger.debug("rebooting board")
        self.mcu.run_serial_cmd("reboot")

        if sleep_after > 0:
            self.logger.info(f"sleeping for {sleep_after} seconds.")
            time.sleep(sleep_after)

    def _generate_eq(
        self,
        eq_name: str,
        eq_port: str,
        os_type: OSType | None = None,
    ) -> EyeQ5:
        self.logger.debug(f"generating eyeq {eq_name}")
        if os_type is not None:
            eq = EyeQ5(eq_name, eq_port, os_type)
        else:
            eq = EyeQ5(eq_name, eq_port, OSType.LINUX)
        return eq

    def _generate_eqs(
        self,
        eqs: dict[str, str],
        os_type: OSType | None = None,
    ) -> list[EyeQ5]:
        return [
            self._generate_eq(eq_name, eq_port, os_type)
            for eq_name, eq_port in eqs.items()  # for black format
        ]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(eqs={self.eqs}, mcu={self.mcu})"
