from typing import Any, Self
from msgspec import Struct

from pyorm.connection import get_db_connection
from pyorm.utils import get_model_fields, get_sql_type


class BaseModel(Struct, kw_only=True):

    id: str

    @classmethod
    def _table_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def create_table(cls) -> str:
        """
        TODO: Add uniqueness constraints
        """
        if cls._table_name is None:
            raise NotImplementedError("Should not create a table for BaseModel directly")
        fields = get_model_fields(cls)
        if not fields:
            raise ValueError("No fields defined for the model")
        fields_def = ", ".join(f"{name} {get_sql_type(type_)}" for name, type_ in fields.items())
        query = f"CREATE TABLE IF NOT EXISTS {cls._table_name()} ({fields_def});"
        conn = get_db_connection("database.db")
        conn.execute(query)
        conn.commit()

    @classmethod
    def create(cls, *_: Any, **kwargs: dict[str, Any]):
        if not kwargs:
            raise ValueError("No values provided for creation")
        query = f"INSERT INTO {cls._table_name()} ({', '.join(kwargs.keys())}) VALUES ({', '.join([f"'{val}'" for val in kwargs.values()])});"
        conn = get_db_connection("database.db")
        conn.execute(query)
        conn.commit()
    
    @classmethod
    def get(cls, *_: Any, **kwargs: dict[str, Any]) -> list[Self] | None:
        query = f"SELECT * FROM {cls._table_name()}"
        if kwargs:
            query += " WHERE"
            for key, value in kwargs.items():
                query += f" {key} = '{value}'"
        query += ";"
        conn = get_db_connection("database.db")
        if (results := conn.execute(query).fetchall()):
            return [cls(*row) for row in results]
        return None
    
    def update(self, *_: Any, **kwargs: dict[str, Any]):
        raise NotImplementedError # TODO: Implement me
    
    def delete(self):
        query = f"DELETE FROM {self._table_name()} WHERE id = '{self.id}';"
        conn = get_db_connection("database.db")
        conn.execute(query)
        conn.commit()
