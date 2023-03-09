SELECT
TO_DATE('2023-01-03T00:00:00Z', 'YYYY-MM-DD') a,
-- TO_DATE(hire_date::varchar, 'YYYY-MM-DD') b,
TO_DATE((hire_date::varchar),'YYYY-MM-DD') c
from {{df_1}}
