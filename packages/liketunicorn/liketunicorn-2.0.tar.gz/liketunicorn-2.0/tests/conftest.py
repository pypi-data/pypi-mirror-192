from __future__ import annotations

from typing import Any, Awaitable, Callable

import pytest

from liketunicorn.config import Config
from liketunicorn.enums import RunTypeEnum
from liketunicorn.server import Server
from tests.mocked_bot import MockedBot


@pytest.fixture
def app() -> Callable[..., Awaitable[Any]]:
    async def my_app(*args: Any, **kwargs: Any) -> None:
        return None

    yield my_app


@pytest.fixture
def bot() -> MockedBot:
    _bot = MockedBot()
    yield _bot


@pytest.fixture
def polling_config(
    app: Callable[..., Awaitable[Any]],
    bot: MockedBot,
) -> Config:
    _config = Config(
        app=app,
        bot=bot,
        run_type=RunTypeEnum.POLLING,
    )

    yield _config


@pytest.fixture
def polling_server(polling_config: Config) -> Server:
    _server = Server(config=polling_config)
    yield _server


@pytest.fixture
def polling_server_without_main_loop(polling_server: Server) -> Server:
    async def plug(*args: Any, **kwargs: Any) -> None:
        ...

    polling_server.main_loop = plug
    yield polling_server
