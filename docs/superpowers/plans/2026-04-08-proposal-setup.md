# Proposal Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create all deliverables required for the Proposal milestone (due Apr 13): `CLAUDE.md`, directory structure, and `docs/proposal.md`.

**Architecture:** Pure file creation and git operations — no code to run. Each task produces a committed file. The proposal is a markdown document; CLAUDE.md provides project context for future Claude Code sessions.

**Tech Stack:** Git, GitHub CLI (`gh`), Markdown

---

## File Map

| Action | Path | Purpose |
|---|---|---|
| Modify | `.gitignore` | Add `.DS_Store` |
| Create | `CLAUDE.md` | Project context for Claude Code sessions |
| Create | `docs/proposal.md` | 1-page proposal with reflection paragraph |
| Create | `knowledge/raw/.gitkeep` | Placeholder for web scrape sources |
| Create | `knowledge/wiki/.gitkeep` | Placeholder for Claude-generated wiki pages |
| Create | `knowledge/index.md` | Index of all wiki pages |
| Create | `scripts/.gitkeep` | Placeholder for Python extraction scripts |
| Create | `dbt/.gitkeep` | Placeholder for dbt project |
| Create | `.github/workflows/.gitkeep` | Placeholder for GitHub Actions |

---

## Task 1: Fix .gitignore

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Add `.DS_Store` to .gitignore**

Add this block at the top of `.gitignore` (before the existing content):

```
# macOS
.DS_Store
```

- [ ] **Step 2: Verify .DS_Store is now ignored**

Run:
```bash
git check-ignore -v .DS_Store
```
Expected output: `.gitignore:1:.DS_Store    .DS_Store`

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: ignore .DS_Store"
```

---

## Task 2: Create CLAUDE.md

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Create CLAUDE.md with project context**

Create `CLAUDE.md` at the repo root with this content:

```markdown
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
```

- [ ] **Step 2: Verify file exists**

Run:
```bash
ls -la CLAUDE.md
```
Expected: file listed with non-zero size

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md with project context and knowledge base conventions"
```

---

## Task 3: Create Directory Structure

**Files:**
- Create: `knowledge/raw/.gitkeep`
- Create: `knowledge/wiki/.gitkeep`
- Create: `knowledge/index.md`
- Create: `scripts/.gitkeep`
- Create: `dbt/.gitkeep`
- Create: `.github/workflows/.gitkeep`

- [ ] **Step 1: Create placeholder directories**

Run:
```bash
mkdir -p knowledge/raw knowledge/wiki scripts dbt .github/workflows
touch knowledge/raw/.gitkeep knowledge/wiki/.gitkeep scripts/.gitkeep dbt/.gitkeep .github/workflows/.gitkeep
```

- [ ] **Step 2: Create knowledge/index.md**

Create `knowledge/index.md` with this content:

```markdown
# Knowledge Base Index

This index lists all wiki pages in `knowledge/wiki/`. Use this file first when
querying the knowledge base via Claude Code.

## Wiki Pages

| Page | Summary |
|---|---|
| [overview.md](wiki/overview.md) | Axos Bank business model, history, and market position |
| [key-entities.md](wiki/key-entities.md) | Profiles of key competitors: Ally, SoFi, Discover, Marcus |
| [competitive-themes.md](wiki/competitive-themes.md) | Synthesis of how digital banks differentiate on deposits, loans, and efficiency |

## Raw Sources

Raw scraped files are in `knowledge/raw/`. Sources include:
- Axos Bank investor relations (earnings press releases, annual highlights)
- Competitor IR/about pages: Ally Bank, SoFi, Discover Bank, Marcus by Goldman Sachs
- FDIC quarterly banking profiles

_Wiki pages are generated by Claude Code from raw sources. See CLAUDE.md for query conventions._
```

- [ ] **Step 3: Verify structure**

Run:
```bash
find knowledge scripts dbt .github -type f | sort
```
Expected output:
```
.github/workflows/.gitkeep
dbt/.gitkeep
knowledge/index.md
knowledge/raw/.gitkeep
knowledge/wiki/.gitkeep
scripts/.gitkeep
```

- [ ] **Step 4: Commit**

```bash
git add knowledge/ scripts/ dbt/ .github/
git commit -m "chore: scaffold directory structure for pipeline and knowledge base"
```

---

## Task 4: Create docs/proposal.md

**Files:**
- Create: `docs/proposal.md`

- [ ] **Step 1: Create docs/proposal.md**

Create `docs/proposal.md` with this content:

```markdown
# Project Proposal

**Course:** ISBA 4715
**Student:** [Your Name]
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

**GitHub Repo:** [data-analyst-banking](https://github.com/[your-username]/data-analyst-banking)

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
```

- [ ] **Step 2: Fill in your name and GitHub username**

In `docs/proposal.md`:
- Replace `[Your Name]` with your actual name
- Replace `[your-username]` in the repo URL with your GitHub username

- [ ] **Step 3: Verify the file renders correctly**

Open `docs/proposal.md` in your editor and confirm:
- Name and GitHub username are filled in
- Job posting link points to `job-posting.pdf`
- All table columns are aligned

- [ ] **Step 4: Commit**

```bash
git add docs/proposal.md
git commit -m "docs: add project proposal for Jr. Data Analyst at Axos Bank"
```

---

## Task 5: Push to GitHub and Verify

- [ ] **Step 1: Push all commits to remote**

```bash
git push origin main
```
Expected: all 4 commits pushed, no errors

- [ ] **Step 2: Verify repo is public**

Run:
```bash
gh repo view --json visibility -q .visibility
```
Expected output: `PUBLIC`

If output is `PRIVATE`, run:
```bash
gh repo edit --visibility public
```

- [ ] **Step 3: Verify all required files are present on GitHub**

Run:
```bash
gh repo view --web
```
Confirm in browser:
- `CLAUDE.md` is visible at repo root
- `docs/job-posting.pdf` is present
- `docs/proposal.md` is present
- Directory structure (`knowledge/`, `scripts/`, `dbt/`, `.github/`) is visible

- [ ] **Step 4: Copy the repo URL for Brightspace submission**

Run:
```bash
gh repo view --json url -q .url
```
Copy the output URL — this is what you submit to Brightspace.

---

## Deliverables Checklist (Proposal — 10 pts)

| # | Deliverable | File | Status |
|---|---|---|---|
| 1 | Job posting PDF | `docs/job-posting.pdf` | Already committed |
| 2 | Proposal with reflection | `docs/proposal.md` | Task 4 |
| 3 | GitHub repo initialized | `CLAUDE.md`, directory structure | Tasks 1–3 |
