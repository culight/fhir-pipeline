with raw_claims as (
    select *
    from {{ source('fhir_r4', 'fhir_resources') }}
),
claims_staged as (
    select
        resource_id as id,
        resource_type,
        raw_data:billablePeriod.start as billable_period_start,
        raw_data:billablePeriod.end as billable_period_end
    from raw_claims
    where resource_type = 'Claim'
)

select *
from claims_staged
