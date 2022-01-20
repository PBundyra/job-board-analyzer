import altair as alt
import query


def top_langs_chart():
    df = query.lang_query()
    chart = (
        alt.Chart(
            df,
            title="Languages popularity"
        )
            .mark_bar()
            .encode(
            x=alt.X("count",
                    title="Number of offers"),
            y=alt.Y("name",
                    sort=alt.EncodingSortField(field="count", order="descending"),
                    title=""),
            tooltip=["name", "count"],
            color=alt.Color("name")
        )
    )
    return chart


def top_loc_chart():
    df = query.lang_query()
    chart = (
        alt.Chart(
            df,
            title="Languages popularity"
        )
            .mark_bar()
            .encode(
            x=alt.X("count",
                    title="Number of offers"),
            y=alt.Y("name",
                    sort=alt.EncodingSortField(field="count", order="descending"),
                    title=""),
            tooltip=["name", "count"],
            color=alt.Color("name")
        )
    )
    return chart

def top_exp_lvl():
    df = query.lang_query()
    chart = (
        alt.Chart(
            df,
            title="Languages popularity"
        )
            .mark_bar()
            .encode(
            x=alt.X("count",
                    title="Number of offers"),
            y=alt.Y("name",
                    sort=alt.EncodingSortField(field="count", order="descending"),
                    title=""),
            tooltip=["name", "count"],
            color=alt.Color("name")
        )
    )
    return chart
