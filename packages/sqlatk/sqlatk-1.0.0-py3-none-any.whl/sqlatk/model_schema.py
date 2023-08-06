from typing import Callable
from typing import Container
from typing import List
from typing import TypeVar
from typing import Generic
from typing import KeysView
from typing import Type
from typing import Union
from typing import Optional
from dataclasses import dataclass
from databases import Database
from databases.interfaces import Record
from pydantic import BaseModel
from pydantic import BaseConfig
from pydantic import create_model
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import ColumnCollection
from sqlalchemy.orm.properties import ColumnProperty


class ORMConfig(BaseConfig):
    orm_mode = True


def model2schema(
    model: Type, *, config: Type = ORMConfig, exclude: Container[str] = []
) -> Type[BaseModel]:
    mapper_attrs = lambda mapper: mapper.attrs if hasattr(mapper, "attrs") else []
    attrs = mapper_attrs(inspect(model))
    is_column_field = (
        lambda attr: isinstance(attr, ColumnProperty)
        and attr.columns
        and not attr.key in exclude
    )
    pytype = (
        lambda c: getattr(getattr(c.type, "impl", None), "python_type", None)
        if hasattr(c.type, "impl")
        else getattr(c.type, "python_type", None)
    )
    deftype = lambda c: ... if (c.default is None and not c.nullable) else None

    mapper_attrs = lambda mapper: mapper.attrs if hasattr(mapper, "attrs") else []
    attrs = mapper_attrs(inspect(model))
    attrs = list(filter(is_column_field, attrs))
    attrs = [(attr.key, attr.columns[0]) for attr in attrs]
    fields = {name: (pytype(col), deftype(col)) for (name, col) in attrs}
    return create_model(model.__name__, __config__=config, **fields)  # type: ignore


M = TypeVar("M", bound=Table)
S = TypeVar("S", bound=BaseModel)

A = TypeVar("A")
B = TypeVar("B")


def process_optional(
    optional: Optional[A], process: Callable[[A], B]
) -> Union[B, None]:
    return None if optional is None else process(optional)


def process_many(records: List[Record], process: Callable[[Record], A]) -> List[A]:
    return [process(record) for record in records]


@dataclass(frozen=False, order=True)
class ModelSchema(Generic[M, S]):

    model: M
    schema: S

    @classmethod
    def from_model(cls, model: M):
        schema = model2schema(model)
        return cls(model=model, schema=schema)

    @property
    def table(self) -> Table:
        return self.model.__table__

    @property
    def tablename(self) -> str:
        return self.table.name

    @property
    def columns(self) -> ColumnCollection:
        return self.table.c

    @property
    def primary_key(self) -> PrimaryKeyConstraint:
        return self.table.primary_key

    @property
    def primary_column(self) -> Column:
        return self.primary_key.columns[0]

    @property
    def keys(self) -> KeysView:
        return self.schema.__fields__.keys()

    def __record_schema(self, record: Record):
        return self.schema.from_orm(record)

    def __record_dict(self, record: Record):
        return self.__record_schema(record).dict()

    def __record_model(self, record: Record):
        return self.model(**self.__record_dict(record))

    async def fetch_one_record(self, db: Database, primary_key) -> Union[Record, None]:
        query = self.table.select(where=self.primary_column == primary_key)
        return await db.fetch_one(query=query)

    async def fetch_one_schema(self, db: Database, primary_key):
        record = await self.fetch_one_record(db=db, primary_key=primary_key)
        return process_optional(record, self.__record_schema)

    async def fetch_one_dict(self, db: Database, primary_key):
        record = await self.fetch_one_record(db=db, primary_key=primary_key)
        return process_optional(record, self.__record_dict)

    async def fetch_one_model(self, db: Database, primary_key):
        record = await self.fetch_one_record(db=db, primary_key=primary_key)
        return process_optional(record, self.__record_model)

    async def iter_records(self, db: Database):
        query = self.table.select()
        models = await db.iterate(query=query)
        async for model in models:
            yield model

    async def iter_schemas(self, db: Database):
        iterator = await self.iter_records(db=db)
        for model in iterator:
            yield self.schema.from_orm(model)

    async def iter_many_models(self, db: Database, primary_keys: List[str]):
        query = self.table.select().where(self.primary_key().in_(tuple(primary_keys)))
        models = await db.iterate(query)
        for model in models:
            yield model

    async def iter_many_schemas(self, db: Database, primary_keys: List[str]):
        models = await self.iter_many_models(db, primary_keys)
        for model in models:
            yield self.schema.from_orm(model)

    async def fetch_all_records(self, db: Database) -> List[Record]:
        query = self.table.select()
        return await db.fetch_all(query=query)

    async def fetch_all_schemas(self, db: Database) -> List[S]:
        records = await self.fetch_all_records(db=db)
        return process_many(records, self.__record_schema)

    async def fetch_all_dicts(self, db: Database) -> List[S]:
        records = await self.fetch_all_records(db=db)
        return process_many(records, self.__record_dict)

    async def insert_one(self, db: Database, data: S):
        query = self.table.insert().values(**data.dict())
        await db.execute(query)

    async def insert_many(self, db: Database, data: List[S]):
        query = self.table.insert()
        values = [e.dict() for e in data]
        await db.execute_many(query, values=values)
