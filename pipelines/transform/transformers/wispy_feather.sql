SELECT
id as unique_id,
first_name,
last_name,
first_merge_employment::json->>'job_title' as title, -- get first employment array
work_email as primary_email,
personal_email as alternative_email,
ssn,
date_of_birth as dob,
remote_id as payroll_id,
employee_number,
first_merge_employment::json->>'employment_type' as employee_type,
null as overrides, -- These are non-standard and should be applied customer by customer
null as custom_fields, -- These are non-standard and should be applied customer by customer
hire_date,
TO_DATE((hire_date::varchar),'YYYY-MM-DD') c,
termination_date,
home_location::json->>'street_1' as home_address_street,
home_location::json->>'street_2' as home_address_street_line_2,
home_location::json->>'state' as home_address_state,
home_location::json->>'city' as home_address_city,
home_location::json->>'country' as home_address_country,
mobile_phone_number as main_phone,
-- office_address_street,
-- office_address_street_line_2,
-- office_address_city,
-- office_address_state,
-- office_address_postal_code,
'US' as office_address_country,
COALESCE(first_merge_employment::json->>'pay_frequency', 'TWICE_MONTHLY') as pay_frequency
FROM {{ df_1 }},
LATERAL(
    SELECT
        employments::json->0 as first_merge_employment
)fme

