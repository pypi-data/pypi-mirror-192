from __future__ import annotations

import asyncio
from time import perf_counter
from typing import Any, AsyncGenerator, Awaitable, Callable

from liketunicorn.logger import logger
from liketunicorn.protocol import BotProtocol


async def feed(app: Callable[..., Awaitable[None]], update: Any) -> None:
    try:
        await app(update)
    except BaseException as e:
        logger.warning("Failed to process update: %s." % str(e))


async def listen(bot: BotProtocol) -> AsyncGenerator[Any, None, None]:
    SLEEP_TIME = 0.5
    logger.info(
        "Listen updates:",
        f"on error sleep time {SLEEP_TIME}",
        "process updates timer registered",
        "rule to close: Update.update_id must be 0",
    )
    need_to_close = False

    get_updates = bot.config
    while not need_to_close:
        start = perf_counter()
        logger.debug("Start process updates")

        try:
            updates = await bot.request(get_updates)
            logger.debug(f"Got new updates `updates[{len(updates)}]`")
        except Exception as e:  # pragma: no cover
            logger.error("Skip updates: %s: %s." % (type(e).__name__, e))
            updates = []
            await asyncio.sleep(SLEEP_TIME)
        for update in updates:
            if not update.update_id:
                logger.info("Got none update, it's call to close listen, process last updates")
                need_to_close = True
            logger.debug(f"Process `update<{update.update_id}>`")
            yield update

            get_updates.offset = update.update_id + 1
        end = perf_counter()
        logger.debug(f"Successfully processed updates: time(ns) - {end - start}")

    logger.info("Listen closed")


async def _polling(
    app: Callable[..., Awaitable[None]], bot: BotProtocol
) -> None:  # pragma: no cover
    async for update in listen(bot=bot):
        await feed(app=app, update=update)


async def polling(
    app: Callable[..., Awaitable[None]], bot: BotProtocol
) -> None:  # pragma: no cover
    await _polling(app=app, bot=bot)
