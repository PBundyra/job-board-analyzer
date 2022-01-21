#!/usr/bin/python
import psycopg2
import streamlit as st
import psycopg2.pool


def init_connection():
    return psycopg2.pool.SimpleConnectionPool(1, 1, **st.secrets["postgres"])
