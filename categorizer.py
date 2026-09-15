DEFAULT_CATEGORY_RULES = {
    "Groceries": [
        "ALBERT HEIJN",
        "JUMBO",
        "LIDL",
        "ALDI",
    ],
    "Subscriptions": [
        "SPOTIFY",
        "NETFLIX",
        "YOUTUBE PREMIUM",
    ],
    "Transport": [
        "UBER",
        "NS ",
        "OVPAY",
        "SHELL",
    ],
    "Restaurants": [
        "MCDONALD",
        "BURGER KING",
        "RESTAURANT",
        "CAFE",
    ],
    "Shopping": [
        "AMAZON",
        "BOL.COM",
        "ZALANDO",
    ],
    "Housing": [
        "RENT",
        "HOUSING",
        "DUWO",
    ],
    "Income": [
        "SALARY",
        "SALARIS",
        "PAYROLL",
    ],
}


def categorize_transaction(description, category_rules):
    description = description.upper()

    for category, keywords in category_rules.items():

        for keyword in keywords:

            if keyword.upper() in description:
                return category

    return "Other"