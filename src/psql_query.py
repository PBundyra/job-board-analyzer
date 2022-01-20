import psycopg2
import pandas as pd
from config import config



def query(query):
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
        cur.execute(query)
        # display the PostgreSQL database server version
        fetched_data = cur.fetchall()
        df = pd.DataFrame(fetched_data, columns=["name", "count"]) \
            # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
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