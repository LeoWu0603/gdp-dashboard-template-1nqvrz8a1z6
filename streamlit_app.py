import streamlit as st
import pandas as pd
import pyodbc

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# Set up the connection string
server = st.secrets["mssql_account"]["server"]
database = st.secrets["mssql_account"]["database"]
username = st.secrets["mssql_account"]["username"]
password = st.secrets["mssql_account"]["password"]
driver = 'ODBC Driver 17 for SQL Server'

# Function to fetch data from the database
def fetch_data():
    # Establish connection
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.v_Predictive_patientunique")
    rows = cursor.fetchall()
    df = pd.DataFrame([tuple(row) for row in rows], columns=[col[0] for col in cursor.description])
    cursor.close()
    conn.close()
    return df
    
# Streamlit app
st.title('Predictive Patient Data')

# Fetch and display data
df = fetch_data()
st.dataframe(df)

# Optionally display the first few rows
st.write("Preview of the data:")
st.write(df.head())
