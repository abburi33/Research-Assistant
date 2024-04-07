import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

# Set page configuration
st.set_page_config(page_title='Data Visualization')
st.header('Excel to Data Visualization')

### --- LOAD DATAFRAME
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

# Read main dataframe
df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:D',
                   header=3)

# Read dataframe for participants
df_participants = pd.read_excel(excel_file,
                                sheet_name=sheet_name,
                                usecols='F:G',
                                header=3)

# Drop NaN values from participants dataframe
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION
# Get unique values for department and age
department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

# Slider for age selection
age_selection = st.slider('Age:',
                          min_value=min(ages),
                          max_value=max(ages),
                          value=(min(ages), max(ages)))

# Multiselect for department selection
department_selection = st.multiselect('Department:',
                                      department,
                                      default=department)

# --- FILTER DATAFRAME BASED ON SELECTION
# Create a mask based on selection
mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
# Group dataframe by rating and count votes
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
# Plot bar chart using Plotly Express
bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence=['#F63366'] * len(df_grouped),
                   template='plotly_white')
st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
# Display image and dataframe side by side
col1, col2 = st.columns(2)
image = Image.open('images/survey.jpg')
col1.image(image,
           use_column_width=True)
col2.dataframe(df[mask])

# --- PLOT PIE CHART
# Plot pie chart for total number of participants
pie_chart = px.pie(df_participants,
                    title='Total No. of Participants',
                    values='Participants',
                    names='Departments')
st.plotly_chart(pie_chart)
