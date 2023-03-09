SELECT
id as unique_id,
first_name,
last_name,
first_merge_employment::json->>'job_title' as title, -- get first employment array
work_email as primary_email,
personal_email as alternative_email,
--ssn,
(TO_DATE(replace(hire_date, '"',''), 'YYYY-MM-DD'))::varchar as dob,
remote_id as payroll_id,
employee_number,
first_merge_employment::json->>'employment_type' as employee_type,
case when first_merge_employment::json->>'employment_type' = 'FULL_TIME' then '100%' else null end as employee_fte,
employment_status,
null as overrides, -- These are non-standard and should be applied customer by customer
null as custom_fields, -- These are non-standard and should be applied customer by customer
(TO_DATE(replace(hire_date, '"',''), 'YYYY-MM-DD'))::varchar hire_date,
CASE 
    WHEN (termination_date is not null) and (termination_date != 'null')
    THEN (TO_DATE(replace(termination_date, '"',''), 'YYYY-MM-DD'))::varchar
    ELSE null
END AS termination_date,
home_location::json->>'street_1' as home_address_street,
home_location::json->>'street_2' as home_address_street_line_2,
home_location::json->>'state' as home_address_state,
home_location::json->>'city' as home_address_city,
home_location::json->>'country' as home_address_country,
mobile_phone_number as main_phone,
work_location::json->>'street_1' as office_address_street,
work_location::json->>'street_2' as office_address_street_line_2,
work_location::json->>'state' as office_address_state,
work_location::json->>'city' as office_address_city,
COALESCE(work_location::json->>'country', 'US') as office_address_country,
COALESCE(first_merge_employment::json->>'pay_frequency', 'TWICE_MONTHLY') as pay_frequency
FROM {{ df_1 }},
LATERAL(
    SELECT
        employments::json->0 as first_merge_employment
)fme,
LATERAL(
    SELECT employments ob
)obj

