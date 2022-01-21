#!/usr/bin/python
import streamlit as st
import psql_query
import charts
from streamlit import session_state as stat
import config
import psql_query

EXP_LIST = ['Expert', 'Junior', 'Mid', 'Senior', 'Trainee']

def filters() -> st.form:
    form = st.sidebar.form(key="Filtry")
    languages = psql_query.get_tech_list()
    langs = form.multiselect(label="Languages",
                             options=psql_query.get_tech_list())
    loc = form.multiselect(label="Localization",
                           options=psql_query.get_loc_list())
    experience = form.multiselect(label="Experience",
                                  options=EXP_LIST)
    submit_button = form.form_submit_button(label='Show me my dear data')
    return form


def init_state() -> None:
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
    if 'med_loc' not in stat:
        stat.med_loc = charts.med_sal_by_loc()
    if 'med_exp' not in stat:
        stat.med_exp = charts.med_sal_by_exp()
    if 'med_metric' not in stat:
        stat.med_metric = psql_query.get_med_salary()
    if 'avg_metric' not in stat:
        stat.avg_metric = psql_query.get_avg_salary()
    if 'cnt_metric' not in stat:
        stat.cnt_metric = psql_query.get_offer_cnt()


def metrics() -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Number of offers", stat.cnt_metric)
    col2.metric("Average salary [PLN]", stat.avg_metric)
    col3.metric("Median of salary [PLN]", stat.med_metric)


def init_config() -> None:
    st.set_page_config(layout="wide", page_title="Placeholder na chadowy tytuł", initial_sidebar_state="collapsed",
                       page_icon=":ramen:")
    st.title("Placeholder na chadowy tytuł")
    st.write("Placeholder na opis który ma tak dużo essy że ledwo daję radę.")
