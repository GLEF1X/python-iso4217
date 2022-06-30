import functools
import pathlib
from typing import Any

import ijson

DATAHUB_CURRENCY_RESOURCE_PATH = (
    pathlib.Path(__file__).resolve().parent / "data" / "currencies.json"
)


class CurrencyNotFoundError(Exception):
    pass


class Currency:
    def __init__(
        self,
        alphabetical_code,
        currency_name,
        entity,
        decimal_places,
        numeric_code,
        withdrawal_date,
    ):
        self.withdrawal_date = withdrawal_date
        self.numeric_code = numeric_code
        self.decimal_places = decimal_places
        self.entity = entity
        self.currency_name = currency_name
        self.alphabetical_code = alphabetical_code

    @classmethod
    def from_dict(cls, d):
        numeric_code = d["NumericCode"]
        if numeric_code is not None:
            numeric_code = int(numeric_code)

        decimal_places = d["MinorUnit"]
        if isinstance(decimal_places, str) and decimal_places.isdigit():
            decimal_places = int(decimal_places)

        return cls(
            alphabetical_code=d["AlphabeticCode"],
            currency_name=d["Currency"],
            entity=d["Entity"],
            decimal_places=decimal_places,
            numeric_code=numeric_code,
            withdrawal_date=d["WithdrawalDate"],
        )

    def __str__(self):
        if self.was_withdrawn:
            return "{0} (not active) - withdrawn at {1}".format(
                self.currency_name, self.withdrawal_date
            )

        return "{0} {1}".format(self.currency_name, self.numeric_code)

    def __repr__(self):
        return "<Currency {0}>".format(self.currency_name)

    @property
    def was_withdrawn(self):
        return self.withdrawal_date is not None


@functools.lru_cache(maxsize=512)
def find_currency(**filters: Any):
    for currency in iter_currency():
        for filter_key, filter_value in filters.items():
            f = getattr(currency, filter_key, None)
            if f is None:
                continue
            if f == filter_value:
                return currency
            elif isinstance(f, str) and f.lower() == filter_value:
                return currency

    raise CurrencyNotFoundError(f"Currency by {filters} filters was not found")


def iter_currency():
    with open(DATAHUB_CURRENCY_RESOURCE_PATH, "r") as f:
        for currency_dict in ijson.items(f, "item", use_float=True):
            yield Currency.from_dict(currency_dict)
