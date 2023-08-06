from __future__ import annotations

from functools import partial

from me_setups.boards.gas52 import Gas52Board
from me_setups.boards.types import BoardType
from me_setups.components import const as C


Gas52 = Gas52Board


Gas52EvoB1 = partial(
    Gas52Board,
    eqs=C.GAS52_EQS,
    mcu=C.GAS52_MCU,
    board_type=BoardType.EVO,
    board_rev="0x1",
)


Gas52EvoC1 = partial(
    Gas52Board,
    eqs=C.GAS52_EQS,
    mcu=C.GAS52_MCU,
    board_type=BoardType.EVO,
    board_rev="0x2",
)


Gas52Evo = Gas52EvoC1
