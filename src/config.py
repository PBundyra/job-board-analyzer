#!/usr/bin/python
import psycopg2
import streamlit as st
from streamlit import session_state as stat
import psycopg2.pool


# def config(filename='./database.ini', section='postgresql'):
#     # create a parser
#     parser = ConfigParser()
#     # read config file
#     parser.read(filename)
#
#     # get section, default to postgresql
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception('Section {0} not found in the {1} file'.format(section, filename))
#
#     return db


# @st.cache
def init_connection():
    return psycopg2.pool.ThreadedConnectionPool(1, 1, **st.secrets["postgres"])
