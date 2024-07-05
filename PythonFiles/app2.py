import streamlit as st
from PIL import Image
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder

def preprocess_data(df):
    # Remove 'INR' from Bus_fare and convert to float
    df['Bus_fare'] = df['Bus_fare'].str.replace('INR', '', regex=True).astype(float)

    # Remove 'Seats available' from Seats and convert to float
    df['Seats'] = df['Seats'].str.replace('Seats available', '', regex=True).replace('Seat available', '', regex=True).astype(float)
    
    # Drop the 'Unnamed: 0' column if it exists
    df.drop(columns=['Unnamed: 0'], errors='ignore', inplace=True)
    
    # Handle missing values
    df = df.fillna({
        'Bus_fare': df['Bus_fare'].mean(),
        'Seats': df['Seats'].mean(),
        'Hours': 0,
        'Minutes': 0,
        'Total_Hours': 0,
        'Total_Minutes': 0,
        'Ratings' : df['Ratings'].mean(),
        'Starting_point':'Not mentioned'
    })
    
    

    # Define a function to clean and convert the duration format
    def clean_duration(duration):
        if '-' in duration:
            parts = re.findall(r'(\d+)-?(\d+)?h', duration)
            hours = sum(int(part[1]) for part in parts)
            minutes = int(re.search(r'(\d+)-?(\d+)?m', duration).group(2))
        else:
            hours = int(re.search(r'(\d+)h', duration).group(1))
            minutes = int(re.search(r'(\d+)m', duration).group(1))
        return hours, minutes

    # Apply the clean_duration function to the Duration column
    df[['Hours', 'Minutes']] = df['Duration'].apply(lambda x: pd.Series(clean_duration(x)))

    # Calculate the total time in minutes
    df['Total_Hours'] = df['Hours'] + df['Minutes'] // 60
    df['Total_Minutes'] = df['Total_Hours'] * 60 + df['Minutes'] % 60

    # Label encode the bus types
    label_encoder = LabelEncoder()
    df['Bus_type_encoded'] = label_encoder.fit_transform(df['Bus_types'])
    df['Starting_point_encoded'] = label_encoder.fit_transform(df['Starting_point'])
    

    return df


im = Image.open("redbus lead.png")
st.set_page_config(
    page_title='Query',
    page_icon=im,
    layout="wide",
)
st.title('Red Bus Insights')
st.image(im)

def query_(n):
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Ta9ta6me@27",
        database = "redbus",
        autocommit = True)
    mycursor = mydb.cursor()
    if n==1:
        sql = ''' SELECT Names, Bus_fare, Seats FROM redbus.Kerala_buses
where Bus_types = "A/C Sleeper (2+1)" and Starting_point = "Majestic" '''
                
        mycursor.execute(sql)
        result = mycursor.fetchall()
        df = pd.DataFrame(result, columns=["Bus Name", "Bus_fare", " Available seats"])
        st.table(df)
    elif n==2:
        sql = '''SELECT Names, Bus_fare, Seats, Duration FROM redbus.Kerala_buses
where Bus_fare = (select max(Bus_fare) from redbus.Kerala_buses)'''
        mycursor.execute(sql)
        result = mycursor.fetchall()
        df = pd.DataFrame(result, columns=["Names", "Bus_fare","Seats","Duration"])
        st.table(df)     
    elif n==3:
        sql = ''' select Bus_fare, Ratings from redbus.WBTC_buses''' 
        mycursor.execute(sql)
        result = mycursor.fetchall()
        
        df = pd.DataFrame(result, columns=["Bus_fare","Ratings"])
        #df.set_index("Bus_fare",inplace=True)
        plt.figure(figsize=(10, 6))
        plt.scatter(df['Bus_fare'], df['Ratings'])
        plt.title('Scatter Plot of Bus Fare vs Ratings')
        plt.xlabel('Bus_fare')
        plt.ylabel('Ratings')
        st.pyplot(plt) 
        #st.table(df)
    elif n==4:
        sql = '''select Names, Bus_fare, Seats from redbus.UPSRTC_buses
where Starting_time > "00:00" '''  
        mycursor.execute(sql)
        result = mycursor.fetchall()
        df = pd.DataFrame(result, columns=["Names","Bus_fare","Seats" ])
        st.table(df)   
    elif n==5:
        sql = '''select names,Duration from redbus.HRTC_buses
where Duration = (select max(Duration) from redbus.HRTC_buses)'''
        mycursor.execute(sql)
        result = mycursor.fetchall()
        df = pd.DataFrame(result, columns=["Names","Duration"])
        st.table(df) 

# Define a list of options for the drop-down menu
options_data = {
    "1. What is the available kerala's bus name and number of seats where the starting point is from 'Majestic' and a/c sleeper? ":1,
    "2. Which kerala bus is having the highest bus fare?":2,
    "3. Is there any correlation between bus fare and ratings ?":3,
    "4. Show me the list of upsrtc buses which is starting above 12.am?":4,
    "5. What is the longest duration by a HRTC bus and its name?":5,
}

# Create a drop-down menu using st.selectbox
selected_option = st.selectbox("Select any Question", list(options_data.keys()))
selected_id = options_data[selected_option]
query_(selected_id)










