import functools
import pathlib
from typing import Any

import ijson

DATAHUB_CURRENCY_RESOURCE_PATH = pathlib.Path(__file__).resolve().parent / "data" / "currencies.json"


class CurrencyNotFoundError(Exception):
    pass


class DatahubCurrency:
    def __init__(
            self,
            alphabetical_code,
            currency_name,
            entity,
            decimal_places,
            numeric_code,
            withdrawal_date
    ):
        self.withdrawal_date = withdrawal_date
        self.numeric_code = numeric_code
        self.decimal_places = decimal_places
        self.entity = entity
        self.currency_name = currency_name
        self.alphabetical_code = alphabetical_code

    @classmethod
    def from_dict(cls, d):
        return cls(
            alphabetical_code=d["AlphabeticCode"],
            currency_name=d["Currency"],
            entity=d["Entity"],
            decimal_places=d["MinorUnit"],
            numeric_code=d["NumericCode"],
            withdrawal_date=d["WithdrawalDate"]
        )


@functools.lru_cache(maxsize=512)
def find_currency(**filters: Any):
    for currency in iter_currency():
        for filter_key, filter_value in filters.items():
            if getattr(currency, filter_key, None) == filter_value:
                return currency

    raise CurrencyNotFoundError(f"Currency by {filters} filters was not found")


def iter_currency():
    with open(DATAHUB_CURRENCY_RESOURCE_PATH, "r") as f:
        for currency_dict in ijson.items(f, 'item', use_float=True):
            yield DatahubCurrency.from_dict(currency_dict)
