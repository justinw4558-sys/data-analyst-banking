# Proposal Design — U.S. Bank Performance & Competitive Intelligence Pipeline

**Date:** 2026-04-08
**Due:** 2026-04-13 at 9:55 AM

---

## Job Posting

**Role:** Jr. Data Analyst
**Company:** Axos Bank (NYSE: AX)
**Location:** San Diego, CA
**File:** `docs/job-posting.pdf`

**Key skills required:**
- SQL, Python, Tableau, Excel
- Financial statement analysis (P&L, balance sheet, cash flow)
- Budgeting, forecasting, financial reporting
- Data architecture, data integration

---

## Project Framing

**Project title:** U.S. Bank Performance & Competitive Intelligence Pipeline

**Repo name:** `data-analyst-banking`

**Transferability:** Applicable to similar roles at other banks (JPMorgan, Wells Fargo), fintechs (SoFi, Ally), or any organization doing financial performance reporting.

---

## Data Sources

### Source 1 — API: FDIC BankFind Suite
- **Endpoint:** `https://banks.data.fdic.gov/api/financials`
- **Auth:** None required (public API)
- **Data:** Quarterly call report data per institution — total assets, net income, ROA, ROE, net interest margin, non-interest income, efficiency ratio, loan totals
- **Scope:** All FDIC-insured institutions, 2015–present (~4,500+ active banks)
- **Load:** Python script → Snowflake `RAW` schema, scheduled via GitHub Actions

### Source 2 — Web Scrape: Competitive Intelligence
- **Targets:**
  - Axos Bank investor relations (earnings press releases, annual report highlights) — 5–6 files
  - Competitor IR/about pages: Ally Bank, SoFi, Discover Bank, Marcus by Goldman Sachs — 8–10 files
  - FDIC quarterly banking profiles — 1–2 files
- **Tool:** Firecrawl or requests + BeautifulSoup
- **Output:** Raw markdown/text → `knowledge/raw/`

---

## dbt Star Schema

### Fact Table: `fct_bank_financials`
- **Grain:** One row per bank per quarter
- **Metrics:** net income, total assets, total deposits, total loans, non-interest income, operating expenses
- **Derived:** ROA, ROE, net interest margin, efficiency ratio

### Dimension Tables
| Table | Key Fields |
|---|---|
| `dim_bank` | institution name, charter class, state, asset size tier, digital-first flag |
| `dim_date` | quarter, year, quarter label |

### Business Questions
- **Descriptive:** How has U.S. bank profitability trended by asset size tier from 2015–present?
- **Diagnostic:** Why do digital-first banks (Axos peer group) show different efficiency ratios vs. traditional banks?

---

## Streamlit Dashboard

### View 1 — U.S. Banking Landscape (Descriptive)
- Line chart: avg ROA/ROE by bank tier over time
- Bar chart: net interest margin distribution, latest quarter
- Filters: year range, asset size tier, state

### View 2 — Axos Peer Benchmarking (Diagnostic)
- Table + bar chart: Axos vs. digital-first peers on ROA, efficiency ratio, NIM
- Line chart: Axos profitability trend vs. peer group average over time
- Callout metric cards: Axos ROA vs. peer median

Shared sidebar: date range filter, peer group selector

---

## Knowledge Base

### Raw Sources (`knowledge/raw/`) — 15+ files, 3+ sources
- Axos IR: earnings press releases, annual report highlights
- Competitors: Ally, SoFi, Discover, Marcus IR/about pages
- FDIC quarterly banking profiles

### Wiki Pages (`knowledge/wiki/`)
| Page | Content |
|---|---|
| `overview.md` | Axos Bank business model, market position |
| `key-entities.md` | Competitor profiles (Ally, SoFi, Discover, Marcus) |
| `competitive-themes.md` | Synthesis: how digital banks differentiate on deposits, loans, efficiency |

### Index
`knowledge/index.md` — lists all wiki pages with one-line summaries

### CLAUDE.md Query Conventions
Instructions for querying the knowledge base during the final interview demo.

---

## Proposal Reflection Paragraph (Draft)

When I came across the Jr. Data Analyst posting at Axos Bank, it stood out because it asks for exactly what this course has been building toward. The role wants SQL, Python, and dashboarding experience — but it also wants someone who understands financial statements and can turn raw data into reporting that actually drives decisions. That combination is what made it feel like the right fit. For this project, I'm pulling FDIC call report data through a Python pipeline into Snowflake, transforming it with dbt into a star schema, and surfacing bank profitability trends and a peer benchmarking view for Axos in a Streamlit dashboard. The data architecture and integration work in the pipeline maps closely to what the Commercial Analytics team at Axos describes doing day-to-day. And because the dataset covers all FDIC-insured banks, this project doesn't just apply to one job — it's a foundation I can point to for similar roles across banking and fintech.

---

## Proposal Deliverables Checklist

- [ ] `docs/job-posting.pdf` — already committed
- [ ] `docs/proposal.md` — 1-page proposal using proposal-template.md, kept as markdown
- [ ] GitHub repo initialized with professional name, `.gitignore`, directory structure, `CLAUDE.md`
- [ ] Repo URL submitted to Brightspace by Apr 13 at 9:55 AM
