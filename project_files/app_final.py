import streamlit as st
from PIL import Image
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
#import plotly.express as px
import seaborn as sns
import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder




from streamlit_option_menu import option_menu
with st.sidebar:
    a = option_menu(
            menu_title="Main Menu",
            options=["Home","Select the Bus"],
            icons=["bi bi-android", "binoculars", "app-indicator", "person-video3"],
            menu_icon="cast",
            default_index=0,
        )

if a == 'Home':
    st.title('Red Bus Analysis and Insights')
    
    st.write(" We've analyzed Red Bus data to help you navigate your next journey. Explore trends, compare fares & amenities, and make informed travel decisions!")
    
    
if a == "Select the Bus":
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Ta9ta6me@27",
        database = "redbus",
        autocommit = True)
    mycursor = mydb.cursor()
    
    
    #st.write(final_result)
    c1,c2,c3= st.columns([5,3,2])
    c4,c5,c6 = st.columns([2,3,3])
    with c3:
        mycursor.execute("SELECT distinct(AC_Type) FROM redbus.andhra;")
        AC_result = mycursor.fetchall()
        bus_type_selected = [i[0] for i in AC_result]
        AC_Type = st.selectbox("Select the AC Type",bus_type_selected)
    with c6:
        mycursor.execute("SELECT distinct(Bus_fare_range) FROM redbus.andhra;")
        Fare_result = mycursor.fetchall()
        bus_fare_selected = [i[0] for i in Fare_result]
        bus_fare = st.selectbox("Bus Fare Range",bus_fare_selected)   
    with c4:
        mycursor.execute("select distinct(Ratings_range) from redbus.andhra;")
        Ratings_result = mycursor.fetchall()
        ratings_selected = [i[0] for i in Ratings_result]
        ratings = st.selectbox("Select the Ratings", ratings_selected)
    
    with c1:
        mycursor.execute("select distinct(Route) from redbus.andhra;")
        Route_result = mycursor.fetchall()
        starting_selected = [i[0] for i in Route_result]
        starting_place = st.selectbox("Select the Route", starting_selected)   
    
    with c2:
        mycursor.execute("select distinct(Seat_Type) from redbus.andhra;")
        Seat_result = mycursor.fetchall()
        Seat_selected = [i[0] for i in Seat_result]
        Seat_type = st.selectbox("Select the Seat Type", Seat_selected) 
     
    with c5:
        mycursor.execute("select distinct(Starting_time_interval) from redbus.andhra;")
        Starting_time_result = mycursor.fetchall()
        starting_time = [i[0] for i in Starting_time_result]
        starting_time_selected = st.selectbox("Starting time", starting_time) 
           
        
        
    mycursor.execute(f"SELECT *FROM redbus.andhra where AC_Type = '{AC_Type}'and Bus_fare_range = '{bus_fare}'and Ratings > '{ratings}'and Route='{starting_place}' and Seat_Type = '{Seat_type}' and Starting_time_interval = '{starting_time_selected}';")
    final_result = mycursor.fetchall()
    mycursor.execute("describe redbus.andhra")
    columns = mycursor.fetchall()
    final_columns = [i[0] for i in columns]
    df = pd.DataFrame(final_result,columns=final_columns)
    st.write(df)
        #st.table(result)
    # with c1:
    #     ratings = st.selectbox("Select the rating",andhra_df.Ratings.unique())
        
    # st.dataframe(andhra_df[andhra_df['Ratings']== bus_type])













