#!/usr/bin/python
import streamlit as st
from streamlit import session_state as stat
import content

if __name__ == '__main__':
    content.init_config()
    st.title("Job Boards Analyzer")
    content.side_bar()

    if stat.bar_but_res:
        get_back = st.button("Home")
        if get_back:
            stat.bar_but_res = False
        content.statistics_page()
    else:
        content.home_page()
