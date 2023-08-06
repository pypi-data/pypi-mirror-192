from __future__ import annotations

from collections import deque
from typing import Any, Deque, Optional
from dataclasses import dataclass


class Session:
    class ResponseGenerator:
        def __init__(self, session: Session) -> None:
            self._accessor = session

        def add_result_for(self, result: Optional[Any] = None) -> Any:
            response = result
            self._accessor.add_response(response)
            return response

    def __init__(self) -> None:
        self.requests: Deque[Any] = deque()
        self.responses: Deque[Any] = deque()
        self.response_generator = Session.ResponseGenerator(self)

    def get_request(self) -> Any:
        return self.requests.pop()

    def get_response(self) -> Any:
        return self.responses.pop()

    def add_request(self, request: Any) -> Any:
        self.requests.append(request)
        return request

    def add_response(self, response: Any) -> Any:
        self.responses.append(response)
        return response

    def add_result_for(self, result: Optional[Any] = None) -> Any:
        return self.response_generator.add_result_for(result=result)

@dataclass
class ConfigModel:
    offset: Optional[int] = None


class MockedBot:
    config = ConfigModel()

    def __init__(self) -> None:
        self.session = Session()

    async def request(self, data: Any) -> Any:
        self.session.add_request(data)
        return self.session.get_response()
