# Project Proposal

**Course:** ISBA 4715
**Student:** Justin Wang
**Date:** April 2026

---

## Job Posting

**Role:** Jr. Data Analyst
**Company:** Axos Bank
**Location:** San Diego, CA (4350 La Jolla Village Drive, Suite 140)
**Pay:** $25.20–$33.00/hr, Full-time
**File:** [`docs/job-posting.pdf`](job-posting.pdf)

---

## Project: U.S. Bank Performance & Competitive Intelligence Pipeline

**GitHub Repo:** [SQL-Project](https://github.com/justinw4558-sys/SQL-Project)

---

## Reflection

When I came across the Jr. Data Analyst posting at Axos Bank, it stood out because it asks for exactly what this course has been building toward. The role wants SQL, Python, and dashboarding experience — but it also wants someone who understands financial statements and can turn raw data into reporting that actually drives decisions. That combination is what made it feel like the right fit. For this project, I'm pulling FDIC call report data through a Python pipeline into Snowflake, transforming it with dbt into a star schema, and surfacing bank profitability trends and a peer benchmarking view for Axos in a Streamlit dashboard. The data architecture and integration work in the pipeline maps closely to what the Commercial Analytics team at Axos describes doing day-to-day. And because the dataset covers all FDIC-insured banks, this project doesn't just apply to one job — it's a foundation I can point to for similar roles across banking and fintech.

---

## Data Sources

| # | Type | Source | Purpose |
|---|---|---|---|
| 1 | API | FDIC BankFind Suite (`banks.data.fdic.gov/api/`) | Quarterly financials for all U.S. banks → Snowflake → dbt → dashboard |
| 2 | Web Scrape | Axos IR + competitor pages (Ally, SoFi, Discover, Marcus) | Competitive intelligence → knowledge base |

## Tech Stack

| Layer | Tool |
|---|---|
| Data Warehouse | Snowflake |
| Transformation | dbt (staging + mart / star schema) |
| Orchestration | GitHub Actions |
| Dashboard | Streamlit (Streamlit Community Cloud) |
| Knowledge Base | Claude Code |
