import pandas as pd


def parse_wise(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse a Wise CSV export and convert it into
    FinSight's standard transaction format.
    """

    required_columns = {
        "ID",
        "Date",
        "Date Time",
        "Amount",
        "Currency",
        "Description",
        "Running Balance",
        "Total Fees",
        "Transaction Type",
        "Transaction Details Type",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Wise CSV is missing required columns: {missing_columns}"
        )

    df = df.copy()

    # Rename core fields
    df = df.rename(
        columns={
            "Date Time": "date",
            "Description": "description",
            "Amount": "amount",
            "Currency": "currency",
            "Transaction Type": "transaction_type",
            "Total Fees": "fee",
            "Running Balance": "balance",
        }
    )

    # ----------------------------
    # CLEAN BASIC DATA
    # ----------------------------

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

    # ----------------------------
    # IMPROVE DESCRIPTION
    # ----------------------------

    merchant = (
        df["Merchant"]
        .fillna("")
        .astype(str)
        .str.strip()
        if "Merchant" in df.columns
        else pd.Series("", index=df.index)
    )

    payee = (
        df["Payee Name"]
        .fillna("")
        .astype(str)
        .str.strip()
        if "Payee Name" in df.columns
        else pd.Series("", index=df.index)
    )

    payer = (
        df["Payer Name"]
        .fillna("")
        .astype(str)
        .str.strip()
        if "Payer Name" in df.columns
        else pd.Series("", index=df.index)
    )

    # Prefer merchant name for card transactions
    has_merchant = merchant != ""

    df.loc[
        has_merchant,
        "description"
    ] = merchant[has_merchant]

    # If no merchant, use payee name
    no_description = df["description"] == ""

    df.loc[
        no_description & (payee != ""),
        "description"
    ] = payee[
        no_description & (payee != "")
    ]

    # If still empty, use payer name
    no_description = df["description"] == ""

    df.loc[
        no_description & (payer != ""),
        "description"
    ] = payer[
        no_description & (payer != "")
    ]

    # Final fallback
    df.loc[
        df["description"] == "",
        "description"
    ] = "Unknown transaction"

    # ----------------------------
    # ADD STANDARD FIELDS
    # ----------------------------

    df["bank"] = "Wise"
    df["category"] = "Uncategorized"

    # Remove unusable rows
    df = df.dropna(
        subset=["date", "amount"]
    )

    df = df.sort_values("date")

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