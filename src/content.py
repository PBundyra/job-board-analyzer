#!/usr/bin/python
import streamlit as st
import charts
from streamlit import session_state as stat
import config
import psql_query

EXP_LIST = ['Trainee', 'Junior', 'Mid', 'Senior', 'Expert']


def init_state() -> None:
    if 'conn' not in stat:
        stat.conn = config.init_connection()
        # my_bar.progress(10)
    if 'top_exp' not in stat:
        stat.top_exp = charts.top_exp()
        # my_bar.progress(15)
    if 'top_loc' not in stat:
        stat.top_loc = charts.top_loc(10)
        # my_bar.progress(20)
    if 'top_tech' not in stat:
        stat.top_tech = charts.top_tech(10)
    if 'top_cat' not in stat:
        stat.top_cat = charts.top_cat(10)
        # my_bar.progress(25)
    if 'avg_exp' not in stat:
        stat.avg_exp = charts.avg_sal_by_exp()
        # my_bar.progress(30)
    if 'avg_loc' not in stat:
        stat.avg_loc = charts.avg_sal_by_loc(10)
        # my_bar.progress(40)
    if 'avg_tech' not in stat:
        stat.avg_tech = charts.avg_sal_by_tech(10)
    if 'avg_cat' not in stat:
        stat.avg_cat = charts.avg_sal_by_cat(10)
        # my_bar.progress(45)
    if 'med_tech' not in stat:
        stat.med_tech = charts.med_sal_by_tech(10)
    if 'med_cat' not in stat:
        stat.med_cat = charts.med_sal_by_cat(10)
        # my_bar.progress(50)
    if 'med_loc' not in stat:
        stat.med_loc = charts.med_sal_by_loc(10)
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
    if 'def_but_res' not in stat:
        stat.def_but_res = True
    if 'loc_but1_res' not in stat:
        stat.loc_but1_res = False
    if 'loc_but2_res' not in stat:
        stat.loc_but2_res = False
    if 'cat_but1_res' not in stat:
        stat.cat_but1_res = False
    if 'cat_but2_res' not in stat:
        stat.cat_but2_res = False
    if 'tech_but1_res' not in stat:
        stat.tech_but1_res = False
    if 'tech_but2_res' not in stat:
        stat.tech_but2_res = False
    if 'med_but1_res' not in stat:
        stat.med_but1_res = False
    if 'med_but2_res' not in stat:
        stat.med_but2_res = False
    if 'med_but3_res' not in stat:
        stat.med_but3_res = False
    if 'butt_list' not in stat:
        stat.butt_list = [False] * 10


def metrics() -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Number of offers", stat.cnt_metric)
    col2.metric("Average salary [PLN]", stat.avg_metric)
    col3.metric("Median of salary [PLN]", stat.med_metric)


def init_config() -> None:
    st.set_page_config(layout="wide", page_title="Placeholder na chadowy tytuł", initial_sidebar_state="collapsed",
                       page_icon=":ramen:")


def funfact() -> None:
    st.subheader("Did you know that?")
    sel1 = st.slider(label="Top [%]", min_value=1, max_value=100, value=25)
    sel2 = st.select_slider(label="of highest salaries for", options=EXP_LIST,
                            value='Senior')
    st.write("equals")
    df = psql_query.top_med_by_exp(100 - sel1).values
    medians = [{el[0]: el[1]} for el in df]
    medians = {k: v for d in medians for k, v in d.items()}
    st.metric(label="", value=round(medians[sel2]))


def greetings() -> None:
    st.subheader("We would like to greet our professor at the University of Warsaw - prof. Murlak")
    st.write("P.S. If you are prof. Murlak please click button the below")
    ball = st.button("Hi prof. Murlak")
    if ball:
        st.balloons()


def default_state() -> None:
    init_state()

    BUTT_DICT = {"loc_but1_res": charts.med_sal_by_loc, "loc_but2_res": charts.avg_sal_by_loc,
                 "cat_but1_res": charts.med_sal_by_cat, "cat_but2_res": charts.avg_sal_by_cat,
                 "tech_but1_re": charts.med_sal_by_tech, "tech_but2_res": charts.avg_sal_by_tech,
                 "med_but1_res": charts.top_tech, "med_but2_res": charts.top_loc,
                 "med_but3_res": charts.top_cat}
    BUTT_LIST = ["loc_but1_res", "loc_but2_res",
                 "cat_but1_res", "cat_but2_res",
                 "tech_but1_res", "tech_but2_res",
                 "med_but1_res", "med_but2_res", "stat.med_but3_res"]


    if stat.def_but_res and all(not butt_res for butt_res in stat.butt_list):
        st.title("Placeholder na chadowy tytuł")
        st.subheader("Well... basically why should you become a DevOps.")
        metrics()

        loc1, loc2 = st.columns(2)
        loc_but1, loc_but2 = st.columns(2)
        cat1, cat2 = st.columns(2)
        cat_but1, cat_but2 = st.columns(2)
        tech1, tech2 = st.columns(2)
        tech_but1, tech_but2 = st.columns(2)
        exp1, exp2 = st.columns(2)
        med1, med2, med3 = st.columns(3)
        med_but1, med_but2, med_but3 = st.columns(3)

        loc1.altair_chart(stat.med_loc, use_container_width=True)
        loc2.altair_chart(stat.avg_loc, use_container_width=True)
        stat.butt_list[0] = loc_but1.button("See more details about medians", 2137)
        stat.butt_list[1] = loc_but2.button("See more details about averages", 2138)
        # stat.loc_but2_res = loc_but2.button("See more details about averages", 2138)

        cat1.altair_chart(stat.med_cat, use_container_width=True)
        cat2.altair_chart(stat.avg_cat, use_container_width=True)
        stat.butt_list[2] = cat_but1.button("See more details about medians", 2139)
        stat.butt_list[3] = cat_but2.button("See more details about averages", 2140)

        tech1.altair_chart(stat.med_tech, use_container_width=True)
        tech2.altair_chart(stat.avg_tech, use_container_width=True)
        stat.butt_list[4] = tech_but1.button("See more details about medians", 2141)
        stat.butt_list[5] = tech_but2.button("See more details about averages", 2142)

        exp1.altair_chart(stat.med_exp, use_container_width=True)
        exp2.altair_chart(stat.avg_exp, use_container_width=True)

        med1.altair_chart(stat.top_tech, use_container_width=True)
        med2.altair_chart(stat.top_loc, use_container_width=True)
        med3.altair_chart(stat.top_cat, use_container_width=True)
        stat.butt_list[6] = med_but1.button("See more details about demand", 2143)
        stat.butt_list[7] = med_but2.button("See more details about demand", 2144)
        stat.butt_list[8] = med_but3.button("See more details about demand", 2145)

        funfact()
        greetings()

    else:
        for i in range(len(stat.butt_list)):
            if stat.butt_list[i]:
                stat.butt_list[i] = False
                get_back = st.button("Home")
                if get_back:
                    stat.def_but_res = True
                st.altair_chart(BUTT_DICT[BUTT_LIST[i]](-1), use_container_width=True)

