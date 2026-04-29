with staging as (
    select * from {{ ref('stg_fdic_financials') }}
),

dim_bank as (
    select * from {{ ref('dim_bank') }}
),

dim_date as (
    select * from {{ ref('dim_date') }}
),

fact as (
    select
        -- surrogate key
        {{ dbt_utils.generate_surrogate_key(['s.bank_id', 's.report_date_str']) }} as fact_id,

        -- foreign keys
        s.bank_id,
        s.report_date_str                       as date_key,

        -- bank attributes (denormalized for dashboard convenience)
        s.bank_name,
        d.year_quarter,
        d.report_year,
        d.report_quarter,
        b.is_axos,
        b.peer_group_name,

        -- balance sheet ($thousands)
        s.total_assets,
        s.total_deposits,
        s.net_loans,
        s.total_equity,
        s.total_securities,

        -- income statement ($thousands)
        s.net_income,
        s.interest_income,
        s.noninterest_income,
        s.noninterest_expense,

        -- derived metrics
        s.interest_income + s.noninterest_income    as total_revenue,
        s.net_income / nullif(s.total_assets, 0) * 100  as roa_calc,

        -- ratios from FDIC (pre-calculated)
        s.net_interest_margin,
        s.return_on_assets,
        s.return_on_equity,
        s.loans_to_deposits_ratio,

        -- metadata
        s._loaded_at

    from staging s
    left join dim_bank b on s.bank_id = b.bank_id
    left join dim_date d on s.report_date_str = d.date_key
)

select * from fact
