import altair as alt
import query


def get_chart(df, title):
    chart = alt.Chart(
        df,
        title=title
    ) \
        .mark_bar() \
        .encode(
        x=alt.X("count",
                title="Number of offers"),
        y=alt.Y("name",
                sort=alt.EncodingSortField(field="count", order="descending"),
                title=""),
        tooltip=["name", "count"],
        color=alt.Color("count", scale=alt.Scale(scheme='browns'))
    )
    return chart


def top_langs_chart():
    df = query.lang_query().head(15)
    chart = get_chart(df, title="Demand for employees depending on technology")
    return chart


def top_loc_chart():
    df = query.loc_query().head(10)
    chart = get_chart(df, title="Demand for employees depending on localization")
    return chart


def top_exp_lvl():
    df = query.exp_lvl_query()
    chart = get_chart(df, title="Demand for employees depending on experience level")
    return chart
