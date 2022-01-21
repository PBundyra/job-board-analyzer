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
    content.init_state()
    content.metrics()
    sbar = content.filters()
    exp1, exp2 = st.columns(2)
    loc1, loc2 = st.columns(2)
    tech1, tech2 = st.columns(2)
    med1, med2, med3 = st.columns(3)

    exp1.altair_chart(stat.top_exp, use_container_width=True)
    exp2.altair_chart(stat.avg_exp, use_container_width=True)
    loc1.altair_chart(stat.top_loc, use_container_width=True)
    loc2.altair_chart(stat.avg_loc, use_container_width=True)
    tech1.altair_chart(stat.top_tech, use_container_width=True)
    tech2.altair_chart(stat.avg_tech, use_container_width=True)
    med1.altair_chart(stat.med_tech, use_container_width=True)
    med2.altair_chart(stat.med_loc, use_container_width=True)
    med3.altair_chart(stat.med_exp, use_container_width=True)
    # st.altair_chart(stat.med_tech, use_container_width=True)

    # exp2.element(charts.pie_chart())

    st.write(charts.pie_chart())
