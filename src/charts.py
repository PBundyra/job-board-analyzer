import altair as alt
from psql_query import run_query, COUNT_BY_LOC, COUNT_BY_TECH, COUNT_BY_EXP, AVG_BY_LOC, AVG_BY_EXP, AVG_BY_TECH, \
    MED_BY_TECH
import pandas as pd
import streamlit as st


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


@st.experimental_memo
def top_langs_chart() -> alt.Chart:
    df = run_query(COUNT_BY_TECH).head(10)
    return get_chart(df, title="Demand for employees depending on technology", axis_x_title="Number of offers")


@st.experimental_memo
def top_loc_chart() -> alt.Chart:
    df = run_query(COUNT_BY_LOC).head(10)
    return get_chart(df, title="Demand for employees depending on localization", axis_x_title="Number of offers")


@st.experimental_memo
def top_exp_lvl() -> alt.Chart:
    df = run_query(COUNT_BY_EXP)
    return get_chart(df, title="Demand for employees depending on experience", axis_x_title="Number of offers")


@st.experimental_memo
def avg_sal_by_loc() -> alt.Chart:
    df = run_query(AVG_BY_LOC).head(10)
    return get_chart(df, title="Average offered salary by localization", axis_x_title="Average salary")


@st.experimental_memo
def avg_sal_by_tech():
    df = run_query(AVG_BY_TECH).head(10)
    return get_chart(df, title="Average offered salary by technology", axis_x_title="Average salary")

@st.experimental_memo
def avg_sal_by_exp() -> alt.Chart:
    df = run_query(AVG_BY_EXP)
    return get_chart(df, title="Average offered salary by experience", axis_x_title="Average salary")

@st.experimental_memo
def med_sal_by_tech() -> alt.Chart:
    df = run_query(MED_BY_TECH).head(10)
    return get_chart(df, title="Median offered salary by technology", axis_x_title="Median salary")


# def pie_chart():
#     df = run_query(AVG_BY_EXP)
#     l = [{'name': dicti['name'], 'value': dicti['count']} for dicti in df.to_dict('records')]
#
#     option = {
#         "toolpit": {
#             "trigger": "item",
#         },
#         "legend": {"top": "bottom"},
#         # "toolbox": {
#         #     "show": False,
#         #     "feature": {
#         #         "mark": {"show": False},
#         #         "dataView": {"show": False, "readOnly": False},
#         #         "restore": {"show": False},
#         #         "saveAsImage": {"show": False},
#         #     },
#         # },
#         "series": [
#             {
#                 "name": "Demand for employees depending on experience",
#                 "type": "pie",
#                 "radius": [15, 130],
#                 "center": ["50%", "50%"],
#                 "roseType": "area",
#                 "itemStyle": {"borderRadius": 5},
#                 "label": {
#                     "show": False
#                 },
#                 "emphasis": {
#                     "label": {
#                         "show": False
#                     }
#                 },
#                 "data": l,
#             }
#         ],
#         "color": ['#9f3632', '#c16840', '#eabe83', '#edd3ab', '#eedbbd']
#     }
#     return st_echarts(
#         options=option, height="300px",
#     )
