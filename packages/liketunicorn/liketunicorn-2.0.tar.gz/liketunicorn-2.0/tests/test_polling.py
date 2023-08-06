from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from liketunicorn.polling import feed, listen
from liketunicorn.server import Server


@pytest.mark.asyncio
async def test_feed_exception() -> None:
    is_called = False

    async def app(update: Any) -> None:
        nonlocal is_called
        is_called = True

        assert update == 1
        raise Exception

        nonlocal _update  # noqa
        _update = 2

    _update = 1
    await feed(app, _update)
    assert is_called
    assert _update == 1


@pytest.mark.asyncio
async def test_feed() -> None:
    async def app(update: Any) -> None:
        assert update == 1

        nonlocal _update
        _update = 2

    _update = 1
    await feed(app, _update)

    assert _update == 2

@dataclass
class _UpdateModel:
    update_id: int


@pytest.mark.asyncio
async def test_listen(polling_server: Server) -> None:
    polling_server.config.bot.session.add_result_for(
        result=[
            _UpdateModel(update_id=1),
            _UpdateModel(update_id=2),
            _UpdateModel(update_id=3),
            _UpdateModel(update_id=0),
        ],
    )
    async for update in listen(bot=polling_server.config.bot):
        last_known_id = update.update_id
        assert last_known_id == update.update_id
