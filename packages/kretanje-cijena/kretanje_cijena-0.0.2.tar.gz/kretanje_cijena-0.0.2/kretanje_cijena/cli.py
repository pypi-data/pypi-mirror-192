"""CLI interface for kretanje_cijena project.
"""

from brds import Fetcher as _Fetcher
from brds import FileWriter as _FileWriter
from brds import fload as _fload

from .gunzip_importer import GunzipImporter as _GunzipImporter


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m kretanje_cijena` and `$ kretanje_cijena `.

    """
    fetcher = _Fetcher(
        _GunzipImporter("https://kretanje-cijena.hr:50001"),
        _FileWriter.from_environment(),
        ["/data/public"],
        "kretanje-cijena",
    )
    fetcher.fetch()

    data = _fload("kretanje-cijena/data/public")
    for data_type, values in data.items():
        print(data_type, len(values))
        if len(values) > 0:
            print(values[0].keys())
