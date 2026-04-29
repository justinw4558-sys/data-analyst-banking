with banks as (
    select
        bank_id,
        -- take the most recent name in case it changed over time
        last_value(bank_name) over (
            partition by bank_id
            order by report_date_str
            rows between unbounded preceding and unbounded following
        )                       as bank_name,
        max(report_date_str) over (partition by bank_id)    as latest_report_date,
        max(total_assets)    over (partition by bank_id)    as peak_assets,
        min(report_year)     over (partition by bank_id)    as first_report_year,
        max(report_year)     over (partition by bank_id)    as last_report_year,
        count(*)             over (partition by bank_id)    as quarters_reported
    from {{ ref('stg_fdic_financials') }}
    qualify row_number() over (partition by bank_id order by report_date_str desc) = 1
),

-- flag Axos and peer banks for easy filtering in the dashboard
flagged as (
    select
        bank_id,
        bank_name,
        latest_report_date,
        peak_assets,
        first_report_year,
        last_report_year,
        quarters_reported,
        case bank_id
            when 35546 then true   -- Axos Bank cert number
            else false
        end                     as is_axos,
        case bank_id
            when 35546 then 'Axos Bank'
            when 57803 then 'Ally Bank'
            when 58177 then 'SoFi Bank'
            when 32551 then 'LendingClub Bank'
            else null
        end                     as peer_group_name
    from banks
)

select * from flagged
