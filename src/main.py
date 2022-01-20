#!/usr/bin/python
import pandas as pd
import streamlit as st
import psycopg2
import query
import altair as alt
import charts
import default_data

if __name__ == '__main__':
    df = query.loc_query('Warszawa')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)
    l = list(map(lambda x: x[0], df.values.tolist()))
    print(l)
    # print(df.values.tolist())



    st.altair_chart(chart, use_container_width=True)

