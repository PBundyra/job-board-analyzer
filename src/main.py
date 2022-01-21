#!/usr/bin/python
import pandas as pd
import streamlit as st
import psql_query
import charts
import altair as alt
from streamlit import session_state as stat
import config
from streamlit_echarts import st_echarts
import content


if __name__ == '__main__':
    content.init_config()
    # st.balloons()
    # st.experimental_memo.clear()


    form = st.sidebar.form(key="Filtry")
    languages = psql_query.get_tech_list()
    langs = form.multiselect(label="Technology",
                             options=psql_query.get_tech_list())
    loc = form.multiselect(label="Localization",
                           options=psql_query.get_loc_list())
    experience = form.multiselect(label="Experience",
                                  options=content.EXP_LIST)
    submit_button = form.form_submit_button(label='Show me my dear data')
    default_button = form.form_submit_button(label='Show me defaults')

    if submit_button:
        st.write("Essa")
    else:
        content.default_state()

    st.subheader("We would like to greet our professor at the University of Warsaw - prof. Murlak")
    st.write("P.S. If you are prof. Murlak please click button the below")
    ball = st.button("Hi prof. Murlak")
    if ball:
        st.balloons()
