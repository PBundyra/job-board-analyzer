import pandas as pd
import streamlit as st
from plotly.express import imshow
import charts
from streamlit import session_state as stat


def heatmap_with_all_params(df: pd.DataFrame):
    cities = df['City']
    exps = df['Experience']
    techs = df['Category/Technology']

    for exp in exps.unique():

        for city in cities.unique():
            for tech in techs.unique():
                if not ((df['City'] == city) & (df['Category/Technology'] == tech) & (df['Experience'] == exp)).any():
                    df.loc[len(df.index)] = [city, tech, exp, 0, 0, 0]

        medians = [list(df[(df['City'] == City) & (df['Experience'] == exp)]['Median']) for City in
                   df['City'].unique()]

        averages = [list(df[(df['City'] == City) & (df['Experience'] == exp)]['Average']) for City in
                    df['City'].unique()]

        demands = [list(df[(df['City'] == City) & (df['Experience'] == exp)]['Demand']) for City in
                   df['City'].unique()]

        fig = imshow(medians, title=f"Medians for {exp}", y=cities.unique(), x=techs.unique(),
                     labels=dict(x="Technology", y="City", color="[PLN]"), color_continuous_scale="Oranges")
        st.plotly_chart(fig)

        fig = imshow(averages, title=f"Averages for {exp}", y=cities.unique(), x=techs.unique(),
                     labels=dict(x="Technology", y="City", color="[PLN]"), color_continuous_scale="Oranges")
        st.plotly_chart(fig)

        fig = imshow(demands, title=f"Demands for {exp}", y=cities.unique(), x=techs.unique(),
                     labels=dict(x="Technology", y="City", color=""), color_continuous_scale="Oranges")
        st.plotly_chart(fig)


def heatmap_with_city_and_exp(df: pd.DataFrame) -> None:
    cities = df['City']
    exps = df['Experience']

    for city in cities.unique():
        for exp in exps.unique():
            if not ((df['City'] == city) & (df['Experience'] == exp)).any():
                df.loc[len(df.index)] = [city, exp, 0, 0, 0]

    medians = [list(df[df['City'] == City]['Median']) for City in
               df['City'].unique()]
    #
    averages = [list(df[df['City'] == City]['Average']) for City in
                df['City'].unique()]

    demands = [list(df[df['City'] == City]['Demand']) for City in
               df['City'].unique()]

    fig = imshow(medians, title="Medians", y=cities.unique(), x=exps.unique(),
                 labels=dict(x="Technology", y="City", color="[PLN]"), color_continuous_scale="Oranges")
    st.plotly_chart(fig)

    fig = imshow(averages, title="Averages", y=cities.unique(), x=exps.unique(),
                 labels=dict(x="Technology", y="City", color="[PLN]"), color_continuous_scale="Oranges")
    st.plotly_chart(fig)

    fig = imshow(demands, title="Demands", y=cities.unique(), x=exps.unique(),
                 labels=dict(x="Technology", y="City", color=""), color_continuous_scale="Oranges")
    st.plotly_chart(fig)


def heatmap_with_city_and_tech(df: pd.DataFrame) -> None:
    cities = df['City']
    techs = df['Category/Technology']

    for city in cities.unique():
        for tech in techs.unique():
            if not ((df['City'] == city) & (df['Category/Technology'] == tech)).any():
                df.loc[len(df.index)] = [city, tech, 0, 0, 0]

    medians = [list(df[df['City'] == City]['Median']) for City in
               df['City'].unique()]
    #
    averages = [list(df[df['City'] == City]['Average']) for City in
                df['City'].unique()]

    demands = [list(df[df['City'] == City]['Demand']) for City in
               df['City'].unique()]

    fig = imshow(medians, title="Medians", y=cities.unique(), x=techs.unique(),
                 labels=dict(x="Technology", y="City", color="[PLN]"), color_continuous_scale="Oranges")
    st.plotly_chart(fig)

    fig = imshow(averages, title="Averages", y=cities.unique(), x=techs.unique(),
                 labels=dict(x="Technology", y="City", color="[PLN]"), color_continuous_scale="Oranges")
    st.plotly_chart(fig)

    fig = imshow(demands, title="Demands", y=cities.unique(), x=techs.unique(),
                 labels=dict(x="Technology", y="City", color=""), color_continuous_scale="Oranges")
    st.plotly_chart(fig)


def heatmap_with_exp_and_tech(df: pd.DataFrame) -> None:
    techs = df['Category/Technology']
    exps = df['Experience']

    for exp in exps.unique():
        for tech in techs.unique():
            if not ((df['Experience'] == exp) & (df['Category/Technology'] == tech)).any():
                df.loc[len(df.index)] = [tech, exp, 0, 0, 0]

    medians = [list(df[df['Category/Technology'] == cat]['Median']) for cat in
               df['Category/Technology'].unique()]
    #
    averages = [list(df[df['Category/Technology'] == cat]['Average']) for cat in
                df['Category/Technology'].unique()]

    demands = [list(df[df['Category/Technology'] == cat]['Demand']) for cat in
               df['Category/Technology'].unique()]

    fig = imshow(medians, title="Medians", y=techs.unique(), x=exps.unique(),
                 labels=dict(x="Technology", y="Category/Technology", color="[PLN]"), color_continuous_scale="Oranges")
    st.plotly_chart(fig)

    fig = imshow(averages, title="Averages", y=techs.unique(), x=exps.unique(),
                 labels=dict(x="Technology", y="Category/Technology", color="[PLN]"), color_continuous_scale="Oranges")
    st.plotly_chart(fig)

    fig = imshow(demands, title="Demands", y=techs.unique(), x=exps.unique(),
                 labels=dict(x="Technology", y="Category/Technology", color=""), color_continuous_scale="Oranges")
    st.plotly_chart(fig)


def get_heatmap(df: pd.DataFrame) -> None:
    if 'City' in df.columns and 'Experience' in df.columns and 'Category/Technology' in df.columns:
        heatmap_with_all_params(df)
    elif 'City' in df.columns and 'Experience' in df.columns:
        heatmap_with_city_and_exp(df)
    elif 'City' in df.columns and 'Category/Technology' in df.columns:
        heatmap_with_city_and_tech(df)
    elif 'Experience' in df.columns and 'Category/Technology' in df.columns:
        heatmap_with_exp_and_tech(df)
    elif 'City' in df.columns:
        st.altair_chart(charts.med_sal_by_loc(-1), use_container_width=True)
        st.altair_chart(charts.avg_sal_by_loc(-1), use_container_width=True)
        st.altair_chart(charts.dem_loc(-1), use_container_width=True)
    elif 'Experience' in df.columns:
        st.altair_chart(charts.med_sal_by_exp(), use_container_width=True)
        st.altair_chart(charts.avg_sal_by_exp(), use_container_width=True)
        st.altair_chart(charts.dem_exp(), use_container_width=True)
    elif stat.cat_or_tech == 'Category':
        st.altair_chart(charts.med_sal_by_cat(-1), use_container_width=True)
        st.altair_chart(charts.avg_sal_by_cat(-1), use_container_width=True)
        st.altair_chart(charts.dem_cat(-1), use_container_width=True)
    else:
        st.altair_chart(charts.med_sal_by_tech(-1), use_container_width=True)
        st.altair_chart(charts.avg_sal_by_tech(-1), use_container_width=True)
        st.altair_chart(charts.dem_tech(-1), use_container_width=True)
