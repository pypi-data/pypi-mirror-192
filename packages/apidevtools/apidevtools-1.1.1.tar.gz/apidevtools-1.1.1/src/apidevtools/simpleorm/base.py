from abc import abstractmethod as _abstractmethod, ABC as _ABC
from loguru._logger import Logger
from typing import Any

from .schema import Schema
from .records import Records
from .types import SchemaType, Record


class BaseORM(_ABC):
    def __init__(self, database: str, host: str, port: str | int, user: str, password: str | None, logger: Logger):
        self.database: str = database
        self.host: str = host
        self.port: str | int = port
        self.user: str = user
        self.password: str | None = password

        self.logger: Logger = logger

    @_abstractmethod
    async def create_pool(self) -> bool:
        ...

    @_abstractmethod
    async def close_pool(self) -> bool:
        ...

    @_abstractmethod
    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        ...

    @_abstractmethod
    async def select(self, query: str, args: tuple[Any, ...] = (), schema_t: SchemaType = dict) -> Records:
        ...

    @_abstractmethod
    async def insert(self, schema: Schema, schema_t: SchemaType = dict) -> Record:
        ...

    @_abstractmethod
    async def update(self, schema: Schema, where: str, schema_t: SchemaType = dict) -> Record:
        ...

    @_abstractmethod
    async def delete(self, instance: dict | Schema, schema_t: SchemaType = dict, tablename: str = None) -> Record:
        ...
