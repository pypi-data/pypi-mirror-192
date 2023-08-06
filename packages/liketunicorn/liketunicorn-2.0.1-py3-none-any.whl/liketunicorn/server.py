from __future__ import annotations

import asyncio
import sys

from liketunicorn.config import Config
from liketunicorn.enums import RunTypeEnum
from liketunicorn.logger import logger
from liketunicorn.polling import polling


class Server:
    def __init__(self, config: Config) -> None:
        self.config = config

    def run(self) -> None:  # pragma: no cover
        return asyncio.run(self.serve())

    async def serve(self) -> None:  # pragma: no cover
        if not self.config.loaded:
            self.config.load()

        await self.main_loop()

    async def main_loop(self) -> None:
        try:
            if self.config.run_type == RunTypeEnum.POLLING:
                await polling(
                    app=self.config.app,
                    bot=self.config.bot,
                )
            else:
                message = (
                    "Currently unsupported run type '{run_type}', also available: [{available}]."
                )
                raise ValueError(
                    message.format(run_type=self.config.run_type, available=list(RunTypeEnum))
                )
        except ValueError as e:
            logger.error("Error to start app: %s." % e)
            sys.exit(1)
