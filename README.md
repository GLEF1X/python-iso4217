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

# accept arbitrary filters as key/value pairs
currency = find_currency(currency_name="usd")

# if currency was not found, the lib will immediately raise CurrencyNotFoundError
defunct_currency = find_currency(currency_name="abc123")

# You need generator to lazy iter currencies? Ok

for c in iter_currency():
    # do something
```