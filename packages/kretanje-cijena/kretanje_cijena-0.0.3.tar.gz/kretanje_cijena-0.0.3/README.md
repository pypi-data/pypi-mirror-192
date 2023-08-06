
# kretanje_cijena

[![codecov](https://codecov.io/gh/brahle/kretanje-cijena/branch/main/graph/badge.svg?token=kretanje-cijena_token_here)](https://codecov.io/gh/brahle/kretanje-cijena)
[![CI](https://github.com/brahle/kretanje-cijena/actions/workflows/main.yml/badge.svg)](https://github.com/brahle/kretanje-cijena/actions/workflows/main.yml)

API za preuzimanje podataka s web stranice kretanje-cijena.


## Install it from PyPI

```bash
pip install kretanje_cijena
```

## Usage

```py
from brds import GunzipImporter

data = GunzipImporter("https://kretanje-cijena.hr:50001").get("/data/public")
```

```bash
$ python -m kretanje_cijena
#or
$ kretanje_cijena
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
