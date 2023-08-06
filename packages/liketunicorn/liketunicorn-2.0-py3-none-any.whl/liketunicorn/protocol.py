from typing import Any, Protocol

class BotProtocol(Protocol):  # pragma: no cover
    config: Any

    async def request(self, *args: Any, **kwargs: Any) -> ...:
        ...
