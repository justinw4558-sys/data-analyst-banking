with source as (
    select * from {{ source('raw', 'fdic_financials') }}
),

-- deduplicate: keep one row per (bank, quarter) in case of reload duplicates
deduped as (
    select *
    from source
    qualify row_number() over (
        partition by cert, repdte
        order by _loaded_at desc
    ) = 1
),

renamed as (
    select
        -- identifiers
        cert                                    as bank_id,
        name                                    as bank_name,
        repdte                                  as report_date_str,

        -- date parts derived from YYYYMMDD string
        left(repdte, 4)::int                    as report_year,
        right(left(repdte, 6), 2)::int          as report_month,
        case right(left(repdte, 6), 2)::int
            when 3  then 1
            when 6  then 2
            when 9  then 3
            when 12 then 4
        end                                     as report_quarter,

        -- balance sheet ($thousands)
        asset                                   as total_assets,
        dep                                     as total_deposits,
        lnlsnet                                 as net_loans,
        eqtot                                   as total_equity,
        eq                                      as equity,
        sc                                      as total_securities,

        -- income statement ($thousands)
        netinc                                  as net_income,
        intinc                                  as interest_income,
        nonii                                   as noninterest_income,
        nonix                                   as noninterest_expense,

        -- ratios (%)
        nimy                                    as net_interest_margin,
        roa                                     as return_on_assets,
        roe                                     as return_on_equity,
        lnlsdepr                                as loans_to_deposits_ratio,

        -- metadata
        _loaded_at

    from deduped
    where
        repdte is not null
        and cert is not null
        and asset > 0
)

select * from renamed
