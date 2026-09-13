def calculate_summary(df):
    """
    Calculate basic financial summary metrics.

    Returns:
        income
        expenses
        savings
        savings_rate
    """

    income = df.loc[
        df["amount"] > 0,
        "amount"
    ].sum()

    expenses = abs(
        df.loc[
            df["amount"] < 0,
            "amount"
        ].sum()
    )

    savings = income - expenses

    if income > 0:
        savings_rate = savings / income
    else:
        savings_rate = 0

    return {
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "savings_rate": savings_rate,
    }


def calculate_spending_by_category(df):
    """
    Calculate total spending per category.
    """

    return (
        df[df["amount"] < 0]
        .groupby("category")["amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )


def calculate_monthly_spending(df):
    """
    Calculate total spending per month.
    """

    return (
        df[df["amount"] < 0]
        .groupby("month")["amount"]
        .sum()
        .abs()
    )