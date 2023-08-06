from __future__ import annotations

from enum import Enum


class OSType(Enum):
    VOIS = "VOiS"
    UBOOT = "U-Boot"
    LINUX = "Linux"


class McuType(Enum):
    MEAVES = "meaves"
    ADAM = "adam"
    ASR = "asr"


GAS52_EQS_IPS = {
    "EQ5_PBCM_0000": {
        OSType.LINUX: "192.168.19.129",
        OSType.VOIS: "169.254.0.11",
        OSType.UBOOT: None,
    },
    "EQ5_PBCM_0001": {
        OSType.LINUX: "192.168.19.113",
        OSType.VOIS: "169.254.0.12",
        OSType.UBOOT: None,
    },
    "EQ5_PBCM_0010": {
        OSType.LINUX: "192.168.19.105",
        OSType.VOIS: "169.254.0.13",
        OSType.UBOOT: None,
    },
    "EQ5_PBCM_0011": {
        OSType.LINUX: "192.168.19.121",
        OSType.VOIS: "169.254.0.14",
        OSType.UBOOT: None,
    },
}


def get_eq_ip(eq_name: str, os_type: OSType) -> str | None:
    return GAS52_EQS_IPS[eq_name][os_type]
