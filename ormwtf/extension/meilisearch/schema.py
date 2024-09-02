from abc import ABC, abstractmethod
from enum import StrEnum
from typing import (
    Any,
    Generic,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from meilisearch_python_sdk.models.search import SearchResults
from pydantic import BaseModel, Field

from ormwtf.base.pydantic import BaseReference

# ----------------------- #


class SortOrder(StrEnum):
    """
    Sort Order Enum

    Attributes:
        asc (str): Ascending Order
        desc (str): Descending Order
    """

    asc = "asc"
    desc = "desc"


# ....................... #


class SortField(BaseModel):
    """
    Sort field model

    Attributes:
        key (str): Key of the field
        title (str): The field title
        default (bool): Whether the Field is the default sort field
    """

    key: str
    title: str
    default: bool = False


# ----------------------- #

F = TypeVar("F", bound="FilterABC")


class FilterABC(ABC, BaseModel):
    """
    Abstract Base Class for Search Filters

    Attributes:
        key (str): Key of the filter
        title (str): The filter title
        value (Any, optional): The filter value
        type (str): The filter type
    """

    key: str
    title: str
    value: Optional[Any] = None
    type: str = "abc"

    # ....................... #

    @abstractmethod
    def build(self) -> Optional[str]: ...


# ....................... #


class BooleanFilter(FilterABC):
    """
    Boolean Filter Model

    Attributes:
        key (str): Key of the filter
        title (str): The filter title
        value (bool): The filter value
    """

    value: Optional[bool] = None
    type: Literal["boolean"] = "boolean"

    # ....................... #

    def build(self):
        if self.value is not None:
            return f"{self.key} = {str(self.value).lower()}"

        return None


# ....................... #


class NumberFilter(FilterABC):
    """
    Number Filter Model

    Attributes:
        key (str): Key of the filter
        title (str): The filter title
        value (Tuple[float, float]): The filter value
    """

    value: Tuple[Optional[float], Optional[float]] = (None, None)
    type: Literal["number"] = "number"

    # ....................... #

    def build(self):
        low, high = self.value

        if low is None and high is not None:
            return f"{self.key} <= {high}"

        if low is not None and high is None:
            return f"{self.key} >= {low}"

        if low is not None and high is not None:
            return f"{self.key} {low} TO {high}"

        return None


# ....................... #


class DatetimeFilter(FilterABC):
    """
    Datetime Filter Model

    Attributes:
        key (str): Key of the filter
        title (str): The filter title
        value (Tuple[int, int]): The filter value
    """

    value: Tuple[Optional[int], Optional[int]] = (None, None)
    type: Literal["datetime"] = "datetime"

    # ....................... #

    def build(self):
        low, high = self.value

        if low is None and high is not None:
            return f"{self.key} <= {high}"

        if low is not None and high is None:
            return f"{self.key} >= {low}"

        if low is not None and high is not None:
            return f"{self.key} {low} TO {high}"

        return None


# ....................... #


class ArrayFilter(FilterABC):
    """
    Array Filter Model

    Attributes:
        key (str): Key of the filter
        title (str): The filter title
        value (List[Any]): The filter value
    """

    value: List[Any] = []
    type: Literal["array"] = "array"

    # ....................... #

    def build(self):
        if self.value:
            return f"{self.key} IN {self.value}"

        return None


# ....................... #

SomeFilter = Union[BooleanFilter, NumberFilter, DatetimeFilter, ArrayFilter]

# ----------------------- #


class SearchRequest(BaseModel):
    query: str = Field(
        default="",
        title="Query",
    )
    sort: Optional[str] = Field(
        default=None,
        title="Sort Field",
    )
    order: SortOrder = Field(
        default=SortOrder.desc,
        title="Sort Order",
    )
    filters: List[SomeFilter] = Field(
        default_factory=list,
        title="Filters",
        discriminator="type",
    )


# ----------------------- #

S = TypeVar("S", bound="SearchResponse")
T = TypeVar("T")


class SearchResponse(BaseModel, Generic[T]):
    hits: List[T] = Field(
        default_factory=list,
        title="Hits",
    )
    size: int = Field(
        ...,
        title="Hits per Page",
    )
    page: int = Field(
        ...,
        title="Current Page",
    )
    count: int = Field(
        ...,
        title="Total number of Hits",
    )

    # ....................... #

    @classmethod
    def from_search_results(cls: Type[S], res: SearchResults) -> S:
        return cls(
            hits=res.hits,
            size=res.hits_per_page,  # type: ignore
            page=res.page,  # type: ignore
            count=res.total_hits,  # type: ignore
        )


# ....................... #


class MeilisearchReference(BaseReference):
    sort: List[SortField] = Field(
        default_factory=list,
        title="Sort Fields",
    )
    filters: List[SomeFilter] = Field(
        default_factory=list,
        title="Filters",
        discriminator="type",
    )
