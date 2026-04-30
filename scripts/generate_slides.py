"""
generate_slides.py
==================
Generates docs/slides.pdf — the Milestone 02 presentation artifact.

Slide structure:
  1. Title
  2. Descriptive: Axos asset & ROA growth
  3. Diagnostic:  Peer NIM / ROA benchmarking
  4. Recommendation
  5. Data & Method

Run:
    python scripts/generate_slides.py
"""

import os
import textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

# ── Snowflake pull ─────────────────────────────────────────────────────────────
def get_data():
    conn = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema="STAGING_MART",
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT year_quarter, date_key,
               total_assets, return_on_assets, net_interest_margin, net_income
        FROM STAGING_MART.FCT_BANK_FINANCIALS
        WHERE is_axos = TRUE
        ORDER BY date_key
    """)
    axos = pd.DataFrame(cur.fetchall(),
                        columns=["yq","date_key","assets","roa","nim","net_income"])

    cur.execute("""
        SELECT peer_group_name, year_quarter, date_key,
               total_assets, return_on_assets, return_on_equity, net_interest_margin
        FROM STAGING_MART.FCT_BANK_FINANCIALS
        WHERE peer_group_name IS NOT NULL
        ORDER BY peer_group_name, date_key
    """)
    peers = pd.DataFrame(cur.fetchall(),
                         columns=["bank","yq","date_key","assets","roa","roe","nim"])

    cur.execute("""
        SELECT MEDIAN(return_on_assets), MEDIAN(net_interest_margin)
        FROM STAGING_MART.FCT_BANK_FINANCIALS
        WHERE date_key = (SELECT MAX(date_key) FROM STAGING_MART.FCT_BANK_FINANCIALS)
          AND return_on_assets IS NOT NULL
    """)
    row = cur.fetchone()
    industry = {"roa": float(row[0]), "nim": float(row[1])}

    cur.close()
    conn.close()
    return axos, peers, industry


# ── Design tokens ──────────────────────────────────────────────────────────────
NAVY   = "#003DA5"
BLUE   = "#4472C4"
GRAY   = "#6B6B6B"
LGRAY  = "#E8EBF0"
WHITE  = "#FFFFFF"
ACCENT = "#F2A900"   # gold callout
RED    = "#C00000"

PEER_COLORS = {
    "Axos Bank":       NAVY,
    "Ally Bank":       "#7D00B5",
    "SoFi Bank":       "#00A87F",
    "LendingClub Bank":"#FF6B00",
}

W, H = 13.33, 7.5   # 16:9 inches

def fig():
    f = plt.figure(figsize=(W, H), facecolor=WHITE)
    return f

def header_bar(f, title, subtitle=None):
    """Navy top bar with white title text."""
    ax = f.add_axes([0, 0.87, 1, 0.13], facecolor=NAVY)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.03, 0.6, title, color=WHITE,
            fontsize=18, fontweight="bold", va="center", ha="left",
            transform=ax.transAxes)
    if subtitle:
        ax.text(0.03, 0.18, subtitle, color="#B0C4DE",
                fontsize=10, va="center", ha="left",
                transform=ax.transAxes)

def footer(f, note="Source: FDIC BankFind Suite · ISBA 4715 · Justin Wang"):
    ax = f.add_axes([0, 0, 1, 0.04], facecolor=LGRAY)
    ax.axis("off")
    ax.text(0.5, 0.5, note, color=GRAY, fontsize=8,
            ha="center", va="center", transform=ax.transAxes)

def callout_box(ax, x, y, text, width=0.28, height=0.14,
                facecolor=ACCENT, textcolor="black"):
    """Rounded callout box in axes-fraction coordinates."""
    fancy = mpatches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.01",
        facecolor=facecolor, edgecolor="white", linewidth=1.5,
        transform=ax.transAxes, zorder=5, clip_on=False,
    )
    ax.add_patch(fancy)
    ax.text(x + width / 2, y + height / 2, text,
            color=textcolor, fontsize=9, fontweight="bold",
            ha="center", va="center",
            transform=ax.transAxes, zorder=6, clip_on=False,
            wrap=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title
# ══════════════════════════════════════════════════════════════════════════════
def slide_title():
    f = plt.figure(figsize=(W, H), facecolor=NAVY)
    ax = f.add_axes([0, 0, 1, 1], facecolor=NAVY)
    ax.axis("off")

    ax.text(0.5, 0.72,
            "Axos Bank Performance &\nCompetitive Intelligence",
            color=WHITE, fontsize=34, fontweight="bold",
            ha="center", va="center", transform=ax.transAxes,
            linespacing=1.3)

    ax.text(0.5, 0.52,
            "End-to-end data pipeline: FDIC API → Snowflake → dbt → Streamlit",
            color="#B0C4DE", fontsize=14, ha="center", va="center",
            transform=ax.transAxes)

    # gold divider
    ax.plot([0.25, 0.75], [0.43, 0.43], color=ACCENT, linewidth=2,
            transform=ax.transAxes)

    ax.text(0.5, 0.34,
            "Justin Wang  ·  ISBA 4715 Analytics Engineering  ·  LMU",
            color="#B0C4DE", fontsize=12, ha="center", va="center",
            transform=ax.transAxes)

    # tech stack row
    tools = ["FDIC API", "GitHub Actions", "Snowflake", "dbt", "Streamlit"]
    for i, t in enumerate(tools):
        x = 0.18 + i * 0.16
        fancy = mpatches.FancyBboxPatch(
            (x - 0.06, 0.10), 0.12, 0.10,
            boxstyle="round,pad=0.01",
            facecolor="#0A2A6E", edgecolor=ACCENT, linewidth=1,
            transform=ax.transAxes, zorder=5,
        )
        ax.add_patch(fancy)
        ax.text(x, 0.155, t, color=WHITE, fontsize=9, fontweight="bold",
                ha="center", va="center", transform=ax.transAxes, zorder=6)

    return f


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Descriptive
# ══════════════════════════════════════════════════════════════════════════════
def slide_descriptive(axos):
    f = fig()
    header_bar(f,
               "Axos Doubled Assets to $27B While Sustaining ROA 60% Above the Industry",
               subtitle="Descriptive: What happened?")
    footer(f)

    # main chart area
    ax1 = f.add_axes([0.06, 0.14, 0.60, 0.69])

    x = range(len(axos))
    labels = axos["yq"].tolist()
    assets_b = axos["assets"] / 1_000_000

    # asset area
    ax1.fill_between(x, assets_b, alpha=0.15, color=NAVY)
    ax1.plot(x, assets_b, color=NAVY, linewidth=2.5, label="Total Assets ($B)")
    ax1.set_ylabel("Total Assets ($B)", color=NAVY, fontsize=11)
    ax1.tick_params(axis="y", labelcolor=NAVY)

    # ROA line — right axis
    ax2 = ax1.twinx()
    ax2.plot(x, axos["roa"], color=ACCENT, linewidth=2.5,
             linestyle="--", marker="o", markersize=4, label="ROA (%)")
    ax2.axhline(y=1.10, color=RED, linewidth=1.2, linestyle=":",
                label="Industry Median ROA (1.10%)")
    ax2.set_ylabel("Return on Assets (%)", color=ACCENT, fontsize=11)
    ax2.tick_params(axis="y", labelcolor=ACCENT)
    ax2.set_ylim(0, 3.5)

    # x ticks — every 4 quarters
    tick_idx = list(range(0, len(labels), 4))
    ax1.set_xticks(tick_idx)
    ax1.set_xticklabels([labels[i] for i in tick_idx], rotation=30, ha="right", fontsize=9)
    ax1.set_xlim(-0.5, len(x) - 0.5)

    # combined legend
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8, framealpha=0.85)
    ax1.grid(axis="y", alpha=0.3)

    # callout panel on right
    panel = f.add_axes([0.70, 0.30, 0.27, 0.55], facecolor=LGRAY)
    panel.axis("off")

    latest = axos.iloc[-1]
    first  = axos.iloc[0]
    growth = (latest["assets"] - first["assets"]) / first["assets"] * 100

    panel.text(0.5, 0.96, "Q4 2025 Snapshot", color=NAVY,
               fontsize=11, fontweight="bold", ha="center", va="top",
               transform=panel.transAxes)
    panel.plot([0, 1], [0.91, 0.91], color=NAVY, linewidth=1, transform=panel.transAxes)

    stats = [
        ("Total Assets",    f"${latest['assets']/1e6:.1f}B"),
        ("Asset Growth\n(2020→2025)", f"+{growth:.0f}%"),
        ("ROA",             f"{latest['roa']:.2f}%"),
        ("Industry Median", "1.10%"),
        ("Outperformance",  f"+{latest['roa']-1.10:.2f} pp"),
        ("NIM",             f"{latest['nim']:.2f}%"),
    ]
    for i, (label, val) in enumerate(stats):
        y = 0.84 - i * 0.145
        panel.text(0.05, y, label, color=GRAY, fontsize=8.5, va="top",
                   transform=panel.transAxes)
        color = RED if "Median" in label else (ACCENT if "Out" in label else NAVY)
        panel.text(0.95, y, val, color=color, fontsize=10, fontweight="bold",
                   ha="right", va="top", transform=panel.transAxes)

    # highlight callout arrow pointing to Q4 2025 on chart
    last_x = len(x) - 1
    ax1.annotate(
        "  Q4 2025\n  $27.2B",
        xy=(last_x, assets_b.iloc[-1]),
        xytext=(last_x - 5, assets_b.iloc[-1] + 2),
        fontsize=8.5, color=NAVY, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5),
    )

    return f


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Diagnostic
# ══════════════════════════════════════════════════════════════════════════════
def slide_diagnostic(peers, industry):
    f = fig()
    header_bar(f,
               "Axos's 4.9% NIM Reflects a Structural Cost Advantage — Not Just Rate Tailwinds",
               subtitle="Diagnostic: Why did it happen?")
    footer(f)

    latest_dt = peers["date_key"].max()
    snap = peers[peers["date_key"] == latest_dt].copy()
    snap = snap.sort_values("nim", ascending=True)

    banks   = snap["bank"].tolist()
    nims    = snap["nim"].tolist()
    roas    = snap["roa"].tolist()
    colors  = [PEER_COLORS.get(b, GRAY) for b in banks]

    ax = f.add_axes([0.06, 0.14, 0.56, 0.69])

    bar_width = 0.35
    x = np.arange(len(banks))

    bars1 = ax.barh(x + bar_width/2, nims,  bar_width, label="NIM (%)",
                    color=colors, alpha=0.9)
    bars2 = ax.barh(x - bar_width/2, roas,  bar_width, label="ROA (%)",
                    color=colors, alpha=0.4, hatch="///")

    # industry median lines
    ax.axvline(x=industry["nim"], color=RED, linestyle=":", linewidth=1.5,
               label=f"Industry Median NIM ({industry['nim']:.2f}%)")
    ax.axvline(x=industry["roa"], color=RED, linestyle="--", linewidth=1.5,
               label=f"Industry Median ROA ({industry['roa']:.2f}%)")

    ax.set_yticks(x)
    ax.set_yticklabels(banks, fontsize=10)
    ax.set_xlabel("Percent (%)", fontsize=10)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="x", alpha=0.3)

    # value labels
    for bar in bars1:
        w = bar.get_width()
        ax.text(w + 0.05, bar.get_y() + bar.get_height()/2,
                f"{w:.2f}%", va="center", fontsize=8.5, color=NAVY, fontweight="bold")
    for bar in bars2:
        w = bar.get_width()
        ax.text(w + 0.05, bar.get_y() + bar.get_height()/2,
                f"{w:.2f}%", va="center", fontsize=8.5, color=GRAY)

    # right panel
    panel = f.add_axes([0.66, 0.14, 0.31, 0.69], facecolor=LGRAY)
    panel.axis("off")

    axos_row = snap[snap["bank"] == "Axos Bank"].iloc[0]
    nim_gap  = axos_row["nim"] - industry["nim"]
    roa_gap  = axos_row["roa"] - industry["roa"]

    panel.text(0.5, 0.97, "Why Axos Outperforms", color=NAVY,
               fontsize=11, fontweight="bold", ha="center", va="top",
               transform=panel.transAxes)
    panel.plot([0, 1], [0.91, 0.91], color=NAVY, linewidth=1, transform=panel.transAxes)

    bullets = [
        ("No branch network",
         "Zero physical overhead → interest income flows directly to bottom line"),
        ("Disciplined deposit pricing",
         "Branchless model allows below-peer deposit rates without losing customers"),
        (f"NIM premium: +{nim_gap:.2f} pp",
         f"Axos NIM of {axos_row['nim']:.2f}% vs {industry['nim']:.2f}% industry median"),
        (f"ROA premium: +{roa_gap:.2f} pp",
         f"Axos ROA of {axos_row['roa']:.2f}% vs {industry['roa']:.2f}% industry median"),
    ]

    y = 0.87
    for title, body in bullets:
        panel.text(0.04, y, f"▶  {title}", color=NAVY, fontsize=8.5,
                   fontweight="bold", va="top", transform=panel.transAxes)
        for line in textwrap.wrap(body, width=38):
            y -= 0.07
            panel.text(0.06, y, line, color=GRAY, fontsize=7.5,
                       va="top", transform=panel.transAxes)
        y -= 0.10

    return f


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Recommendation
# ══════════════════════════════════════════════════════════════════════════════
def slide_recommendation(axos, industry):
    f = fig()
    header_bar(f, "Recommendation", subtitle="Action → Expected Outcome")
    footer(f)

    ax = f.add_axes([0, 0.04, 1, 0.83], facecolor=WHITE)
    ax.axis("off")

    # large action → outcome arrow
    ax.text(0.5, 0.85,
            "Accelerate fee-based revenue (Axos Invest + Axos Clearing)",
            color=NAVY, fontsize=16, fontweight="bold",
            ha="center", va="center", transform=ax.transAxes)

    ax.annotate("", xy=(0.5, 0.60), xytext=(0.5, 0.75),
                xycoords="axes fraction", textcoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color=ACCENT,
                                lw=4, mutation_scale=30))

    ax.text(0.5, 0.52,
            "Sustain ROA ≥ 1.7% as interest rates normalize",
            color=ACCENT, fontsize=16, fontweight="bold",
            ha="center", va="center", transform=ax.transAxes)

    # supporting evidence boxes
    evidence = [
        ("The Risk",
         "Axos NIM has compressed\nfrom 5.3% (2020) to ~4.9%\nas rates peaked and plateau.\nFurther normalization will\nsqueeze net interest income."),
        ("The Opportunity",
         "SoFi's super-app model shows\nfee income can offset NIM\npressure. Axos Invest AUM\nand Axos Clearing revenue\nare underpenetrated vs. SoFi."),
        ("The Precedent",
         "Ally Bank's ROA fell to 0.91%\nas it relied solely on NIM.\nAxos must diversify before\nrate headwinds materialize\nat scale."),
    ]

    box_w, box_h = 0.26, 0.36
    for i, (title, body) in enumerate(evidence):
        x0 = 0.06 + i * 0.31
        fancy = mpatches.FancyBboxPatch(
            (x0, 0.04), box_w, box_h,
            boxstyle="round,pad=0.015",
            facecolor=LGRAY, edgecolor=NAVY, linewidth=1.5,
            transform=ax.transAxes, zorder=3,
        )
        ax.add_patch(fancy)
        ax.text(x0 + box_w/2, 0.04 + box_h - 0.04,
                title, color=NAVY, fontsize=10, fontweight="bold",
                ha="center", va="top", transform=ax.transAxes, zorder=4)
        ax.text(x0 + box_w/2, 0.04 + box_h - 0.10,
                body, color=GRAY, fontsize=8.5,
                ha="center", va="top", transform=ax.transAxes, zorder=4,
                linespacing=1.4)

    return f


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Data & Method
# ══════════════════════════════════════════════════════════════════════════════
def slide_method(axos):
    f = fig()
    header_bar(f, "Data & Method", subtitle="How it was built")
    footer(f)

    ax = f.add_axes([0, 0.04, 1, 0.83], facecolor=WHITE)
    ax.axis("off")

    layers = [
        ("FDIC BankFind\nSuite API",  "114,781 bank-quarters\n2020–2025\nAll FDIC-insured banks",   NAVY),
        ("GitHub Actions",            "Weekly automated\npipeline\nScheduled + manual",             BLUE),
        ("Snowflake RAW",             "Raw ingestion\nTruncate + reload\nbatch strategy",           "#005A8E"),
        ("dbt (Staging\n+ Mart)",     "17 tests passing\nStar schema:\nfact + 2 dims",              "#F97316"),
        ("Streamlit\nDashboard",      "3 interactive tabs\nPublic URL\nSnowflake-connected",        "#00A87F"),
    ]

    n = len(layers)
    box_w = 0.14
    gap   = (1 - n * box_w - 0.04) / (n - 1)
    y0    = 0.25

    for i, (title, body, color) in enumerate(layers):
        x0 = 0.02 + i * (box_w + gap)
        fancy = mpatches.FancyBboxPatch(
            (x0, y0), box_w, 0.50,
            boxstyle="round,pad=0.01",
            facecolor=color, edgecolor="white", linewidth=2,
            transform=ax.transAxes, zorder=3,
        )
        ax.add_patch(fancy)
        ax.text(x0 + box_w/2, y0 + 0.44,
                title, color=WHITE, fontsize=9.5, fontweight="bold",
                ha="center", va="top", transform=ax.transAxes, zorder=4,
                linespacing=1.3)
        ax.text(x0 + box_w/2, y0 + 0.26,
                body, color="#D0E4FF", fontsize=8,
                ha="center", va="top", transform=ax.transAxes, zorder=4,
                linespacing=1.4)

        if i < n - 1:
            ax.annotate("", xy=(x0 + box_w + gap * 0.1, y0 + 0.25),
                        xytext=(x0 + box_w + gap * 0.02, y0 + 0.25),
                        xycoords="axes fraction", textcoords="axes fraction",
                        arrowprops=dict(arrowstyle="-|>", color=GRAY,
                                        lw=2, mutation_scale=18))

    # stats row
    stats = [
        ("114,781", "bank-quarters loaded"),
        ("5,242",   "FDIC-insured banks"),
        ("24",      "quarters (2020–2025)"),
        ("17",      "dbt tests passing"),
        ("4",       "peer banks benchmarked"),
    ]
    for i, (num, label) in enumerate(stats):
        x = 0.09 + i * 0.20
        ax.text(x, 0.18, num, color=NAVY, fontsize=20, fontweight="bold",
                ha="center", va="center", transform=ax.transAxes)
        ax.text(x, 0.10, label, color=GRAY, fontsize=8.5,
                ha="center", va="center", transform=ax.transAxes)

    return f


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Pulling data from Snowflake…")
    axos, peers, industry = get_data()

    out_path = os.path.join(os.path.dirname(__file__), "..", "docs", "slides.pdf")
    out_path = os.path.normpath(out_path)

    print("Building slides…")
    with PdfPages(out_path) as pdf:
        for slide_fn in [
            lambda: slide_title(),
            lambda: slide_descriptive(axos),
            lambda: slide_diagnostic(peers, industry),
            lambda: slide_recommendation(axos, industry),
            lambda: slide_method(axos),
        ]:
            fig_obj = slide_fn()
            pdf.savefig(fig_obj, bbox_inches="tight")
            plt.close(fig_obj)

    print(f"Saved → {out_path}")
