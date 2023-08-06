from __future__ import annotations

import sys
from typing import Any, Awaitable, Callable, Union

from liketunicorn.enums import RunTypeEnum
from liketunicorn.exceptions import ImporterError
from liketunicorn.importer import import_from_string
from liketunicorn.logger import logger
from liketunicorn.protocol import BotProtocol


def _load(load_string: Any) -> Any:
    try:
        loaded = import_from_string(load_string)
    except ImporterError as exception:
        logger.error("Error loading app: %s." % exception)
        sys.exit(1)
    return loaded


class Config:
    def __init__(
        self,
        app: Union[str, Callable[..., Awaitable[None]]],
        bot: Union[str, BotProtocol],
        *,
        run_type: RunTypeEnum,
    ) -> None:
        self.app = app
        self.bot = bot
        self.run_type = run_type
        self.loaded = False

    def load(self) -> None:
        assert not self.loaded

        self.app = _load(self.app)
        self.bot = _load(self.bot)

        self.loaded = True
