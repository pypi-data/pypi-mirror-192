import json
from dataclasses import dataclass
from typing import List, NamedTuple, Optional, Sequence, Type, TypeVar

from dql.node import _fields

T = TypeVar("T", bound="DatasetRecord")


@dataclass
class DatasetRecord:
    id: int
    name: str
    description: Optional[str]
    version: Optional[int]
    labels: Sequence[str]
    shadow: bool

    @classmethod
    def parse(
        cls: Type[T],
        id: int,  # pylint: disable=redefined-builtin
        name: str,
        description: Optional[str],
        version: Optional[int],
        labels: str,
        shadow: int,
    ) -> T:
        labels_lst: List[str] = json.loads(labels)
        return cls(id, name, description, version, labels_lst, bool(shadow))


# TODO use DatasetRowSchema when dataset query refactoring is done (merged)
# https://github.com/iterative/dql/pull/258
DatasetRow = NamedTuple(  # type: ignore
    "DatasetRow",
    _fields + [("source", str)],
)
