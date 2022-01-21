#!/usr/bin/python
import pandas as pd
import streamlit as st
import psql_query
import charts
import altair as alt


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
    st.set_page_config(layout="wide")
    sbar = filters()
    exp1, exp2 = st.columns(2)
    loc1, loc2 = st.columns(2)
    tech1, tech2 = st.columns(2)
    exp1.altair_chart(charts.top_exp_lvl(), use_container_width=True)
    exp2.altair_chart(charts.avg_sal_by_exp(), use_container_width=True)
    # exp2.element(charts.pie_chart())
    loc1.altair_chart(charts.top_loc_chart(), use_container_width=True)
    loc2.altair_chart(charts.avg_sal_by_loc(), use_container_width=True)
    tech1.altair_chart(charts.top_langs_chart(), use_container_width=True)
    tech2.altair_chart(charts.avg_sal_by_tech(), use_container_width=True)
    st.altair_chart(charts.med_sal_by_tech(), use_container_width=True)
