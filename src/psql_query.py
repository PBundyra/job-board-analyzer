import psycopg2
import pandas as pd
from config import init_connection
from streamlit import session_state as stat

pool = init_connection()


def run_query(query: str):
    df = pd.DataFrame
    conn = None
    try:
        # read connection parameters
        # params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = pool.getconn()
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(query)
        # display the PostgreSQL database server version
        fetched_data = cur.fetchall()
        df = pd.DataFrame(fetched_data, columns=["name", "count"]) \
            # close the communication with the PostgreSQL
        cur.close()
        pool.putconn(conn)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            pool.putconn(conn)
            print('Database connection closed.')
    return df


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
                                            FULL JOIN job_category jc on jet.offer_id = jc.offer_id
                                            WHERE salary_currency = 'PLN')
            SELECT cat, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median
            FROM salaries
            GROUP BY cat
            HAVING count(cat) > 3
            ORDER BY median desc;"""
