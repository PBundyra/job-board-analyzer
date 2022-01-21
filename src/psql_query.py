import psycopg2
import pandas as pd
from config import init_connection
from streamlit import session_state as stat
import streamlit as st

pool = init_connection()


def run_query(query: str):
    df = pd.DataFrame
    conn = None
    cur = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = pool.getconn()
        cur = conn.cursor()
        cur.execute(query)
        fetched_data = cur.fetchall()
        df = pd.DataFrame(fetched_data)
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    except Exception as error:
        print(error)
    finally:
        if cur is not None and not cur.closed:
            cur.close()
        if conn is not None:
            pool.putconn(conn)
            print('Database connection closed.')
    return df

@st.cache
def get_offer_cnt():
    return run_query(COUNT_OFFERS)[0][0]

@st.cache
def get_avg_salary():
    return run_query(AVG_SALARY)[0][0]


@st.cache
def get_med_salary():
    return run_query(MED_SALARY)[0][0]


@st.cache
def get_loc_list():
    return run_query(ALL_LOC)[0].tolist()


@st.cache
def get_tech_list():
    return run_query(ALL_TECH)[0].tolist()

COUNT_BY_TECH = """
            SELECT category, count(*)
            FROM job_category
            GROUP BY category
            ORDER BY count(*) DESC;"""

COUNT_BY_LOC = """
            SELECT city, count(*)
            FROM job_location
            GROUP BY city
            ORDER BY count(*) DESC;"""

COUNT_BY_EXP = """
            SELECT experience_level, count(*)
            FROM job_experience_level
            GROUP BY experience_level
            ORDER BY count(*);"""

AVG_BY_LOC = """
            SELECT jl.city, (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
            FROM job_employment_type jet
            FULL JOIN job_location jl ON jet.offer_id = jl.offer_id
            GROUP BY jl.city, jet.salary_currency
            HAVING count(salary_to) > 3 AND jet.salary_currency = 'PLN' AND jl.city IS NOT NULL
            ORDER BY (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2 DESC;"""

AVG_BY_EXP = """
            SELECT jel.experience_level, (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
            FROM job_employment_type jet
            FULL JOIN job_experience_level jel ON jet.offer_id = jel.offer_id
            WHERE salary_currency = 'PLN'
            GROUP BY jel.experience_level, jet.salary_currency
            ORDER BY (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2 DESC;"""

AVG_BY_TECH = """
            SELECT jc.category, (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
            FROM job_employment_type jet
            FULL JOIN job_category jc on jet.offer_id = jc.offer_id
            WHERE salary_currency = 'PLN'
            GROUP BY jc.category, jet.salary_currency
            HAVING count(category) > 3
            ORDER BY (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2 DESC;"""

MED_BY_TECH = """
            WITH salaries(cat, salary) AS (SELECT jc.category, (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                            FROM job_employment_type jet
                                            FULL JOIN job_category jc ON jet.offer_id = jc.offer_id
                                            WHERE salary_currency = 'PLN')
            SELECT cat, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median
            FROM salaries
            GROUP BY cat
            HAVING count(cat) > 3
            ORDER BY median DESC;"""

MED_BY_LOC = """
            WITH salaries(loc, salary) AS (SELECT jl.city,
                                                  (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                           FROM job_employment_type jet
                                                    FULL JOIN job_location jl ON jet.offer_id = jl.offer_id
                                           WHERE salary_currency = 'PLN')
            SELECT loc, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median
            FROM salaries
            GROUP BY loc
            HAVING count(loc) > 3
            ORDER BY median DESC;"""

MED_BY_EXP = """
            WITH salaries(exp, salary) AS (SELECT jel.experience_level,
                                                  (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                           FROM job_employment_type jet
                                                    FULL JOIN job_experience_level jel ON jet.offer_id = jel.offer_id
                                           WHERE salary_currency = 'PLN')
            SELECT exp, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median
            FROM salaries
            GROUP BY exp
            HAVING count(exp) > 3
            ORDER BY median desc;"""

COUNT_OFFERS = "SELECT count(*) FROM job_offer;"

AVG_SALARY = """
            SELECT(CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
            FROM job_employment_type jet
            WHERE salary_currency = 'PLN';
            """

MED_SALARY = """
            WITH salaries(salary) AS (SELECT (CAST(ROUND(salary_to) AS bigint) + CAST(ROUND(salary_from) AS bigint)) / 2
                                      FROM job_employment_type jet
                                      WHERE salary_currency = 'PLN')
            SELECT CAST(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS bigint) AS median
            FROM salaries;"""

ALL_LOC = """
            SELECT city
            FROM job_location
            GROUP BY city
            HAVING count(city) > 3
            ORDER BY city;"""

ALL_TECH = """
            SELECT category
            FROM job_category
            GROUP BY category
            HAVING count(category) > 3
            ORDER BY category;"""
