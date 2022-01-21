#!/usr/bin/python
import pandas as pd
import streamlit as st
import psql_query
import charts
import altair as alt
from streamlit import session_state as stat
import config


def filters():
    form = st.sidebar.form(key="Filtry")
    languages = sorted(['Python', 'Java', 'C++', 'C', 'Scala', 'Assembler', 'CSS', 'HTML', 'RUST'])
    langs = form.multiselect(label="Languages",
                           options=languages)
    widelki = form.slider(label="Salary",
                        min_value=3000,
                        max_value=4000,
                        step=10,
                        value=(3250, 3750))
    loc = form.multiselect(label="Localization",
                         options=['Warsaw', 'Remote'])
    experience = form.multiselect(label="Experience",
                                options=['Giga Paz', 'Paz', 'Chad', 'Giga Chad'])
    submit_button = form.form_submit_button(label='Pokaz hajs')
    return form


if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="Placeholder na chadowy tytuł", initial_sidebar_state="collapsed", page_icon="random")
    st.title("Placeholder na chadowy tytuł")
    st.write("Placeholder na opis który ma tak dużo essy że ledwo daję radę.")
    sbar = filters()
    exp1, exp2 = st.columns(2)
    loc1, loc2 = st.columns(2)
    tech1, tech2 = st.columns(2)
    if 'conn' not in stat:
        stat.conn = config.init_connection()
    if 'top_exp' not in stat:
        stat.top_exp = charts.top_exp_lvl()
    if 'top_loc' not in stat:
        stat.top_loc = charts.top_loc_chart()
    if 'top_tech' not in stat:
        stat.top_tech = charts.top_langs_chart()
    if 'avg_exp' not in stat:
        stat.avg_exp = charts.avg_sal_by_exp()
    if 'avg_loc' not in stat:
        stat.avg_loc = charts.avg_sal_by_loc()
    if 'avg_tech' not in stat:
        stat.avg_tech = charts.avg_sal_by_tech()
    if 'med_tech' not in stat:
        stat.med_tech = charts.med_sal_by_tech()
    exp1.altair_chart(stat.top_exp, use_container_width=True)
    exp2.altair_chart(stat.avg_exp, use_container_width=True)
    loc1.altair_chart(stat.top_loc, use_container_width=True)
    loc2.altair_chart(stat.avg_loc, use_container_width=True)
    tech1.altair_chart(stat.top_tech, use_container_width=True)
    tech2.altair_chart(stat.avg_tech, use_container_width=True)
    st.altair_chart(stat.med_tech, use_container_width=True)

    # exp2.element(charts.pie_chart())
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")
