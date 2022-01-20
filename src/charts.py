import altair as alt
from psql_query import query, COUNT_BY_LOC, COUNT_BY_TECH, COUNT_BY_EXP, avg_sal_by_tech_query
import default_data
import pandas as pd


def get_chart(df, title):
    axis_x = df.columns[1]
    axis_y = df.columns[0]
    chart = alt.Chart(
        df,
        title=title
    ) \
        .mark_bar() \
        .encode(
        x=alt.X(axis_x,
                title="Number of offers"),
        y=alt.Y(axis_y,
                sort=alt.EncodingSortField(field=axis_x, order="descending"),
                title=""),
        tooltip=[axis_y, axis_x],
        color=alt.Color(axis_x, scale=alt.Scale(scheme='browns'))
    )
    return chart


def top_langs_chart():
    df = query(COUNT_BY_TECH).head(15)
    df.columns = ["name", "count"]
    chart = get_chart(df, title="Demand for employees depending on technology")
    return chart


def top_loc_chart():
    df = query(COUNT_BY_LOC).head(10)
    df.columns = ["name", "count"]
    chart = get_chart(df, title="Demand for employees depending on technology")
    return chart


def top_exp_lvl():
    df = query(COUNT_BY_EXP)
    df.columns = ["name", "count"]
    chart = get_chart(df, title="Demand for employees depending on technology")
    return chart


def avg_sal_by_loc():
    df = query(COUNT_BY_LOC)
    df.columns = ["name", "count"]
    chart = get_chart(df, title="Average offered salary by localization")
    return chart


def avg_sal_by_tech_chart():
    l = [[tech, query(avg_sal_by_tech_query(tech))[0][0]] for tech in default_data.default_langs]
    df = pd.DataFrame(l, columns=["name", "avg salary"])
    chart = get_chart(df, title="Average offered salary by technology")
    return chart


# def avg_sal_by_exp():
#     l = [avg_sal_by_tech(tech) for tech in default_data.query_langs]
#     df = pd.DataFrame(l, columns=["name", "avg salary"])
#     chart = get_chart(df, title="Average offered salary by experience")
#     return chart
