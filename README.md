# Finsight

Finsight is a Python and Streamlit personal finance analytics app that reads your bank statement CSV files, normalizes transactions into a common format, and produces basic spending and savings insights.

## Features

- Automatic bank/export format detection
- Currently dedicated CSV parsers for Revolut and Wise, with plans to expand
- Generic fallback parser for unsupported CSV formats
- Automatic comma/semicolon delimiter detection
- Transaction normalization into a common schema
- Rule-based transaction type categorization
- Financial summary metrics: income, expenses, savings, and savings rate
- Spending by category
- Monthly spending trends
- Streamlit dashboard with CSV upload and transaction table
- Clear warning when a bank format is not recognized

## Project Structure

```text
finsight/
├── app.py
├── analytics.py
├── categorizer.py
├── requirements.txt
├── .gitignore
├── parsers/
│   ├── __init__.py
│   ├── detector.py
│   ├── generic.py
│   ├── ing.py
│   ├── loader.py
│   ├── revolut.py
│   └── wise.py
└── sample_data/
    ├── generic_sample.csv
    ├── ing_sample.csv
    ├── revolut_sample.csv
    └── wise_sample.csv
```

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

Then open the local Streamlit page in your browser and upload a supported CSV statement.

## Supported Formats

Finsight currently includes dedicated parsers for Revolut and Wise CSV exports. Dedicated parser for ING is created through an online template, but not verified.

If the bank is not recognized, Finsight attempts to interpret the file using a generic CSV parser. Generic-parser results are explicitly marked as coming from an undetected bank and may be less reliable.

If the generic parser cannot identify enough information to interpret the file, the app reports that the statement could not be interpreted.

## Sample Data

The `sample_data` folder contains synthetic CSV files for testing. These files contain no real financial information.

## Privacy

Bank statements can contain highly sensitive personal and financial information.

Finsight is currently intended as a local development/portfolio project. DO NOT commit real bank statements, account numbers, transaction histories, or other sensitive financial data to GitHub.

The included `.gitignore` excludes common local bank-statement filenames and data folders, but you should still verify staged files before every commit.

## Limitations

- Transaction categorization is currently rule-based.
- Generic CSV parsing is best-effort and may interpret unusual formats incorrectly.
- Bank export formats may change over time and can require parser updates.
- Finsight does not provide financial, investment, tax, or legal advice.

## Possible Future Improvements

- Additional verified formats i.e. dedicated CSV parsers for popular Dutch banks including: ING, ABN AMRO, Rabo Bank, Bunq. This can only be done verifiably through obtaining actual bank statement templates from these banks, which I currently do not have access to. Perhaps in the future.
- Recurring subscription detection
- Month-over-month spending comparisons
- Additional personal finance metrics
- User-editable categories
- Anomaly detection
- Budget targets and goal tracking
- AI integration
    - AI detection of unidentifiable bank statement
    - AI analysis and feedback based on calculated metrics
    - AI coaching to achieve personal financial targets

## Tech Stack

- Python
- pandas
- Streamlit

## If you made it this far

Thanks for checking Finsight out! You can find me on LinkedIn at https://www.linkedin.com/in/ishaanfartyal/
