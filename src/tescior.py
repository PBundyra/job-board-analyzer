import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import numpy as np


class number:
    def __init__(self, val):
        self.num = val

    def get_val(self):
        return self.num

    def increment(self):
        self.num += 1


x = number(2137)

st.title('Turbo giga chad stronka na zaliczenie')

with st.form(key="Filtry"):
    languages = sorted(['Python', 'Java', 'C++', 'C', 'Scala', 'Assembler', 'CSS', 'HTML', 'RUST'])
    langs = st.multiselect(label="Languages",
                         options=languages)
    widelki = st.slider(label="Salary",
                        min_value=3000,
                        max_value=4000,
                        step=10,
                        value=(3250,3750))
    loc = st.multiselect(label="Localization",
                         options=['Warsaw', 'Remote'])
    experience = st.multiselect(label = "Experience",
                                options=['Giga Paz','Paz', 'Chad','Giga Chad'])
    submit_button = st.form_submit_button(label='Pokaz hajs')
if submit_button and widelki[0] <= 3500:
    st.info('Zartujesz sobie? Daj se wiecej')
elif submit_button and widelki[1] >= 3800:
    st.info('Hola hola, nie przesadzaj')
elif submit_button and loc == []:
    st.info('Please select at least one localization')
elif submit_button and langs == []:
    st.info('Please select at least one language')
elif submit_button and loc == []:
    st.info('Please select at least one localization')
elif submit_button:
    # Uderz do bazki
    st.write(f"Mordo klepiesz w {langs} i bedziesz zarabial {widelki} mieszkajac w {loc}")

slider = st.slider(label="ence pence",
                   min_value=69,
                   max_value=2137,
                   step=10,
                   value=420)

st.write(slider)

languages = sorted(['Python', 'Java', 'C++', 'C', 'Scala', 'Assembler', 'CSS', 'HTML', 'RUST'])

options_ex = np.array(languages)

bar = st.multiselect(label="Wpisz sobie filter jaki chcesz",
                     options=options_ex)

st.write(bar)

options = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
    ],
}
st_echarts(options=options)

from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts

b = (
    Bar()
        .add_xaxis(["Microsoft", "Amazon", "IBM", "Oracle", "Google", "Alibaba"])
        .add_yaxis(
        "2017-2018 Revenue in (billion $)", [21.2, 20.4, 10.3, 6.08, 4, 2.2]
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(
            title="Top cloud providers 2018", subtitle="2017-2018 Revenue"
        ),
        toolbox_opts=opts.ToolboxOpts(),
    )
)
st_pyecharts(b)
