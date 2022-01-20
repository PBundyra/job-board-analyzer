import psycopg2
import pandas as pd
from config import config


def loc_query(loc):
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        # cur.execute(f"SELECT AVG(salary_from), AVG(salary_to) from job_employment_type WHERE offer_id IN (SELECT offer_id FROM job_location WHERE city='Warszawa');")
        cur.execute(
            f"SELECT experience_level from job_experience_level group by experience_level;")
        # f"-- SELECT category, count(*) from job_category group by category having count (*) >= 10 order by category;")
        # display the PostgreSQL database server version
        fetched_data = cur.fetchall()
        df = pd.DataFrame(fetched_data)
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return df


def lang_query():
    df = pd.DataFrame(['1'])
    return df


def exp_lvl_query():
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(f"SELECT experience_level FROM job_experience_level GROUP BY experience_level;")
        # create DataFrame from fetched data
        fetched_data = cur.fetchall()
        df = pd.DataFrame(fetched_data, columns=['name', 'count'])
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return df
