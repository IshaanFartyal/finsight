from copy import deepcopy

import streamlit as st
from pandas.errors import ParserError

from analytics import (
    calculate_monthly_spending,
    calculate_spending_by_category,
    calculate_summary,
)
from categorizer import (
    DEFAULT_CATEGORY_RULES,
    categorize_transaction,
)
from parsers.detector import detect_bank
from parsers.generic import parse_generic
from parsers.ing import parse_ing
from parsers.loader import load_bank_csv
from parsers.revolut import parse_revolut
from parsers.wise import parse_wise

# ----------------------------
# PAGE SETUP
# ----------------------------

st.set_page_config(
    page_title="Finsight",
    page_icon="💰",
    layout="wide",
)

st.title("Finsight")
st.write("Upload a bank statement CSV to analyze your finances.")

if "category_rules" not in st.session_state:
    st.session_state.category_rules = deepcopy(
        DEFAULT_CATEGORY_RULES
    )

# ----------------------------
# SIDEBAR CATEGORY EDITOR
# ----------------------------

st.sidebar.header("Transaction Categories")

for category, keywords in st.session_state.category_rules.items():
    with st.sidebar.expander(category):

        keyword_text = st.text_area(
            f"Keywords for {category}",
            value=", ".join(keywords),
            key=f"keywords_{category}",
        )

        updated_keywords = [
            keyword.strip()
            for keyword in keyword_text.split(",")
            if keyword.strip()
        ]

        st.session_state.category_rules[
            category
        ] = updated_keywords


st.sidebar.subheader("Add Category")

new_category = st.sidebar.text_input(
    "Category name"
)

new_keywords = st.sidebar.text_input(
    "Keywords",
    placeholder="GYM, BASIC FIT, SPORTCITY"
)

if st.sidebar.button("Add Category") and new_category:
    keyword_list = [
        keyword.strip()
        for keyword in new_keywords.split(",")
        if keyword.strip()
    ]

    st.session_state.category_rules[
        new_category
    ] = keyword_list

    st.rerun()


# ----------------------------
# RESET CATEGORIES
# ----------------------------

if st.sidebar.button("Reset Categories"):
    st.session_state.category_rules = deepcopy(
        DEFAULT_CATEGORY_RULES
    )

    st.rerun()

# ----------------------------
# FILE UPLOAD
# ----------------------------

uploaded_file = st.file_uploader(
    "Upload bank statement",
    type=["csv"],
)


if uploaded_file is not None:

    try:
        # ----------------------------
        # LOAD CSV
        # ----------------------------

        raw_df = load_bank_csv(uploaded_file)

        # ----------------------------
        # DETECT BANK
        # ----------------------------

        bank = detect_bank(raw_df)

        # ----------------------------
        # PARSE BANK
        # ----------------------------

        if bank == "revolut":
            df = parse_revolut(raw_df)

        elif bank == "wise":
            df = parse_wise(raw_df)

        elif bank == "ing":
            df = parse_ing(raw_df)

        elif bank == "unknown":

            st.warning(
                "Bank format was not recognized. "
                "FinSight is using a generic parser, "
                "so the results may be less reliable."
            )

            df = parse_generic(raw_df)

        # ----------------------------
        # CATEGORIZE TRANSACTIONS
        # ----------------------------

        df["category"] = (
            df["description"]
            .apply(
                lambda description:
                categorize_transaction(
                    description,
                    st.session_state.category_rules
                )
            )
        )

        # ----------------------------
        # TIME FIELDS
        # ----------------------------

        df["month"] = df["date"].dt.to_period("M")

        # ----------------------------
        # ANALYTICS
        # ----------------------------

        summary = calculate_summary(df)

        spending_by_category = (
            calculate_spending_by_category(df)
        )

        monthly_spending = (
            calculate_monthly_spending(df)
        )

        # ----------------------------
        # BANK STATUS
        # ----------------------------

        if bank == "unknown":
            st.write("Detected bank: Undetected bank")

        else:
            st.success(
                f"Detected bank: {bank.title()}"
            )

        # ----------------------------
        # SUMMARY METRICS
        # ----------------------------

        st.subheader("Financial Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Income",
            f"€{summary['income']:,.2f}"
        )

        col2.metric(
            "Expenses",
            f"€{summary['expenses']:,.2f}"
        )

        col3.metric(
            "Savings",
            f"€{summary['savings']:,.2f}"
        )

        col4.metric(
            "Savings Rate",
            f"{summary['savings_rate']:.1%}"
        )

        # ----------------------------
        # SPENDING BY CATEGORY
        # ----------------------------

        st.subheader("Spending by Category")

        if not spending_by_category.empty:

            category_chart = (
                spending_by_category
                .rename("Spending")
                .to_frame()
            )

            st.bar_chart(
                category_chart,
                y="Spending",
            )

        else:
            st.info(
                "No spending transactions found."
            )

        # ----------------------------
        # MONTHLY SPENDING
        # ----------------------------

        st.subheader("Monthly Spending")

        if not monthly_spending.empty:

            monthly_chart = (
                monthly_spending
                .rename("Spending")
                .to_frame()
            )

            monthly_chart.index = (
                monthly_chart.index.astype(str)
            )

            st.line_chart(
                monthly_chart,
                y="Spending",
            )

        else:
            st.info(
                "No monthly spending data available."
            )

        # ----------------------------
        # TRANSACTION TABLE
        # ----------------------------

        st.subheader("Transactions")

        st.dataframe(
            df,
            width="stretch"
        )

    except (ValueError, UnicodeDecodeError, ParserError) as error:

        st.error(
            "Statement could not be interpreted."
        )

        st.caption(
            f"Reason: {error}"
        )