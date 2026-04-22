"""
scrape_competitors.py
Scrapes competitor investor relations and about pages using Firecrawl,
saves raw markdown files to knowledge/raw/, and loads a summary record
into Snowflake RAW.COMPETITOR_SCRAPE.
"""

import os
import re
import time
import hashlib
import snowflake.connector
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from firecrawl import V1FirecrawlApp as FirecrawlApp

load_dotenv()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
KNOWLEDGE_RAW_DIR = Path(__file__).parent.parent / "knowledge" / "raw"
KNOWLEDGE_RAW_DIR.mkdir(parents=True, exist_ok=True)

# Delay between Firecrawl requests (seconds) — polite scraping
REQUEST_DELAY = 3

# Target pages: one focused URL per source, not full site crawls
TARGETS = [
    {
        "company": "axos_bank",
        "label": "Axos Bank - Investor Relations",
        "url": "https://investors.axosfinancial.com/overview",
    },
    {
        "company": "axos_bank",
        "label": "Axos Bank - About",
        "url": "https://www.axosbank.com/About-Us",
    },
    {
        "company": "ally_bank",
        "label": "Ally Bank - Investor Relations",
        "url": "https://media.ally.com/",
    },
    {
        "company": "ally_bank",
        "label": "Ally Bank - About",
        "url": "https://www.ally.com/about/",
    },
    {
        "company": "sofi",
        "label": "SoFi - Investor Relations",
        "url": "https://investors.sofi.com/overview",
    },
    {
        "company": "sofi",
        "label": "SoFi - About",
        "url": "https://www.sofi.com/our-story/",
    },
    {
        "company": "lendingclub_bank",
        "label": "LendingClub - Investor Relations",
        "url": "https://ir.lendingclub.com/overview",
    },
    {
        "company": "lendingclub_bank",
        "label": "LendingClub - About",
        "url": "https://www.lendingclub.com/about",
    },
    {
        "company": "marcus_goldman",
        "label": "Goldman Sachs - Marcus Overview",
        "url": "https://www.goldmansachs.com/what-we-do/consumer-and-wealth-management/marcus/",
    },
    {
        "company": "marcus_goldman",
        "label": "Goldman Sachs - Investor Relations",
        "url": "https://www.goldmansachs.com/investor-relations/",
    },
    # --- Axos additional sources ---
    {
        "company": "axos_bank",
        "label": "Axos Bank - Newsroom",
        "url": "https://www.axosbank.com/About-Us/Newsroom",
    },
    {
        "company": "axos_bank",
        "label": "Axos Bank - Business Banking",
        "url": "https://www.axosbank.com/Business",
    },
    # --- Industry / regulatory sources ---
    {
        "company": "fdic",
        "label": "FDIC - Quarterly Banking Profile Q4 2024",
        "url": "https://www.fdic.gov/analysis/quarterly-banking-profile/",
    },
    {
        "company": "fdic",
        "label": "FDIC - Digital Banking Overview",
        "url": "https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list/",
    },
    {
        "company": "federal_reserve",
        "label": "Federal Reserve - Consumer & Community Banking",
        "url": "https://www.federalreserve.gov/releases/g19/current/",
    },
    # --- Earnings / financial disclosures ---
    {
        "company": "sofi",
        "label": "SoFi - Financial Results & Press Releases",
        "url": "https://investors.sofi.com/press-releases",
    },
    {
        "company": "lendingclub_bank",
        "label": "LendingClub - Press Releases",
        "url": "https://ir.lendingclub.com/press-releases",
    },
    {
        "company": "ally_bank",
        "label": "Ally Bank - Corporate Overview",
        "url": "https://www.ally.com/about/our-company/",
    },
    # --- Industry research ---
    {
        "company": "industry",
        "label": "American Bankers Association - Digital Banking",
        "url": "https://www.aba.com/banking-topics/technology/digital-banking",
    },
]

# Snowflake target
TARGET_TABLE = "COMPETITOR_SCRAPE"


# ---------------------------------------------------------------------------
# Scrape
# ---------------------------------------------------------------------------
def slugify(text):
    return re.sub(r"[^a-z0-9_]", "_", text.lower()).strip("_")


def scrape_targets():
    app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
    results = []

    for target in TARGETS:
        label = target["label"]
        url = target["url"]
        company = target["company"]

        print(f"Scraping: {label} ({url})")
        try:
            response = app.scrape_url(
                url,
                formats=["markdown"],
                only_main_content=True,  # strips nav/footer noise
            )

            content = (response.markdown or "").strip()
            if not content:
                print(f"  WARNING: No content returned for {url}")
                results.append({**target, "content": "", "status": "empty"})
                time.sleep(REQUEST_DELAY)
                continue

            # Save to knowledge/raw/<company>_<slug>.md
            filename = f"{company}_{slugify(label)}.md"
            filepath = KNOWLEDGE_RAW_DIR / filename
            filepath.write_text(
                f"# {label}\n\nSource: {url}\nScraped: {datetime.utcnow().isoformat()}Z\n\n---\n\n{content}",
                encoding="utf-8",
            )
            print(f"  Saved: knowledge/raw/{filename} ({len(content):,} chars)")

            results.append({
                **target,
                "filename": filename,
                "content": content,
                "char_count": len(content),
                "status": "success",
            })

        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({**target, "content": "", "status": f"error: {e}"})

        time.sleep(REQUEST_DELAY)

    return results


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
            COMPANY       VARCHAR(100),
            LABEL         VARCHAR(255),
            URL           VARCHAR(2000),
            FILENAME      VARCHAR(255),
            CHAR_COUNT    NUMBER,
            STATUS        VARCHAR(50),
            CONTENT       TEXT,
            SCRAPED_AT    TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)


def load_to_snowflake(results):
    successful = [r for r in results if r.get("status") == "success"]
    if not successful:
        print("No successful scrapes to load.")
        return

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        create_table_if_not_exists(cursor)

        print(f"Truncating RAW.{TARGET_TABLE}...")
        cursor.execute(f"TRUNCATE TABLE RAW.{TARGET_TABLE}")

        rows = [
            (
                r["company"],
                r["label"],
                r["url"],
                r.get("filename", ""),
                r.get("char_count", 0),
                r["status"],
                r["content"],
            )
            for r in successful
        ]

        insert_sql = f"""
            INSERT INTO RAW.{TARGET_TABLE}
                (COMPANY, LABEL, URL, FILENAME, CHAR_COUNT, STATUS, CONTENT)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(insert_sql, rows)
        conn.commit()
        print(f"Done. {len(rows)} rows loaded into RAW.{TARGET_TABLE}.")

    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    results = scrape_targets()

    successful = sum(1 for r in results if r.get("status") == "success")
    failed = sum(1 for r in results if r.get("status") != "success")
    print(f"\nScrape complete: {successful} succeeded, {failed} failed.")

    load_to_snowflake(results)
