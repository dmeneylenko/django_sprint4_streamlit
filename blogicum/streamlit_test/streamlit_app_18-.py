import streamlit as st
from datetime import time, datetime
import pandas as pd
# import pandas_profiling
# from streamlit_pandas_profiling import st_profile_report
import numpy as np
import os

st.title('Theming with config.toml')
st.write('Hello world!')

st.header('st.button')

'''if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')'''

st.header('st.button api-reference')
st.button("Reset", type="primary")
if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")

if st.button("Aloha", type="tertiary"):
    st.write("Ciao")


st.header('st.slider')

# Example 1

st.subheader('Slider')

age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')

# Example 2

st.subheader('Range slider')

values = st.slider(
     'Select a range of values',
     0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)

# Example 3

st.subheader('Range time slider')

appointment = st.slider(
     "Schedule your appointment:",
     value=(time(11, 30), time(12, 45)))
st.write("You're scheduled for:", appointment)

# Example 4

st.subheader('Datetime slider')

start_time = st.slider(
     "When do you start?",
     value=datetime(2020, 1, 1, 9, 30),
     format="MM/DD/YY - hh:mm")
st.write("Start time:", start_time)

st.header('Line chart')
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.header('st.selectbox')
option = st.selectbox(
     'What is your favorite color?',
     ('Blue', 'Red', 'Green'))

st.write('Your favorite color is ', option)

st.header('st.multiselect')
options = st.multiselect(
     'What are your favorite colors',
     ['Green', 'Yellow', 'Red', 'Blue'],
     ['Yellow', 'Red'])

st.write('You selected:', options)

st.header('st.checkbox')
st.write('What would you like to order?')
icecream = st.checkbox('Ice cream')
coffee = st.checkbox('Coffee')
cola = st.checkbox('Cola')
if icecream:
    st.write("Great! Here's some more 🍦")
if coffee:
    st.write("Okay, here's some coffee ☕")
if cola:
    st.write("Here you go 🥤")

# test
'''st.header('`streamlit_pandas_profiling`')
df = pd.read_csv(
    'https://storage.googleapis.com/tf-datasets/titanic/train.csv'
    )
pr = df.profile_report()
st_profile_report(pr)'''

st.header('st.latex')

st.latex(r'''
     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
     \sum_{k=0}^{n-1} ar^k =
     a \left(\frac{1-r^{n}}{1-r}\right)
     ''')


st.title('Customizing the theme of Streamlit apps')
st.write('Contents of the `.streamlit/config.toml` file of this app')
st.code("""
[theme]
primaryColor="#F39C12"
backgroundColor="#2E86C1"
secondaryBackgroundColor="#AED6F1"
textColor="#FFFFFF"
font="monospace"
""")
number = st.sidebar.slider('Select a number:', 0, 10, 5)
st.write('Selected number from slider widget is:', number)

st.title('st.secrets')
st.write(
    "Has environment variables been set:",
    os.environ["db_username"] == st.secrets["db_username"],
)
st.write(st.secrets['db_username'])

st.title('st.file_uploader')

st.subheader('Input CSV')
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader('DataFrame')
    st.write(df)
    st.subheader('Descriptive Statistics')
    st.write(df.describe())
else:
    st.info('☝️ Upload a CSV file')

'''
st.header('Разметка')

st.set_page_config(layout="wide")

st.title('How to layout your Streamlit app')

with st.expander('About this app'):
    st.write('This app shows the various ways on how you can layout your Streamlit app.')
    st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)

st.sidebar.header('Input')
user_name = st.sidebar.text_input('What is your name?')
user_emoji = st.sidebar.selectbox('Choose an emoji', ['', '😄', '😆', '😊', '😍', '😴', '😕', '😱'])
user_food = st.sidebar.selectbox('What is your favorite food?', ['', 'Tom Yum Kung', 'Burrito', 'Lasagna', 'Hamburger', 'Pizza'])

st.header('Output')

col1, col2, col3 = st.columns(3)

with col1:
    if user_name != '':
        st.write(f'👋 Hello {user_name}!')
    else:
        st.write('👈  Please enter your **name**!')

with col2:
    if user_emoji != '':
        st.write(f'{user_emoji} is your favorite **emoji**!')
    else:
        st.write('👈 Please choose an **emoji**!')

with col3:
    if user_food != '':
        st.write(f'🍴 **{user_food}** is your favorite **food**!')
    else:
        st.write('👈 Please choose your favorite **food**!')
'''