with dates as (
    select distinct
        report_date_str,
        report_year,
        report_month,
        report_quarter
    from {{ ref('stg_fdic_financials') }}
),

enriched as (
    select
        report_date_str                                     as date_key,
        report_year,
        report_quarter,
        report_month,
        concat(report_year, '-Q', report_quarter)           as year_quarter,
        case report_quarter
            when 1 then 'Q1 (Jan-Mar)'
            when 2 then 'Q2 (Apr-Jun)'
            when 3 then 'Q3 (Jul-Sep)'
            when 4 then 'Q4 (Oct-Dec)'
        end                                                 as quarter_label,
        case
            when report_year = year(current_date()) then true
            else false
        end                                                 as is_current_year
    from dates
)

select * from enriched
order by date_key
