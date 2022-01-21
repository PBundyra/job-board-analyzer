#!/usr/bin/python
import streamlit as st
import charts
from streamlit import session_state as stat
import config
import psql_query

EXP_LIST = ['Expert', 'Junior', 'Mid', 'Senior', 'Trainee']


def init_state() -> None:
    if 'conn' not in stat:
        stat.conn = config.init_connection()
        # my_bar.progress(10)
    if 'top_exp' not in stat:
        stat.top_exp = charts.top_exp_lvl()
        # my_bar.progress(15)
    if 'top_loc' not in stat:
        stat.top_loc = charts.top_loc_chart()
        # my_bar.progress(20)
    if 'top_tech' not in stat:
        stat.top_tech = charts.top_langs_chart()
        # my_bar.progress(25)
    if 'avg_exp' not in stat:
        stat.avg_exp = charts.avg_sal_by_exp()
        # my_bar.progress(30)
    if 'avg_loc' not in stat:
        stat.avg_loc = charts.avg_sal_by_loc()
        # my_bar.progress(40)
    if 'avg_tech' not in stat:
        stat.avg_tech = charts.avg_sal_by_tech()
        # my_bar.progress(45)
    if 'med_tech' not in stat:
        stat.med_tech = charts.med_sal_by_tech()
        # my_bar.progress(50)
    if 'med_loc' not in stat:
        stat.med_loc = charts.med_sal_by_loc()
        # my_bar.progress(60)
    if 'med_exp' not in stat:
        stat.med_exp = charts.med_sal_by_exp()
        # my_bar.progress(65)
    if 'med_metric' not in stat:
        stat.med_metric = psql_query.get_med_salary()
        # my_bar.progress(70)
    if 'avg_metric' not in stat:
        stat.avg_metric = psql_query.get_avg_salary()
        # my_bar.progress(80)
    if 'cnt_metric' not in stat:
        stat.cnt_metric = psql_query.get_offer_cnt()
        # my_bar.progress(85)


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


def default_state() -> None:
    init_state()
    metrics()
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

    # st.write(charts.pie_chart())
    st.subheader("Did you know that?")
    sel1 = st.slider(label="Top [%]", min_value=1, max_value=100, value=25)
    sel2 = st.select_slider(label="of highest salaries for", options=['Trainee', 'Junior', 'Mid', 'Senior', 'Expert'], value='Senior')
    text3 = st.write("equals ")
    df = psql_query.top_med_by_exp(100 - sel1).values
    medians = [{el[0]: el[1]} for el in df]
    medians = {k: v for d in medians for k, v in d.items()}
    st.metric(label="", value=round(medians[sel2]))
