"""
Axos Bank Performance & Competitive Intelligence Dashboard
=========================================================
ISBA 4715 — Analytics Engineering | Justin Wang

Connects to Snowflake STAGING_MART schema and surfaces:
  • Descriptive:  Axos Bank financial trends over time
  • Diagnostic:   Axos vs. peer-bank benchmarking
  • Interactive:  user-driven metric/bank exploration
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import snowflake.connector

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Axos Bank Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── connection ─────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_connection():
    """Return a Snowflake connection, reading creds from st.secrets."""
    return snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        role=st.secrets["snowflake"]["role"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema="STAGING_MART",
    )


@st.cache_data(ttl=3600, show_spinner="Loading data from Snowflake…")
def load_data():
    """Pull all mart data into DataFrames (cached 1 hour)."""
    conn = get_connection()
    cur = conn.cursor()

    fact_sql = """
        SELECT
            f.fact_id,
            f.bank_id,
            f.bank_name,
            f.date_key,
            f.year_quarter,
            f.report_year,
            f.report_quarter,
            f.is_axos,
            f.peer_group_name,
            f.total_assets,
            f.total_deposits,
            f.net_loans,
            f.total_equity,
            f.total_securities,
            f.net_income,
            f.interest_income,
            f.noninterest_income,
            f.noninterest_expense,
            f.total_revenue,
            f.net_interest_margin,
            f.return_on_assets,
            f.return_on_equity,
            f.loans_to_deposits_ratio
        FROM STAGING_MART.FCT_BANK_FINANCIALS f
        ORDER BY f.bank_id, f.date_key
    """

    cur.execute(fact_sql)
    cols = [c[0].lower() for c in cur.description]
    fact = pd.DataFrame(cur.fetchall(), columns=cols)

    # numeric coerce
    num_cols = [
        "total_assets", "total_deposits", "net_loans", "total_equity",
        "total_securities", "net_income", "interest_income",
        "noninterest_income", "noninterest_expense", "total_revenue",
        "net_interest_margin", "return_on_assets", "return_on_equity",
        "loans_to_deposits_ratio",
    ]
    for c in num_cols:
        fact[c] = pd.to_numeric(fact[c], errors="coerce")

    cur.close()
    return fact


# ── helpers ────────────────────────────────────────────────────────────────────
PEERS = ["Axos Bank", "Ally Bank", "SoFi Bank", "LendingClub Bank"]
PEER_COLORS = {
    "Axos Bank": "#003DA5",        # Axos navy
    "Ally Bank": "#7D00B5",        # Ally purple
    "SoFi Bank": "#00A87F",        # SoFi teal
    "LendingClub Bank": "#FF6B00", # LC orange
}

METRIC_LABELS = {
    "total_assets": "Total Assets ($K)",
    "total_deposits": "Total Deposits ($K)",
    "net_loans": "Net Loans ($K)",
    "net_income": "Net Income ($K)",
    "total_revenue": "Total Revenue ($K)",
    "net_interest_margin": "Net Interest Margin (%)",
    "return_on_assets": "Return on Assets (%)",
    "return_on_equity": "Return on Equity (%)",
    "loans_to_deposits_ratio": "Loans-to-Deposits Ratio (%)",
}

def fmt_billions(val):
    if pd.isna(val):
        return "N/A"
    if abs(val) >= 1_000_000:
        return f"${val/1_000_000:.1f}B"
    if abs(val) >= 1_000:
        return f"${val/1_000:.0f}M"
    return f"${val:,.0f}K"

def fmt_pct(val, decimals=2):
    return "N/A" if pd.isna(val) else f"{val:.{decimals}f}%"


# ── load ───────────────────────────────────────────────────────────────────────
fact = load_data()

axos = fact[fact["is_axos"] == True].sort_values("date_key")
peers = fact[fact["peer_group_name"].notna()].sort_values("date_key")

# ── sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Axos_Financial_logo.svg/320px-Axos_Financial_logo.svg.png",
    width=160,
)
st.sidebar.title("Axos Bank Intelligence")
st.sidebar.caption("ISBA 4715 · Justin Wang · LMU")

st.sidebar.divider()

years = sorted(fact["report_year"].dropna().unique().tolist())
min_yr, max_yr = int(min(years)), int(max(years))
yr_range = st.sidebar.slider(
    "Year range",
    min_value=min_yr,
    max_value=max_yr,
    value=(min_yr, max_yr),
    step=1,
)

st.sidebar.divider()
selected_metric = st.sidebar.selectbox(
    "Metric (Peer Comparison tab)",
    options=list(METRIC_LABELS.keys()),
    format_func=lambda k: METRIC_LABELS[k],
    index=6,  # default: return_on_assets
)

st.sidebar.divider()
st.sidebar.markdown("**Data source:** FDIC BankFind Suite  \n**Refresh:** Weekly (GitHub Actions)  \n**Rows:** 114,781 bank-quarters")

# ── filter to year range ───────────────────────────────────────────────────────
axos_f = axos[axos["report_year"].between(yr_range[0], yr_range[1])]
peers_f = peers[peers["report_year"].between(yr_range[0], yr_range[1])]
fact_f  = fact[fact["report_year"].between(yr_range[0], yr_range[1])]

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(
    ["🏦  Axos Overview", "📊  Peer Benchmarking", "🔍  Custom Explorer"]
)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Axos Overview (Descriptive)
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.header("Axos Bank — Financial Overview")
    st.caption(
        "Axos Bank (FDIC cert #35546) is a full-service, branchless bank founded in 2000. "
        "All figures in thousands of dollars from FDIC quarterly call reports."
    )

    # KPI cards — most recent quarter
    latest = axos_f.sort_values("date_key").iloc[-1] if not axos_f.empty else None
    if latest is not None:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Assets", fmt_billions(latest["total_assets"]))
        c2.metric("Total Deposits", fmt_billions(latest["total_deposits"]))
        c3.metric("Return on Assets", fmt_pct(latest["return_on_assets"]))
        c4.metric("Net Interest Margin", fmt_pct(latest["net_interest_margin"]))
        st.caption(f"As of {latest['year_quarter']}")

    st.divider()

    # ── Balance Sheet Growth ──────────────────────────────────────────────────
    st.subheader("Balance Sheet Growth")
    fig_bs = go.Figure()
    fig_bs.add_trace(go.Scatter(
        x=axos_f["year_quarter"], y=axos_f["total_assets"] / 1_000_000,
        name="Total Assets ($B)", mode="lines+markers", line=dict(color="#003DA5", width=2),
    ))
    fig_bs.add_trace(go.Scatter(
        x=axos_f["year_quarter"], y=axos_f["total_deposits"] / 1_000_000,
        name="Total Deposits ($B)", mode="lines+markers", line=dict(color="#4472C4", width=2, dash="dash"),
    ))
    fig_bs.add_trace(go.Scatter(
        x=axos_f["year_quarter"], y=axos_f["net_loans"] / 1_000_000,
        name="Net Loans ($B)", mode="lines+markers", line=dict(color="#70AD47", width=2, dash="dot"),
    ))
    fig_bs.update_layout(
        yaxis_title="Billions ($)", xaxis_title="Quarter",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=380, margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig_bs, use_container_width=True)

    st.divider()

    # ── Profitability Trends ──────────────────────────────────────────────────
    st.subheader("Profitability Trends")
    col_left, col_right = st.columns(2)

    with col_left:
        fig_roa = px.area(
            axos_f, x="year_quarter", y="return_on_assets",
            title="Return on Assets (%)",
            color_discrete_sequence=["#003DA5"],
        )
        fig_roa.update_layout(
            showlegend=False, height=280,
            margin=dict(l=0, r=0, t=40, b=0),
            yaxis_title="%", xaxis_title="",
        )
        st.plotly_chart(fig_roa, use_container_width=True)

    with col_right:
        fig_nim = px.area(
            axos_f, x="year_quarter", y="net_interest_margin",
            title="Net Interest Margin (%)",
            color_discrete_sequence=["#4472C4"],
        )
        fig_nim.update_layout(
            showlegend=False, height=280,
            margin=dict(l=0, r=0, t=40, b=0),
            yaxis_title="%", xaxis_title="",
        )
        st.plotly_chart(fig_nim, use_container_width=True)

    st.divider()

    # ── Net Income Bar ────────────────────────────────────────────────────────
    st.subheader("Quarterly Net Income")
    fig_ni = px.bar(
        axos_f, x="year_quarter", y="net_income",
        title="Net Income ($K)",
        color_discrete_sequence=["#003DA5"],
    )
    fig_ni.update_layout(
        height=300, margin=dict(l=0, r=0, t=40, b=0),
        yaxis_title="$K", xaxis_title="Quarter", showlegend=False,
    )
    st.plotly_chart(fig_ni, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Peer Benchmarking (Diagnostic)
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.header("Peer Benchmarking")
    st.caption(
        "Axos vs. Ally Bank, SoFi Bank, and LendingClub Bank — all FDIC-insured digital banks. "
        f"Showing **{METRIC_LABELS[selected_metric]}** — change the metric in the sidebar."
    )

    # ── Line chart: selected metric over time ─────────────────────────────────
    peer_pivot = (
        peers_f[peers_f["peer_group_name"].isin(PEERS)]
        .sort_values("date_key")
    )

    fig_peer = px.line(
        peer_pivot,
        x="year_quarter",
        y=selected_metric,
        color="peer_group_name",
        markers=True,
        color_discrete_map=PEER_COLORS,
        title=f"{METRIC_LABELS[selected_metric]} — Quarterly Trend",
    )
    fig_peer.update_layout(
        height=420, legend_title="Bank",
        margin=dict(l=0, r=0, t=50, b=0),
        yaxis_title=METRIC_LABELS[selected_metric],
        xaxis_title="Quarter",
    )
    st.plotly_chart(fig_peer, use_container_width=True)

    st.divider()

    # ── Latest quarter snapshot table ─────────────────────────────────────────
    st.subheader("Latest Quarter Snapshot")

    snapshot_metrics = [
        "total_assets", "net_income", "return_on_assets",
        "return_on_equity", "net_interest_margin", "loans_to_deposits_ratio",
    ]

    latest_quarter = peers_f["date_key"].max()
    snap = (
        peers_f[
            (peers_f["date_key"] == latest_quarter) &
            (peers_f["peer_group_name"].isin(PEERS))
        ]
        [["peer_group_name"] + snapshot_metrics]
        .set_index("peer_group_name")
    )

    if not snap.empty:
        snap_display = snap.copy()
        snap_display["total_assets"] = snap_display["total_assets"].apply(fmt_billions)
        snap_display["net_income"]    = snap_display["net_income"].apply(fmt_billions)
        snap_display["return_on_assets"]       = snap_display["return_on_assets"].apply(fmt_pct)
        snap_display["return_on_equity"]       = snap_display["return_on_equity"].apply(fmt_pct)
        snap_display["net_interest_margin"]    = snap_display["net_interest_margin"].apply(fmt_pct)
        snap_display["loans_to_deposits_ratio"] = snap_display["loans_to_deposits_ratio"].apply(fmt_pct)
        snap_display.columns = [
            "Total Assets", "Net Income", "ROA", "ROE", "NIM", "Loans/Deposits"
        ]
        snap_display.index.name = "Bank"
        st.dataframe(snap_display, use_container_width=True)
        st.caption(f"Data as of {latest_quarter}")

    st.divider()

    # ── ROA vs NIM scatter ────────────────────────────────────────────────────
    st.subheader("ROA vs. Net Interest Margin — All Quarters")
    scatter_data = peers_f[peers_f["peer_group_name"].isin(PEERS)].dropna(
        subset=["return_on_assets", "net_interest_margin"]
    )
    fig_scatter = px.scatter(
        scatter_data,
        x="net_interest_margin",
        y="return_on_assets",
        color="peer_group_name",
        hover_data=["year_quarter", "bank_name"],
        color_discrete_map=PEER_COLORS,
        opacity=0.75,
        title="ROA vs. NIM (each point = one bank-quarter)",
    )
    fig_scatter.update_layout(
        height=400, legend_title="Bank",
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis_title="Net Interest Margin (%)",
        yaxis_title="Return on Assets (%)",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — Custom Explorer (Interactive)
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.header("Custom Bank Explorer")
    st.caption(
        "Build your own comparison: pick any banks from the FDIC dataset and "
        "choose the metrics you want to compare."
    )

    col_a, col_b = st.columns([2, 1])

    with col_a:
        # bank multi-select — default to peers
        all_banks = (
            fact_f.groupby("bank_name")["total_assets"]
            .max()
            .sort_values(ascending=False)
            .reset_index()
        )
        top_banks = all_banks.head(200)["bank_name"].tolist()

        selected_banks = st.multiselect(
            "Select banks (up to 10)",
            options=top_banks,
            default=[b for b in PEERS if b in top_banks],
            max_selections=10,
        )

    with col_b:
        explorer_metric = st.selectbox(
            "Metric",
            options=list(METRIC_LABELS.keys()),
            format_func=lambda k: METRIC_LABELS[k],
            index=0,  # total_assets
            key="explorer_metric",
        )

    if selected_banks:
        explorer_data = (
            fact_f[fact_f["bank_name"].isin(selected_banks)]
            .sort_values("date_key")
        )

        fig_exp = px.line(
            explorer_data,
            x="year_quarter",
            y=explorer_metric,
            color="bank_name",
            markers=True,
            title=f"{METRIC_LABELS[explorer_metric]} — Custom Comparison",
        )
        fig_exp.update_layout(
            height=450, legend_title="Bank",
            margin=dict(l=0, r=0, t=50, b=0),
            yaxis_title=METRIC_LABELS[explorer_metric],
            xaxis_title="Quarter",
        )
        st.plotly_chart(fig_exp, use_container_width=True)

        # data table
        with st.expander("View raw data"):
            display_cols = [
                "bank_name", "year_quarter", explorer_metric,
                "total_assets", "net_income", "return_on_assets",
            ]
            st.dataframe(
                explorer_data[display_cols].reset_index(drop=True),
                use_container_width=True,
            )
    else:
        st.info("Select at least one bank above to begin.")

    st.divider()

    # ── FDIC industry benchmark ───────────────────────────────────────────────
    st.subheader("FDIC Industry Benchmarks (All Banks, Quarterly Median)")

    industry_agg = (
        fact_f
        .groupby("year_quarter")[[
            "return_on_assets", "return_on_equity",
            "net_interest_margin", "loans_to_deposits_ratio",
        ]]
        .median()
        .reset_index()
        .sort_values("year_quarter")
    )

    bench_metric = st.selectbox(
        "Benchmark metric",
        ["return_on_assets", "return_on_equity", "net_interest_margin", "loans_to_deposits_ratio"],
        format_func=lambda k: METRIC_LABELS[k],
        key="bench_metric",
    )

    fig_bench = go.Figure()
    fig_bench.add_trace(go.Scatter(
        x=industry_agg["year_quarter"],
        y=industry_agg[bench_metric],
        name="FDIC Industry Median",
        mode="lines+markers",
        line=dict(color="#888888", width=2, dash="dash"),
    ))

    # overlay axos
    axos_bench = axos_f[["year_quarter", bench_metric]].sort_values("year_quarter")
    fig_bench.add_trace(go.Scatter(
        x=axos_bench["year_quarter"],
        y=axos_bench[bench_metric],
        name="Axos Bank",
        mode="lines+markers",
        line=dict(color="#003DA5", width=3),
    ))

    fig_bench.update_layout(
        height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=50, b=0),
        yaxis_title=METRIC_LABELS[bench_metric],
        xaxis_title="Quarter",
        title=f"Axos vs. FDIC Industry Median — {METRIC_LABELS[bench_metric]}",
    )
    st.plotly_chart(fig_bench, use_container_width=True)
    st.caption("Industry median computed across all 5,000+ FDIC-insured banks in the dataset.")
