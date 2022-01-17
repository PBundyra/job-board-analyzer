#!/usr/bin/python
import psycopg2
import pandas as pd
import streamlit as st
import altair as alt

from urllib.error import URLError
from config import config


def connect():
    """ Connect to the PostgreSQL database server """
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
        # print('PostgreSQL database version:')
        cur.execute('SELECT * from scraped_item;')

        # display the PostgreSQL database server version
        fetched_data = cur.fetchall()
        df = pd.DataFrame(fetched_data, columns=['ID', 'URL', 'WEBSITE', 'IDK', 'PROPERTIES', 'DATETIME', 'STH'])

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return df


if __name__ == '__main__':
    df = connect()
    print(df)