import psycopg2
import pandas as pd
from config import config, init_connection


def run_query(query):
    conn = None
    df = pd.DataFrame
    try:
        # read connection parameters
        # params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = init_connection()
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(query)
        # display the PostgreSQL database server version
        fetched_data = cur.fetchall()
        df = pd.DataFrame(fetched_data) \
            # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
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


def avg_sal_by_tech_query(tech):
    return f"""
            SELECT (CAST(ROUND(AVG(salary_to)) AS bigint) + CAST(ROUND(AVG(salary_from)) AS bigint)) / 2
            FROM job_employment_type
            WHERE offer_id IN (SELECT offer_id FROM job_category WHERE category = '{tech}');
    """
