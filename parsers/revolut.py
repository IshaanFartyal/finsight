import pandas as pd


def parse_revolut(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse a Revolut CSV export and convert it into
    FinSight's standard transaction format.

    Expected Revolut columns:
    Type
    Product
    Started Date
    Completed Date
    Description
    Amount
    Fee
    Currency
    State
    Balance
    """

    required_columns = {
        "Type",
        "Product",
        "Started Date",
        "Completed Date",
        "Description",
        "Amount",
        "Fee",
        "Currency",
        "State",
        "Balance",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Revolut CSV is missing required columns: {missing_columns}"
        )

    df = df.copy()

    # Keep completed transactions only
    df = df[
        df["State"].astype(str).str.upper() == "COMPLETED"
    ].copy()

    # Rename Revolut columns to FinSight naming
    df = df.rename(
        columns={
            "Completed Date": "date",
            "Description": "description",
            "Amount": "amount",
            "Currency": "currency",
            "Type": "transaction_type",
            "Fee": "fee",
            "Balance": "balance",
        }
    )

    # Convert data types
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["description"] = (
        df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["fee"] = pd.to_numeric(
        df["fee"],
        errors="coerce"
    ).fillna(0)

    df["balance"] = pd.to_numeric(
        df["balance"],
        errors="coerce"
    )

    df["currency"] = (
        df["currency"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["transaction_type"] = (
        df["transaction_type"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Add standardized fields
    df["bank"] = "Revolut"
    df["category"] = "Uncategorized"

    # Remove invalid transactions
    df = df.dropna(
        subset=["date", "amount"]
    )

    # Sort by date
    df = df.sort_values("date")

    # FinSight standard schema
    standard_columns = [
        "date",
        "description",
        "amount",
        "currency",
        "bank",
        "transaction_type",
        "fee",
        "balance",
        "category",
    ]

    return df[standard_columns].reset_index(drop=True)