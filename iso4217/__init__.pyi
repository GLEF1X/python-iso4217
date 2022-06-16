import pathlib
from typing import Any, Dict, Generator, Optional

DATAHUB_CURRENCY_RESOURCE_PATH: pathlib.Path

class CurrencyNotFoundError(Exception): ...

class Currency:
    alphabetical_code: str
    currency_name: str
    entity: str
    decimal_places: int
    numeric_code: int
    withdrawal_date: Optional[str] = None

    def __init__(
        self,
        alphabetical_code: str,
        currency_name: str,
        entity: str,
        decimal_places: int,
        numeric_code: int,
        withdrawal_date: Optional[str] = None,
    ) -> None: ...
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Currency": ...
    @property
    def was_withdrawn(self) -> bool: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

def find_currency(**filters: Any) -> Currency: ...
def iter_currency() -> Generator[Currency, None, None]: ...
