"""
extract_fdic.py
Pulls quarterly financial data from the FDIC BankFind Suite API
and loads it into Snowflake RAW.FDIC_FINANCIALS.
"""

import os
import requests
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
FDIC_BASE_URL = "https://banks.data.fdic.gov/api/financials"
PAGE_SIZE = 10000  # max allowed by FDIC API

# Fields to pull — must match FDIC API uppercase field names exactly
FIELDS = [
    "REPDTE",   # report date (YYYYMMDD)
    "CERT",     # institution certificate number (unique bank ID)
    "NAME",     # institution name
    "ASSET",    # total assets ($thousands)
    "DEP",      # total deposits ($thousands)
    "LNLSNET",  # net loans and leases ($thousands)
    "NETINC",   # net income ($thousands)
    "NIMY",     # net interest margin (%)
    "ROA",      # return on assets (%)
    "ROE",      # return on equity (%)
    "INTINC",   # total interest income ($thousands)
    "NONII",    # total non-interest income ($thousands)
    "NONIX",    # total non-interest expense ($thousands)
    "EQTOT",    # total equity capital ($thousands)
    "SC",       # total securities ($thousands)
    "LNLSDEPR", # loans to deposits ratio (%)
    "EQ",       # total equity ($thousands)
]

# Pull data starting from this date (YYYYMMDD)
START_DATE = "20200101"
END_DATE   = "20260101"

# Snowflake target
TARGET_TABLE = "FDIC_FINANCIALS"


# ---------------------------------------------------------------------------
# Extract
# ---------------------------------------------------------------------------
def fetch_fdic_financials():
    records = []
    offset = 0

    print("Fetching FDIC financial data...")
    while True:
        params = {
            "fields": ",".join(FIELDS),
            "filters": f"REPDTE:[{START_DATE} TO {END_DATE}]",
            "limit": PAGE_SIZE,
            "offset": offset,
            "sort_by": "REPDTE",
            "sort_order": "ASC",
            "output": "json",
        }

        response = requests.get(FDIC_BASE_URL, params=params, timeout=60, allow_redirects=True)
        response.raise_for_status()
        data = response.json()

        batch = data.get("data", [])
        if not batch:
            break

        records.extend([row["data"] for row in batch])
        print(f"  Fetched {len(records):,} records so far...")

        if len(batch) < PAGE_SIZE:
            break
        offset += PAGE_SIZE

    print(f"Total records fetched: {len(records):,}")
    return records


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        role=os.environ["SNOWFLAKE_ROLE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )


def create_table_if_not_exists(cursor):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS RAW.{TARGET_TABLE} (
            REPDTE        VARCHAR(8),
            CERT          NUMBER,
            NAME          VARCHAR(255),
            ASSET         NUMBER,
            DEP           NUMBER,
            LNLSNET       NUMBER,
            NETINC        NUMBER,
            NIMY          FLOAT,
            ROA           FLOAT,
            ROE           FLOAT,
            INTINC        NUMBER,
            NONII         NUMBER,
            NONIX         NUMBER,
            EQTOT         NUMBER,
            SC            NUMBER,
            LNLSDEPR      FLOAT,
            EQ            NUMBER,
            _LOADED_AT    TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)


def load_to_snowflake(records):
    if not records:
        print("No records to load.")
        return

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        create_table_if_not_exists(cursor)

        # Truncate and reload (full refresh)
        print(f"Truncating RAW.{TARGET_TABLE}...")
        cursor.execute(f"TRUNCATE TABLE RAW.{TARGET_TABLE}")

        rows = [
            (
                r.get("REPDTE"),
                r.get("CERT"),
                r.get("NAME"),
                r.get("ASSET"),
                r.get("DEP"),
                r.get("LNLSNET"),
                r.get("NETINC"),
                r.get("NIMY"),
                r.get("ROA"),
                r.get("ROE"),
                r.get("INTINC"),
                r.get("NONII"),
                r.get("NONIX"),
                r.get("EQTOT"),
                r.get("SC"),
                r.get("LNLSDEPR"),
                r.get("EQ"),
            )
            for r in records
        ]

        insert_sql = f"""
            INSERT INTO RAW.{TARGET_TABLE} (
                REPDTE, CERT, NAME, ASSET, DEP, LNLSNET, NETINC,
                NIMY, ROA, ROE, INTINC, NONII, NONIX, EQTOT, SC, LNLSDEPR, EQ
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        batch_size = 5000
        for i in range(0, len(rows), batch_size):
            cursor.executemany(insert_sql, rows[i : i + batch_size])
            print(f"  Inserted {min(i + batch_size, len(rows)):,} / {len(rows):,} rows...")

        conn.commit()
        print(f"Done. {len(rows):,} rows loaded into RAW.{TARGET_TABLE}.")

    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    records = fetch_fdic_financials()
    load_to_snowflake(records)
