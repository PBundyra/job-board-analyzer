import altair as alt
from psql_query import basic_query, COUNT_BY_LOC, COUNT_BY_CAT, COUNT_BY_EXP, AVG_BY_LOC, AVG_BY_EXP, AVG_BY_CAT, \
    MED_BY_TECH, MED_BY_LOC, MED_BY_EXP, COUNT_BY_TECH, AVG_BY_TECH, MED_BY_CAT
import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts


def get_chart(df: pd.DataFrame, title: str, axis_x_title: str) -> alt.Chart:
    axis_x = df.columns[1]
    axis_y = df.columns[0]
    return alt.Chart(
        df,
        title=title
    ) \
        .mark_bar() \
        .encode(
        x=alt.X(axis_x, title=axis_x_title),
        y=alt.Y(axis_y,
                sort=alt.EncodingSortField(field=axis_x, order="descending"),
                title=" "),
        tooltip=[axis_y, axis_x],
        color=alt.Color(axis_x, scale=alt.Scale(scheme='browns'))
    )


@st.experimental_memo(ttl=600)
def dem_cat(num_of_rows: int) -> alt.Chart:
    df = basic_query(COUNT_BY_CAT).head(num_of_rows)
    df.columns = ["category", "Number of offers"]
    return get_chart(df, title="Demand for employees depending on category", axis_x_title="Number of offers")


@st.experimental_memo(ttl=600)
def dem_tech(num_of_rows: int) -> alt.Chart:
    df = basic_query(COUNT_BY_TECH).head(num_of_rows)
    df.columns = ["technology", "Number of offers"]
    return get_chart(df, title="Demand for employees depending on technology", axis_x_title="Number of offers")


@st.experimental_memo(ttl=600)
def dem_loc(num_of_rows: int) -> alt.Chart:
    df = basic_query(COUNT_BY_LOC).head(num_of_rows)
    df.columns = ["city", "Number of offers"]
    return get_chart(df, title="Demand for employees depending on localization", axis_x_title="Number of offers")


@st.experimental_memo(ttl=600)
def dem_exp() -> alt.Chart:
    df = basic_query(COUNT_BY_EXP)
    df.columns = ["experience level", "PLN"]
    return get_chart(df, title="Demand for employees depending on experience", axis_x_title="Number of offers")


@st.experimental_memo(ttl=600)
def avg_sal_by_loc(num_of_rows: int) -> alt.Chart:
    df = basic_query(AVG_BY_LOC).head(num_of_rows)
    df.columns = ["city", "PLN"]
    return get_chart(df, title="Average offered salary by localization", axis_x_title=" ")


@st.experimental_memo(ttl=600)
def avg_sal_by_cat(num_of_rows: int) -> alt.Chart:
    df = basic_query(AVG_BY_CAT).head(num_of_rows)
    df.columns = ["category", "PLN"]
    return get_chart(df, title="Average offered salary by category", axis_x_title=" ")


@st.experimental_memo(ttl=600)
def avg_sal_by_tech(num_of_rows: int) -> alt.Chart:
    df = basic_query(AVG_BY_TECH).head(num_of_rows)
    df.columns = ["technology", "PLN"]
    return get_chart(df, title="Average offered salary by technology", axis_x_title=" ")


@st.experimental_memo(ttl=600)
def avg_sal_by_exp() -> alt.Chart:
    df = basic_query(AVG_BY_EXP)
    df.columns = ["experience level", "PLN"]
    return get_chart(df, title="Average offered salary by experience", axis_x_title=" ")


@st.experimental_memo(ttl=600)
def med_sal_by_cat(num_of_rows: int) -> alt.Chart:
    df = basic_query(MED_BY_CAT).head(num_of_rows)
    df.columns = ["category", "PLN"]
    return get_chart(df, title="Median offered salary by category", axis_x_title=" ")


@st.experimental_memo(ttl=600)
def med_sal_by_tech(num_of_rows: int) -> alt.Chart:
    df = basic_query(MED_BY_TECH).head(num_of_rows)
    df.columns = ["technology", "PLN"]
    return get_chart(df, title="Median offered salary by technology", axis_x_title=" ")


@st.experimental_memo(ttl=600)
def med_sal_by_loc(num_of_rows: int) -> alt.Chart:
    df = basic_query(MED_BY_LOC).head(num_of_rows)
    df.columns = ["city", " "]
    return get_chart(df, title="Median offered salary by localization", axis_x_title=" ")


@st.experimental_memo(ttl=600)
def med_sal_by_exp() -> alt.Chart:
    df = basic_query(MED_BY_EXP)
    df.columns = ["experience level", "PLN"]
    return get_chart(df, title="Median offered salary by experience", axis_x_title=" ")
