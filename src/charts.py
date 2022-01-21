import altair as alt
from psql_query import run_query, COUNT_BY_LOC, COUNT_BY_TECH, COUNT_BY_EXP, AVG_BY_LOC, AVG_BY_EXP
import default_data
import pandas as pd


def get_chart(df: pd.DataFrame, title: str, axis_x_title: str) -> alt.Chart:
    axis_x = df.columns[1]
    axis_y = df.columns[0]
    chart = alt.Chart(
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
    return chart


def top_langs_chart() -> alt.Chart:
    df = run_query(COUNT_BY_TECH).head(15)
    # df.columns = pd.core.index.base.Index
    # df.rename(columns={"name": "name", "count": "count"})
    # df.columns = ["name", "count"]
    chart = get_chart(df, title="Demand for employees depending on technology", axis_x_title="Number of offers")
    return chart


def top_loc_chart() -> alt.Chart:
    df = run_query(COUNT_BY_LOC).head(10)
    # df.rename(columns={0: "name", 1: "count"})
    # df.columns = ["name", "count"]
    chart = get_chart(df, title="Demand for employees depending on technology", axis_x_title="Number of offers")
    return chart


def top_exp_lvl() -> alt.Chart:
    df = run_query(COUNT_BY_EXP)
    # df.rename(columns={0: "name", 1: "count"})
    # df.columns = ["name", "count"]
    chart = get_chart(df, title="Demand for employees depending on technology", axis_x_title="Number of offers")
    return chart


def avg_sal_by_loc() -> alt.Chart:
    df = run_query(AVG_BY_LOC).head(10)
    # df.rename(columns={0: "name", 1: "average salary"})
    # df.rename(columns={"name": "name", "count": "average"})
    chart = get_chart(df, title="Average offered salary by localization", axis_x_title="Average salary")
    return chart


# def avg_sal_by_tech_chart():
#     l = [[tech, run_query(avg_sal_by_tech_query(tech))[0][0]] for tech in default_data.default_langs]
#     df = pd.DataFrame(l, columns=["name", "avg salary"])
#     chart = get_chart(df, title="Average offered salary by technology")
#     return chart
#
#
def avg_sal_by_exp() -> alt.Chart:
    df = run_query(AVG_BY_EXP)
    # df.rename(columns={0: "name", 1: "average salary"})
    # df.rename(columns={"name": "name", "count": "average"})
    # print(df)
    # df.columns = ["name", "average"]
    chart = get_chart(df, title="Average offered salary by experience", axis_x_title="Average salary")
    return chart
