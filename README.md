# `python-iso4217`: fast currency data package for Python

---

This python package automatically updates its own
currency data using github actions and immediately release
new version of package with updates. So it's super fast and at the same time always contains fresh data.

## Installation

### Pip

```bash
pip install python-iso4217
```

### Poetry

```bash
poetry add python-iso4217
```

## Usage

```python
from iso4217 import find_currency, iter_currency

# Filters that could be applied:
#   * currency_name
#   * alphabetical_code
#   * entity
#   * decimal_places
#   * numeric_code
#   * withdrawal_date
# The filters correspond to attributes of `Currency` class

# accept arbitrary filters as key/value pairs
currency = find_currency(currency_name="usd")

# if currency was not found, the lib will immediately raise CurrencyNotFoundError
defunct_currency = find_currency(currency_name="abc123")

# You need generator to lazy iter currencies? Ok

for c in iter_currency():
# do something
```

## Advanced


### Work with pydantic

```python
import inspect

from iso4217 import Currency as _Currency, find_currency
from pydantic import BaseModel, root_validator, StrictInt


class Currency(BaseModel, _Currency):
    __root__: StrictInt

    @root_validator(skip_on_failure=True)
    def humanize(cls, values):
        currency_numeric_code: int = values.get("__root__")
        # inspect.getfullargspec(_Currency.__init__) will contain `self`, so we cut it off
        orig_currency_cls_dunder_init_arg_names = inspect.getfullargspec(_Currency.__init__).args[1:]
        currency = find_currency(numeric_code=currency_numeric_code)
        return {
            k: getattr(currency, k, None)
            for k in orig_currency_cls_dunder_init_arg_names
        }
```