import streamlit as st
import pandas as pd
import numpy as np


st.title('URBANIZATION MEASUREMENT')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Loading data...Done!")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Bar graph')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
year = st.slider('year', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == year]

st.subheader('Map of all data at %s:00' % year)
st.map(filtered_data)



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
            chart = (alt.Chart(data).mark_area(opacity=0.3).encode(x="year:T",y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),color="Region:N",))
            st.altair_chart(chart, use_container_width=True)

