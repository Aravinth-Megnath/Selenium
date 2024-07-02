import streamlit as st
import pandas as pd 
import numpy as np
import seaborn as sns
import re

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


andhra_df = pd.read_csv('andhra.csv')

andhra_df = preprocess_data(andhra_df)


# Streamlit UI
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", pages)

# Home page content
if page == "Home":
    st.title("Home Page")
    st.write("This is the home page of the app. Navigate to the heatmap page to see the correlation heatmap.")

# Heatmap page content
elif page == "Heatmap":
    st.title("Heatmap Page")

    numerical_andhra_df = andhra_df.select_dtypes(include='number')
    corr_andhra_df = numerical_andhra_df.corr()

    # Plotting the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_andhra_df, cmap='RdYlGn', linewidths=0.30, annot=True)
    plt.title('Correlation between features')
    st.pyplot(plt)  # Use st.pyplot to display the heatmap in Streamlit