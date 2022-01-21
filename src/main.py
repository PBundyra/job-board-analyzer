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

# def filters() -> st.form:
#
#     return form


if __name__ == '__main__':
    content.init_config()

    form = st.sidebar.form(key="Filtry")
    languages = psql_query.get_tech_list()
    langs = form.multiselect(label="Languages",
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
#         # my_bar = st.progress(0)
        content.init_state()
        content.metrics()
        # sbar = content.filters()
        exp1, exp2 = st.columns(2)
        loc1, loc2 = st.columns(2)
        tech1, tech2 = st.columns(2)
        med1, med2, med3 = st.columns(3)

        exp1.altair_chart(stat.top_exp, use_container_width=True)
        exp2.altair_chart(stat.avg_exp, use_container_width=True)
        loc1.altair_chart(stat.top_loc, use_container_width=True)
        loc2.altair_chart(stat.avg_loc, use_container_width=True)
        # my_bar.progress(90)
        tech1.altair_chart(stat.top_tech, use_container_width=True)
        tech2.altair_chart(stat.avg_tech, use_container_width=True)
        med1.altair_chart(stat.med_tech, use_container_width=True)
        med2.altair_chart(stat.med_loc, use_container_width=True)
        med3.altair_chart(stat.med_exp, use_container_width=True)
        # my_bar.progress(95)
        # st.altair_chart(stat.med_tech, use_container_width=True)

        # exp2.element(charts.pie_chart())

        st.write(charts.pie_chart())
        # my_bar.progress(100)
    st.balloons()
