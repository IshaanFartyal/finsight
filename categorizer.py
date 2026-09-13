def categorize_transaction(description):
    description = description.upper()

    if any(
        word in description
        for word in [
            "ALBERT HEIJN",
            "JUMBO",
            "LIDL",
            "ALDI",
        ]
    ):
        return "Groceries"

    elif any(
        word in description
        for word in [
            "SPOTIFY",
            "NETFLIX",
            "YOUTUBE PREMIUM",
        ]
    ):
        return "Subscriptions"

    elif any(
        word in description
        for word in [
            "UBER",
            "NS ",
            "OVPAY",
            "SHELL",
        ]
    ):
        return "Transport"

    elif any(
        word in description
        for word in [
            "MCDONALD",
            "BURGER KING",
            "RESTAURANT",
            "CAFE",
        ]
    ):
        return "Restaurants"

    elif any(
        word in description
        for word in [
            "AMAZON",
            "BOL.COM",
            "ZALANDO",
        ]
    ):
        return "Shopping"

    elif any(
        word in description
        for word in [
            "RENT",
            "HOUSING",
            "DUWO",
        ]
    ):
        return "Housing"

    elif any(
        word in description
        for word in [
            "SALARY",
            "SALARIS",
            "PAYROLL",
        ]
    ):
        return "Income"

    else:
        return "Other"