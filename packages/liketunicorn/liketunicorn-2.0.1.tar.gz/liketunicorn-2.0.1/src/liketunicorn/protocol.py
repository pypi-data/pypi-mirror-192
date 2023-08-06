from __future__ import annotations

from typing import Any, Protocol


class BotProtocol(Protocol):  # pragma: no cover
    config: Any

    def get_current(self) -> Any:
        ...

    def set_current(self, *args: Any) -> Any:
        ...

    def reset_current(self, *args: Any) -> None:
        ...

    async def request(self, *args: Any, **kwargs: Any) -> ...:
        ...
