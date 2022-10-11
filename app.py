import streamlit as st

import streamlit_book as stb
import geemap
from pathlib import Path
#geemap.ee_initialize()


st.session_state["warned_about_save_answers"] = True


st.set_page_config(layout="wide", page_title="SatSchool", page_icon="🛰️")



hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Set multipage
current_path = Path(__file__).parent.absolute()

# Streamit book properties
stb.set_book_config(menu_title="Main Menu",
                    menu_icon="",
                    options=[
                            "Introduction",
                            "Land",
                            "Oceans",
                            "Ice",
                            "Quiz"
                            ],
                    paths=[
                        current_path / "apps/intro",
                        current_path / "apps/land",
                        current_path / "apps/oceans",
                        current_path / "apps/ice.py",
                        current_path / "apps/quiz.py",
                          ],
                    icons=[
                          "house",
                          "",
                          "",
                          "",
                          "",
                          "trophy"
                          ],
                    save_answers=True,
                    )
    
with st.sidebar:

    st.sidebar.title("About")
    st.sidebar.info(
        """
        🌐 https://eo-cdt.org
        
        ©️ 2022 SatSchool
    """
    )

    
    
#1

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)

st.title("Main Page")
st.sidebar.success("Select a page above.")

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Input a text here", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    st.session_state["my_input"] = my_input
    st.write("You have entered: ", my_input)





#2
import streamlit as st
import pandas as pd
import numpy as np


st.title('URBANIZATION MEASUREMENT')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#upload
@st.cache
def load_data(nrows):
            data = pd.read_csv(DATA_URL, nrows=nrows)
            lowercase = lambda x: str(x).lower()
            data.rename(lowercase, axis='columns', inplace=True)
            data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
            return data
#data details
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Loading data...Done!")

if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(data)
#graph    
st.subheader('Bar graph')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)
# Some number in the range 0-23
year = st.slider('year', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == year]

st.subheader('Map of all data at %s:00' % year)
st.map(filtered_data)
#part2
st.title('Map data')
st.title('try part 2')
@st.cache
def get_UN_data():
            AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
            df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
            return df.set_index("Region")

df = get_UN_data()
countries = st.multiselect("Choose countries", list(df.index), ["China", "United States of America"])
if not countries:
            st.error("Please select at least one country.")
else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(columns={"index": "year", "value": "Gross Agricultural Product ($B)"})
            chart = (alt.Chart(data).mark_area(opacity=0.3).encode(x="year:T",y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),color="Region:N"))
            st.altair_chart(chart, use_container_width=True)

            
