# CLAUDE.md — Project Context

## Project Overview

**U.S. Bank Performance & Competitive Intelligence Pipeline**

An end-to-end data pipeline and analytics project targeting the Jr. Data Analyst role
at Axos Bank (NYSE: AX). Pulls U.S. bank financial data from the FDIC public API,
transforms it through dbt into a star schema in Snowflake, and surfaces bank
profitability trends and Axos peer benchmarking in a Streamlit dashboard. Also
includes a competitive intelligence knowledge base scraped from Axos and competitor
investor relations pages.

**Job posting:** `docs/job-posting.pdf` — Jr. Data Analyst, Axos Bank, San Diego, CA

---

## Tech Stack

| Layer | Tool |
|---|---|
| IDE | Cursor |
| AI Development | Claude Code + Superpowers |
| Version Control | Git + GitHub (public repo) |
| Data Warehouse | Snowflake (trial, AWS US East 1) |
| Transformation | dbt |
| Orchestration | GitHub Actions (scheduled) |
| Dashboard | Streamlit (Streamlit Community Cloud) |
| Knowledge Base | Claude Code (scrape → summarize → query) |

---

## Data Sources

### Source 1 — API: FDIC BankFind Suite
- **Base URL:** `https://banks.data.fdic.gov/api/`
- **Key endpoint:** `/financials` — quarterly call report data per institution
- **Auth:** None required (public API)
- **Script:** `scripts/extract_fdic.py`
- **Loads to:** Snowflake `RAW.FDIC_FINANCIALS`

### Source 2 — Web Scrape: Competitive Intelligence
- **Targets:** Axos IR, Ally Bank, SoFi, Discover Bank, Marcus by Goldman Sachs
- **Raw files:** `knowledge/raw/`
- **Tool:** Firecrawl or requests + BeautifulSoup
- **Script:** `scripts/scrape_competitors.py`

---

## Directory Structure

```
.
├── .github/workflows/       # GitHub Actions pipelines
├── dbt/                     # dbt project (staging + mart models)
├── docs/                    # Proposal, job posting, specs, plans
│   ├── job-posting.pdf
│   ├── proposal.md
│   └── superpowers/
│       ├── specs/
│       └── plans/
├── knowledge/
│   ├── raw/                 # Scraped source files (15+ files, 3+ sources)
│   ├── wiki/                # Claude Code-generated wiki pages
│   └── index.md             # Index of all wiki pages
├── scripts/                 # Python extraction and scrape scripts
├── .env                     # Local credentials (never committed)
├── .gitignore
├── CLAUDE.md                # This file
└── README.md
```

---

## Snowflake Schema

- `RAW` — raw ingested data, one table per source
- `STAGING` — dbt staging models (cleaning, renaming, type casting)
- `MART` — dbt mart models (star schema: fact + dimension tables)

### Star Schema
- **Fact:** `fct_bank_financials` — one row per bank per quarter
- **Dims:** `dim_bank`, `dim_date`

---

## Credentials

Never commit credentials. All secrets are stored in:
- **Local:** `.env` file (gitignored)
- **CI/CD:** GitHub Actions repository secrets

Required environment variables:
```
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_DATABASE=
SNOWFLAKE_WAREHOUSE=
SNOWFLAKE_ROLE=
```

---

## Knowledge Base

### How to Query

To ask questions about the knowledge base during a Claude Code session:

1. Open Claude Code in this repo directory
2. Ask questions like:
   - "What does the knowledge base say about Axos Bank's competitive position?"
   - "How does Axos compare to SoFi based on the wiki?"
   - "What themes emerge across our scraped competitor sources?"
3. Claude Code will read `knowledge/wiki/` pages and `knowledge/raw/` sources to answer

### Wiki Pages

| File | Content |
|---|---|
| `knowledge/wiki/overview.md` | Axos Bank business model and market position |
| `knowledge/wiki/key-entities.md` | Competitor profiles (Ally, SoFi, Discover, Marcus) |
| `knowledge/wiki/competitive-themes.md` | Synthesis: how digital banks differentiate |

### Conventions

- Always read `knowledge/index.md` first to understand available wiki pages
- Prefer wiki pages for synthesized insights; use `knowledge/raw/` for source-level detail
- When answering questions, cite the specific wiki page or raw source file
