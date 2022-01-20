SELECT AVG(salary_from), AVG(salary_to)
from job_employment_type
WHERE offer_id IN (SELECT offer_id FROM job_location WHERE city = 'Warszawa');

SELECT city
from job_location
group by city
order by city;

SELECT experience_level
FROM job_experience_level
group by experience_level
order by experience_level;

SELECT *
from job_employment_type
order by offer_id;

SELECT category, count(*)
from job_category
group by category;

SELECT max(employment_type), count(*)
from job_employment_type
group by employment_type
order by employment_type;


SELECT city, count(*)
FROM job_location
GROUP BY city
ORDER BY count(*) DESC;

SELECT (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
FROM job_employment_type
WHERE offer_id IN (SELECT offer_id FROM job_category WHERE category = 'java');