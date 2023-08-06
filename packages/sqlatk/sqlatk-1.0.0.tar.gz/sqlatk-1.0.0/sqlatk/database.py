from abc import abstractmethod
from typing import Optional
from typing import List
from typing import Dict
from typing import Any
from dataclasses import dataclass
from dataclasses import field
from databases import Database
from pydantic import BaseModel
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from fastapi import APIRouter
from fastapi import Depends

from .model_schema import ModelSchema
from .model_schema import M
from .model_schema import S



class TableSeedData(BaseModel):
    tablename: str
    data: List[Dict[str, Any]]


class DatabaseSeedData(BaseModel):
    tables: List[TableSeedData]



@dataclass(frozen=False,order=True)
class DatabaseURL:
    url_base:str
    url_sync:Optional[str] = field(default=None)
    url_async:Optional[str] = field(default=None)

    def __init__(self,url_base:str):
        self.url_base = url_base
        self.url_sync = url_base.replace("postgres://", "postgresql://")
        self.url_async = url_base.replace("postgres://", "postgresql+asyncpg://")

@dataclass(frozen=False,order=True)
class DatabaseConfig:

    url:DatabaseURL = field(default=None)
    is_async: bool = field(default=True)
    min_size: int = field(default=0)
    max_size: int = field(default=0)
    

class DatabaseBase(BaseModel):
    config: DatabaseConfig

    @property
    def url(self) -> DatabaseURL:
        return self.config.url

    @abstractmethod
    def database(self) -> Database:
        pass

    @abstractmethod
    def attach_to_fastapi_app(self, app):
        pass

    @abstractmethod
    def database_from_starlette_request(self, request) -> Database:
        pass


class AsyncDatabase(DatabaseBase):


    def database(self) -> Database:
        config = self.config
        url = config.url.url_async
        min_size = config.min_size
        max_size = config.max_size
        return Database(url, min_size=min_size, max_size=max_size)

    def database_from_starlette_request(self, request) -> Database:
        return request.app.state._db

    async def connect_fastapi_app(self, app):
        db = self.database()
        try:
            await db.connect()
            app.state._db = db
        except Exception as error:
            print(error)

    async def disconnect_fastapi_app(self, app):
        try:
            await app.state._db.disconnect()
        except Exception as error:
            print(error)

    def attach_to_fastapi_app(self, app):
        async def startup() -> None:
            await self.connect_fastapi_app(app=app)

        async def shutdown() -> None:
            await self.disconnect_fastapi_app(app=app)

        app.add_event_handler("startup", startup)
        app.add_event_handler("shutdown", shutdown)

    async def create(self, metadata,engine: Optional[object]=None, checkfirst: bool = True):
        if engine is None:
            sync_db_url = self.url.url_sync
            engine = create_engine(sync_db_url)
        await metadata.create_all(engine, checkfirst=checkfirst)

    async def seed_db(
        self,
        model_schemas_map:Dict[str,ModelSchema],
        metadata: Optional[MetaData],
        database_seed_data: Optional[Dict] = None,
        seed_data_path: Optional[str] = None,
        seed_order:Optional[List[str]] = None
    ):

        self.create(metadata=metadata)
        seed_data = database_seed_data.copy()
        if not seed_data and seed_data_path is not None:
            seed_data = DatabaseSeedData.parse_file(seed_data_path)
            seed_data = {seed.tablename: seed.data for seed in seed_data.tables}
        if seed_data:
            database = self.database()
            began_disconnected = not database.is_connected
            if began_disconnected:
                await database.connect()
            seed_order = list(seed_data.keys()) if seed_order is None else seed_order
            for tablename in seed_order:
                if tablename in seed_data:
                    ms = model_schemas_map.get(tablename,None)
                    data = [ms.schema(**record) for record in seed_data[tablename]]
                    await ms.insert_many(database, data)

            if began_disconnected:
                await database.disconnect()

    def init_subrouter(self,ms: ModelSchema[M, S]):

        tablename = ms.tablename
        prefix = f"/{tablename}"
        router = APIRouter(prefix=prefix)

        @router.get("/{primary_key}", response_model=S)
        async def get_one(
            primary_key, db: Database = Depends(self.database_from_starlette_request)
        ):
            return await ms.fetch_one_schema(db, primary_key)

        @router.get("/", response_model=List[dict])
        async def get_all(db: Database = Depends(self.database_from_starlette_request)):
            return await ms.fetch_all_dicts(db)

        return router


    def attach_crud_routers_to_app(self,app,model_schemas:List[str,ModelSchema]):
        for ms in model_schemas:
            subrouter = self.init_subrouter(ms=ms)
            app.include_router(subrouter)


