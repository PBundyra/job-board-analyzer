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
        x=alt.X(axis_x,
                title=axis_x_title),
        y=alt.Y(axis_y,
                sort=alt.EncodingSortField(field=axis_x, order="descending"),
                title=""),
        tooltip=[axis_y, axis_x],
        color=alt.Color(axis_x, scale=alt.Scale(scheme='browns'))
    )


# def get_group_chart(df: pd.DataFrame) -> alt.Chart:
#     return basic_query("XD")


@st.experimental_memo(ttl=600)
def top_cat(num_of_rows: int) -> alt.Chart:
    df = basic_query(COUNT_BY_CAT).head(num_of_rows)
    df.columns = ["name", "count"]
    return get_chart(df, title="Demand for employees depending on category", axis_x_title="Number of offers")


@st.experimental_memo(ttl=600)
def top_tech(num_of_rows: int) -> alt.Chart:
    df = basic_query(COUNT_BY_TECH).head(num_of_rows)
    df.columns = ["name", "count"]
    return get_chart(df, title="Demand for employees depending on technology", axis_x_title="Number of offers")


@st.experimental_memo(ttl=600)
def top_loc(num_of_rows: int) -> alt.Chart:
    df = basic_query(COUNT_BY_LOC).head(num_of_rows)
    df.columns = ["name", "count"]
    return get_chart(df, title="Demand for employees depending on localization", axis_x_title="Number of offers")


@st.experimental_memo(ttl=600)
def top_exp() -> alt.Chart:
    df = basic_query(COUNT_BY_EXP)
    df.columns = ["name", "count"]
    return get_chart(df, title="Demand for employees depending on experience", axis_x_title="Number of offers")


@st.experimental_memo(ttl=600)
def avg_sal_by_loc(num_of_rows: int) -> alt.Chart:
    df = basic_query(AVG_BY_LOC).head(num_of_rows)
    df.columns = ["name", "count"]
    return get_chart(df, title="Average offered salary by localization", axis_x_title="Average salary")


@st.experimental_memo(ttl=600)
def avg_sal_by_cat(num_of_rows: int) -> alt.Chart:
    df = basic_query(AVG_BY_CAT).head(num_of_rows)
    df.columns = ["name", "count"]
    return get_chart(df, title="Average offered salary by category", axis_x_title="Average salary")


@st.experimental_memo(ttl=600)
def avg_sal_by_tech(num_of_rows: int) -> alt.Chart:
    df = basic_query(AVG_BY_TECH).head(num_of_rows)
    df.columns = ["name", "count"]
    return get_chart(df, title="Average offered salary by technology", axis_x_title="Average salary")


@st.experimental_memo(ttl=600)
def avg_sal_by_exp() -> alt.Chart:
    df = basic_query(AVG_BY_EXP)
    df.columns = ["name", "count"]
    return get_chart(df, title="Average offered salary by experience", axis_x_title="Average salary")


@st.experimental_memo(ttl=600)
def med_sal_by_cat(num_of_rows: int) -> alt.Chart:
    df = basic_query(MED_BY_CAT).head(num_of_rows)
    df.columns = ["name", "count"]
    return get_chart(df, title="Median offered salary by category", axis_x_title="Median salary")


@st.experimental_memo(ttl=600)
def med_sal_by_tech(num_of_rows: int) -> alt.Chart:
    df = basic_query(MED_BY_TECH).head(num_of_rows)
    df.columns = ["name", "count"]
    return get_chart(df, title="Median offered salary by technology", axis_x_title="Median salary")


@st.experimental_memo(ttl=600)
def med_sal_by_loc(num_of_rows: int) -> alt.Chart:
    df = basic_query(MED_BY_LOC).head(num_of_rows)
    df.columns = ["name", "count"]
    return get_chart(df, title="Median offered salary by localization", axis_x_title="Median salary")


@st.experimental_memo(ttl=600)
def med_sal_by_exp() -> alt.Chart:
    df = basic_query(MED_BY_EXP)
    df.columns = ["name", "count"]
    return get_chart(df, title="Median offered salary by experience", axis_x_title="Median salary")


def pie_chart():
    df = basic_query(AVG_BY_EXP)
    df.columns = ["name", "count"]
    l = [{'name': dicti['name'], 'value': dicti['count']} for dicti in df.to_dict('records')]

    option = {
        "toolpit": {
            "trigger": "item",
        },
        "legend": {"top": "bottom"},
        # "toolbox": {
        #     "show": False,
        #     "feature": {
        #         "mark": {"show": False},
        #         "dataView": {"show": False, "readOnly": False},
        #         "restore": {"show": False},
        #         "saveAsImage": {"show": False},
        #     },
        # },
        "series": [
            {
                "name": "Demand for employees depending on experience",
                "type": "pie",
                "radius": [15, 130],
                "center": ["50%", "50%"],
                "roseType": "area",
                "itemStyle": {"borderRadius": 5},
                "label": {
                    "show": False
                },
                "emphasis": {
                    "label": {
                        "show": False
                    }
                },
                "data": l,
            }
        ],
        "color": ['#9f3632', '#c16840', '#eabe83', '#edd3ab', '#eedbbd']
    }
    return st_echarts(
        options=option, height="300px",
    )
