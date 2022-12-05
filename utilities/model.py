from typing import List, Optional, Any, Dict, Tuple
from sqlalchemy import (
    Table,
)
from pydantic import NonNegativeInt
from pydantic.main import ModelMetaclass

from .db import database

class Model:

    def __issue_returning(
        self,
        table: Table,
        query: Any,
        returning: Optional[List[str]] = None,
    ) -> Any:
        returnings = [table.c[k] for k in returning]
        query = query.returning(*returnings)
        return query

    async def create(
        self,
        table: Table,
        payload: ModelMetaclass,
        returning: Optional[List[str]] = None,
        is_exclude_none=False,
    ) -> Optional[Dict[str, Any]]:
        query = table.insert().values(payload.dict(exclude_none=is_exclude_none))
        
        if returning:
            query = self.__issue_returning(
                table,
                query,
                returning,
            )
            returnings = dict()
            # replaced from execute since we cannot retrieve multiple columns in execute when using returning
            data = await database.fetch_one(query=query)
            for key in data:
                returnings[key] = data[key]
        else:
            data = await database.execute(query=query)
            returnings = None

        return returnings

    async def get(
        self,
        table: Table,
        filters: Dict[str, Any],
        limit: Optional[NonNegativeInt] = 30,
        offset: Optional[NonNegativeInt] = 0,
        isAll: Optional[bool] = False,
    ):
        # TODO: change to dictionary implementation if already available in new sqlalchemy version
        where_obj = [table.c[key] == value for (key, value) in filters.items()]
        column_names = []
        for name in table.columns.keys():
            column_names.append(table.c[name])
            
        query = table.select().where(
            *where_obj
        )

        if not isAll:
            query = query.offset(offset or 0).limit(limit or 30)
            
        return await database.fetch_all(query=query)

    async def update(
        self,
        table: Table,
        primary_keys: Dict[str, Any],
        payload: ModelMetaclass,
        is_exclude_none=False,
    ):
        # if primary_keys is empty raise an Error
        if len(primary_keys) == 0:
            raise ValueError('primary key is required')
        # TODO: change to dictionary implementation if already available in new sqlalchemy version
        where_obj = [table.c[key] == value for (key, value) in primary_keys.items()]
        query = (
            table.update().values(
                **payload.dict(exclude_none=is_exclude_none)
            ).where(
                *where_obj
            )
        )

        return await database.execute(query=query)


    async def delete(
        self,
        table: Table,
        primary_keys: Dict[str, Any],
    ):
        # if primary_keys is empty raise an Error
        if len(primary_keys) == 0:
            raise ValueError('primary key is required')
        # TODO: change to dictionary implementation if already available in new sqlalchemy version
        where_obj = [table.c[key] == value for (key, value) in primary_keys.items()]
        query = table.delete().where(
            *where_obj
        )

        return await database.execute(query=query)

    def get_primary_keys(
        self,
        table: Table,
    ) -> List[str]:
        return [pk.name for pk in table.primary_key.columns.values()]
