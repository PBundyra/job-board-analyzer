-- NO OFFERS BY TECH
SELECT category, count(*)
from job_category
group by category;

-- NO OFFERS BY LOC
SELECT city, count(*)
FROM job_location
GROUP BY city
ORDER BY count(*) DESC;

-- AVG BY LOC
SELECT jl.city, (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
FROM job_employment_type jet
         FULL JOIN job_location jl ON jet.offer_id = jl.offer_id
GROUP BY jl.city, jet.salary_currency
HAVING count(salary_to) > 3
   AND jet.salary_currency = 'PLN'
   AND jl.city IS NOT NULL
ORDER BY (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2 DESC;

-- AVG BY EXP
SELECT jel.experience_level,
       (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
FROM job_employment_type jet
         FULL JOIN job_experience_level jel ON jet.offer_id = jel.offer_id
WHERE salary_currency = 'PLN'
GROUP BY jel.experience_level, jet.salary_currency
ORDER BY (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2 DESC;

-- AVG BY TECH
SELECT jc.category,
       (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
FROM job_employment_type jet
         FULL JOIN job_category jc on jet.offer_id = jc.offer_id
WHERE salary_currency = 'PLN'
GROUP BY jc.category, jet.salary_currency
HAVING count(category) > 3
ORDER BY (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2 DESC;

-- MEDIAN SALARY BY TECH
WITH salaries(cat, salary) AS (SELECT jc.category, (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                          FROM job_employment_type jet
                                FULL JOIN job_category jc on jet.offer_id = jc.offer_id
                          WHERE salary_currency = 'PLN')
SELECT cat, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)
FROM salaries
GROUP BY cat
HAVING count(cat) > 3;

-- COUNT OFFERS
SELECT count(*) from job_offer;

-- AVG SALARY
SELECT        (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
FROM job_employment_type jet
WHERE salary_currency = 'PLN';

-- MED BY LOC
WITH salaries(loc, salary) AS (SELECT jl.city,
                                      (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                               FROM job_employment_type jet
                                        FULL JOIN job_location jl ON jet.offer_id = jl.offer_id
                               WHERE salary_currency = 'PLN')
SELECT loc, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median
FROM salaries
GROUP BY loc
HAVING count(loc) > 3
ORDER BY median desc;