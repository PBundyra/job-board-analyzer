#!/usr/bin/python
import streamlit as st
import charts
from streamlit import session_state as stat
import config
import psql_query
import matplotlib.pyplot as plt
import heatmaps as hm

EXP_LIST = ['Trainee', 'Junior', 'Mid', 'Senior', 'Expert']


def init_state() -> None:
    if 'conn' not in stat:
        stat.conn = config.init_connection()
    if 'dem_exp' not in stat:
        stat.dem_exp = charts.dem_exp()
    if 'dem_loc' not in stat:
        stat.dem_loc = charts.dem_loc(10)
    if 'dem_tech' not in stat:
        stat.dem_tech = charts.dem_tech(10)
    if 'dem_cat' not in stat:
        stat.dem_cat = charts.dem_cat(10)
    if 'avg_exp' not in stat:
        stat.avg_exp = charts.avg_sal_by_exp()
    if 'avg_loc' not in stat:
        stat.avg_loc = charts.avg_sal_by_loc(10)
    if 'avg_tech' not in stat:
        stat.avg_tech = charts.avg_sal_by_tech(10)
    if 'avg_cat' not in stat:
        stat.avg_cat = charts.avg_sal_by_cat(10)
    if 'med_tech' not in stat:
        stat.med_tech = charts.med_sal_by_tech(10)
    if 'med_cat' not in stat:
        stat.med_cat = charts.med_sal_by_cat(10)
    if 'med_loc' not in stat:
        stat.med_loc = charts.med_sal_by_loc(10)
    if 'med_exp' not in stat:
        stat.med_exp = charts.med_sal_by_exp()
    if 'med_metric' not in stat:
        stat.med_metric = psql_query.get_med_salary()
    if 'avg_metric' not in stat:
        stat.avg_metric = psql_query.get_avg_salary()
    if 'cnt_metric' not in stat:
        stat.cnt_metric = psql_query.get_offer_cnt()
    if 'def_but_res' not in stat:
        stat.def_but_res = True
    if 'but_list' not in stat:
        stat.but_list = [False] * 10
    if 'bar_but_res' not in stat:
        stat.bar_but_res = False
    if 'selected_tech' not in stat:
        stat.selected_tech = None
    if 'selected_loc' not in stat:
        stat.selected_loc = None
    if 'selected_cat' not in stat:
        stat.selected_cat = None
    if 'selected_exp' not in stat:
        stat.selected_exp = None
    if 'cat_or_tech' not in stat:
        stat.cat_or_tech = ""


def metrics() -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Number of offers", stat.cnt_metric)
    col2.metric("Average salary [PLN]", stat.avg_metric)
    col3.metric("Median of salary [PLN]", stat.med_metric)


def init_config() -> None:
    st.set_page_config(layout="wide", page_title="Job Boards Analyzer", initial_sidebar_state="collapsed",
                       page_icon=":ramen:")
    init_state()


def funfact() -> None:
    st.subheader("Did you know that?")
    sel1 = st.slider(label="Top [%]", min_value=1, max_value=100, value=25)
    sel2 = st.select_slider(label="of highest salaries for", options=EXP_LIST,
                            value='Senior')
    df = psql_query.top_med_by_exp(100 - sel1).values
    medians = [{el[0]: el[1]} for el in df]
    medians = {k: v for d in medians for k, v in d.items()}
    st.write(f"equals {round(medians[sel2])}")
    plt.figure()


def greetings() -> None:
    st.subheader("We would like to greet our professor at the University of Warsaw - prof. Murlak")
    st.write("P.S. If you are prof. Murlak please click button the below")
    ball = st.button("Hi prof. Murlak")
    if ball:
        st.balloons()


def side_bar() -> None:
    form = st.sidebar.form(key="Filtry")
    stat.selected_loc = form.multiselect(label="Localization",
                                         options=psql_query.get_loc_list())
    stat.selected_exp = form.multiselect(label="Experience",
                                         options=EXP_LIST)
    stat.cat_or_tech = form.radio(label="Choose to filter by category or technology", options=["Category", "Technology"])

    stat.selected_cat = form.multiselect(label="Category", options=psql_query.get_cat_list())
    stat.selected_tech = form.multiselect(label="Technology", options=psql_query.get_tech_list())
    stat.bar_but_res = form.form_submit_button(label='Show me my dear data')

    if stat.bar_but_res and not any([stat.selected_tech, stat.selected_loc, stat.selected_cat, stat.selected_exp]):
        form.error("Please select at least one option")
        stat.bar_but_res = False
    if (stat.cat_or_tech == "Category" and stat.selected_tech) or (
            stat.cat_or_tech == "Technology" and stat.selected_cat):
        form.error("Please select choose category or technology and fill the right bar")


def statistics_page() -> None:
    df = psql_query.get_query_with_params(loc=stat.selected_loc, exp=stat.selected_exp,
                                          tech=stat.selected_tech, cat=stat.selected_cat)
    if df.empty:
        st.warning("No offers have been found.")
    else:
        df.columns = ["City", "Category/Technology", "Experience", "Average", "Median", "Demand"]
        if not stat.selected_exp:
            df = df.loc[:, df.columns != 'Experience']
        if not stat.selected_cat and not stat.selected_tech:
            df = df.loc[:, df.columns != 'Category/Technology']
        if not stat.selected_loc:
            df = df.loc[:, df.columns != 'City']
        st.write(df)
        hm.get_heatmap(df)


def default_charts() -> None:
    loc1, loc2 = st.columns(2)
    loc_but1, loc_but2 = st.columns(2)
    cat1, cat2 = st.columns(2)
    cat_but1, cat_but2 = st.columns(2)
    tech1, tech2 = st.columns(2)
    tech_but1, tech_but2 = st.columns(2)
    exp1, exp2 = st.columns(2)
    dem1, dem2, dem3 = st.columns(3)
    dem_but1, dem_but2, dem_but3 = st.columns(3)

    loc1.altair_chart(stat.med_loc, use_container_width=True)
    loc2.altair_chart(stat.avg_loc, use_container_width=True)
    stat.but_list[0] = loc_but1.button("See more details about medians", 2137)
    stat.but_list[1] = loc_but2.button("See more details about averages", 2138)

    cat1.altair_chart(stat.med_cat, use_container_width=True)
    cat2.altair_chart(stat.avg_cat, use_container_width=True)
    stat.but_list[2] = cat_but1.button("See more details about medians", 2139)
    stat.but_list[3] = cat_but2.button("See more details about averages", 2140)

    tech1.altair_chart(stat.med_tech, use_container_width=True)
    tech2.altair_chart(stat.avg_tech, use_container_width=True)
    stat.but_list[4] = tech_but1.button("See more details about medians", 2141)
    stat.but_list[5] = tech_but2.button("See more details about averages", 2142)

    exp1.altair_chart(stat.med_exp, use_container_width=True)
    exp2.altair_chart(stat.avg_exp, use_container_width=True)

    dem1.altair_chart(stat.dem_tech, use_container_width=True)
    dem2.altair_chart(stat.dem_loc, use_container_width=True)
    dem3.altair_chart(stat.dem_cat, use_container_width=True)
    stat.but_list[6] = dem_but1.button("See more details about demand", 2143)
    stat.but_list[7] = dem_but2.button("See more details about demand", 2144)
    stat.but_list[8] = dem_but3.button("See more details about demand", 2145)


def home_page() -> None:
    BUT_DICT = {"loc_but1_res": charts.med_sal_by_loc, "loc_but2_res": charts.avg_sal_by_loc,
                "cat_but1_res": charts.med_sal_by_cat, "cat_but2_res": charts.avg_sal_by_cat,
                "tech_but1_res": charts.med_sal_by_tech, "tech_but2_res": charts.avg_sal_by_tech,
                "med_but1_res": charts.dem_tech, "med_but2_res": charts.dem_loc,
                "med_but3_res": charts.dem_cat}
    BUT_LIST = ["loc_but1_res", "loc_but2_res",
                "cat_but1_res", "cat_but2_res",
                "tech_but1_res", "tech_but2_res",
                "med_but1_res", "med_but2_res", "med_but3_res"]

    if stat.def_but_res and all(not but_res for but_res in stat.but_list):
        st.subheader("Well... basically why should you become a DevOps.")
        metrics()
        default_charts()
        funfact()
        greetings()
    else:
        for i in range(len(stat.but_list)):
            if stat.but_list[i]:
                stat.but_list[i] = False
                get_back = st.button("Home")
                if get_back:
                    stat.def_but_res = True
                st.altair_chart(BUT_DICT[BUT_LIST[i]](-1), use_container_width=True)
