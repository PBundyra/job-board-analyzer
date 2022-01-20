#!/usr/bin/python
import pandas as pd
import streamlit as st
import psql_query
import charts
import altair as alt


if __name__ == '__main__':
    # df = query.loc_query('Warszawa')
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(df)
    # l = list(map(lambda x: x[0], df.values.tolist()))
    # print(l)
    # print(df.values.tolist())
    # print(query.list_categories())
    st.altair_chart(charts.top_exp_lvl(), use_container_width=True)
    st.altair_chart(charts.top_loc_chart(), use_container_width=True)
    st.altair_chart(charts.top_langs_chart(), use_container_width=True)
    # st.altair_chart(charts.avg_sal_by_tech_chart(), use_container_width=True)
