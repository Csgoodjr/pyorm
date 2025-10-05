import builtins
import inspect
from typing import TypeVar

T = TypeVar("T")


def get_model_fields(model: T) -> dict[str, type]:
    return {k: v for k,v in inspect.get_annotations(model).items() if not k.startswith("_")}


def get_sql_type(value: type) -> str:
    match value:
        case builtins.str:
            return "TEXT NOT NULL"
        case _ if value == builtins.str | None:
            return "TEXT"
        case builtins.int:
            return "INTEGER NOT NULL"
        case _ if value == builtins.int | None:
            return "INTEGER"
        case builtins.float:
            return "REAL NOT NULL"
        case _ if value == builtins.float | None:
            return "REAL"
        case builtins.bool:
            return "BOOLEAN NOT NULL"
        case _ if value == builtins.bool | None:
            return "BOOLEAN"
        case builtins.bytes:
            return "BLOB NOT NULL"
        case _:
            raise ValueError(f"Unsupported type: {value}")
