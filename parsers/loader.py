import csv

import pandas as pd


def load_bank_csv(file):
    """
    Load a bank CSV and automatically detect
    comma or semicolon separators.
    """

    file.seek(0)

    sample = file.read(4096)

    if isinstance(sample, bytes):
        sample = sample.decode(
            "utf-8-sig"
        )

    try:
        dialect = csv.Sniffer().sniff(
            sample,
            delimiters=",;"
        )

        separator = dialect.delimiter

    except csv.Error:
        raise ValueError(
            "Could not determine CSV separator."
        )

    file.seek(0)

    return pd.read_csv(
        file,
        sep=separator,
        dtype=str,
        encoding="utf-8-sig",
    )