from __future__ import annotations

from argparse import ArgumentParser
from typing import Awaitable, Callable, Union

from liketunicorn.config import Config
from liketunicorn.enums import RunTypeEnum
from liketunicorn.protocol import BotProtocol
from liketunicorn.server import Server

parser = ArgumentParser(prog="tunicorn")
parser.add_argument("app")
parser.add_argument("bot")
parser.add_argument(
    "-rt",
    "--run-type",
    type=RunTypeEnum,
    default=RunTypeEnum.POLLING,
)


def main() -> None:
    args = parser.parse_args()
    run(
        args.app,
        args.bot,
        run_type=args.run_type,
    )


def run(
    app: Union[str, Callable[..., Awaitable[None]]],
    bot: Union[str, BotProtocol],
    *,
    run_type: RunTypeEnum,
) -> None:
    config = Config(
        app,
        bot,
        run_type=run_type,
    )
    server = Server(config=config)

    server.run()


if __name__ == "__main__":
    main()
