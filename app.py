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
#im = Image.open("redbus lead.png")
# st.set_page_config(
#     page_title='Query',
#     page_icon=im,
#     layout="wide",
# )



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

from streamlit_option_menu import option_menu
with st.sidebar:
    a = option_menu(
            menu_title="Main Menu",
            options=["Home","Select the Bus", "Bus Popularity", "Occupancy and Popularity","Occupancy Rate",
                     'Starting Point Analysis', "Starting and Ending Times","Customer Preferences and Segmentation"],
            icons=["bi bi-android", "binoculars", "app-indicator", "person-video3"],
            menu_icon="cast",
            default_index=0,
        )

if a == 'Home':
    st.title('Red Bus Analysis and Insights')
    
    st.write(" We've analyzed Red Bus data to help you navigate your next journey. Explore trends, compare fares & amenities, and make informed travel decisions!")
    #st.image(im)
    
if a == "Select the Bus":
    # st.title('Correlation')
    # st.write('A slight positive correlation (0.073) exists between bus fare and the starting point. This suggests that some starting points may have slightly higher fares, potentially due to higher demand or more premium services starting from those points.')
    andhra_df = pd.read_csv(r'C:\Users\Hp\Selenium\andhra.csv')
    # andhra_df = preprocess_data(andhra_df)
    # numerical_andhra_df = andhra_df.select_dtypes(include='number')
    # corr_andhra_df = numerical_andhra_df.corr()
    # plot = sns.heatmap(corr_andhra_df, cmap='RdYlGn', linewidths=0.30, annot=True)
    # st.pyplot(plot.get_figure())
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
        result = mycursor.fetchall()
        bus_type_selected = [i[0] for i in result]
        AC_Type = st.selectbox("Select the AC Type",bus_type_selected)
    with c6:
        mycursor.execute("SELECT distinct(Bus_fare_range) FROM redbus.andhra;")
        result = mycursor.fetchall()
        bus_fare_selected = [i[0] for i in result]
        bus_fare = st.selectbox("Bus Fare Range",bus_fare_selected)   
    with c4:
        mycursor.execute("select distinct(Ratings_range) from redbus.andhra;")
        result = mycursor.fetchall()
        ratings_selected = [i[0] for i in result]
        ratings = st.selectbox("Select the Ratings", ratings_selected)
    
    with c1:
        mycursor.execute("select distinct(Route) from redbus.andhra;")
        result = mycursor.fetchall()
        starting_selected = [i[0] for i in result]
        starting_place = st.selectbox("Select the Route", starting_selected)   
    
    with c2:
        mycursor.execute("select distinct(Seat_Type) from redbus.andhra;")
        result = mycursor.fetchall()
        reaching_selected = [i[0] for i in result]
        reaching_place = st.selectbox("Select the Seat Type", reaching_selected) 
     
    with c5:
        mycursor.execute("select distinct(Starting_time_interval) from redbus.andhra;")
        result = mycursor.fetchall()
        starting_time = [i[0] for i in result]
        starting_time_selected = st.selectbox("Starting time", starting_time) 
           
        
        
mycursor.execute(f"SELECT *FROM redbus.andhra where AC_Type = '{AC_Type}'and Bus_fare_range = '{bus_fare}'and Ratings > '{ratings}'and Route='{starting_place}' and Seat_Type = '{reaching_place}' and Starting_time_interval = '{starting_time_selected}';")
result = mycursor.fetchall()
mycursor.execute("describe redbus.andhra")
columns = mycursor.fetchall()
final_columns = [i[0] for i in columns]
df = pd.DataFrame(result,columns=final_columns)
st.write(df)
        #st.table(result)
    # with c1:
    #     ratings = st.selectbox("Select the rating",andhra_df.Ratings.unique())
        
    # st.dataframe(andhra_df[andhra_df['Ratings']== bus_type])

if a == 'Bus Popularity':
    import re
    st.title("Bus Popularity")
    st.write("Looks like Volvo Multi Axle B11R AC Seater\Sleeper (2+1) and NON A/C Seater (2+3) buses are filling soon")

    # Define the function to categorize bus types
    def ac_non(bus_type):
        pattern = '^NON'
        if re.findall(pattern, bus_type):
            return 'Non A/C'
        else:
            return 'A/C'
        

    # Apply the function to the 'Bus_types' column
    andhra_df = pd.read_csv('andhra.csv')
    andhra_df = preprocess_data(andhra_df)
    andhra_df['AC_Type'] = andhra_df['Bus_types'].apply(ac_non)
    avg_seats_by_type = andhra_df.groupby(['Bus_types', 'AC_Type'])['Seats'].mean().reset_index()
    avg_seats_by_type.columns = ['Bus Type', 'AC Type', 'Average Remaining Seats']
    result_df = avg_seats_by_type.sort_values(by='Average Remaining Seats',ascending = True).head(5)
    st.table(result_df)


    # View the result
if a == 'Occupancy and Popularity':
    st.title('Occupancy and Popularity')
    st.write("The number of seats available can indicate the popularity of the bus route. For instance, if many seats are available close to departure time, the route might not be very popular. Conversely, few available seats indicate high demand.")
    andhra_df = pd.read_csv('andhra.csv')
    andhra_df = preprocess_data(andhra_df)

    import re

    # Define the function to categorize bus types
    def ac_non(bus_type):
        pattern = '^NON'
        if re.findall(pattern, bus_type):
            return 'Non A/C'
        else:
            return 'A/C'

    # Apply the function to the 'Bus_types' column
    andhra_df['AC_Type'] = andhra_df['Bus_types'].apply(ac_non)

    # View the result
    andhra_df.AC_Type.value_counts()
        # Convert departure_time to datetime if not already
    andhra_df['Starting_time'] = pd.to_datetime(andhra_df['Starting_time'])

    # Calculate the time remaining until departure
    current_time = pd.Timestamp('2024-06-21 20:00')

    andhra_df['time_until_departure'] = (andhra_df['Starting_time'] - current_time).dt.total_seconds() / 3600  # time until departure in hours

    # Analyze seats remaining close to departure (e.g., within 2 hours)
    seats_close_to_departure = andhra_df[andhra_df['time_until_departure'] < 2].groupby('AC_Type')['Seats'].mean().reset_index()
    seats_close_to_departure.columns = ['AC Type', 'Average Remaining Seats Close to Departure']

    # View the result
    st.table(seats_close_to_departure)
 

if a == 'Starting and Ending Times':
    st.title("Bus Departures and Arrivals by Hour")
    st.write('The starting and ending times can be analyzed to determine peak travel times. This can help in adjusting schedules to meet demand more effectively.')
    andhra_df = pd.read_csv('andhra.csv')
    andhra_df = preprocess_data(andhra_df)
        # Convert to datetime
    andhra_df['Starting_time'] = pd.to_datetime(andhra_df['Starting_time'], format='%H:%M')
    andhra_df['Ending_time'] = pd.to_datetime(andhra_df['Ending_time'], format='%H:%M')

    # Extract hours for starting and ending times
    andhra_df['Starting_hour'] = andhra_df['Starting_time'].dt.hour
    andhra_df['Ending_hour'] = andhra_df['Ending_time'].dt.hour

    # Count the number of departures and arrivals by hour
    starting_hour_counts = andhra_df['Starting_hour'].value_counts().sort_index()
    ending_hour_counts = andhra_df['Ending_hour'].value_counts().sort_index()

    
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    # Plot starting hours
    axes[0].bar(starting_hour_counts.index, starting_hour_counts.values)
    axes[0].set_title('Bus Departures by Hour')
    axes[0].set_xlabel('Hour of the Day')
    axes[0].set_ylabel('Number of Departures')
    
    # Plot ending hours
    axes[1].bar(ending_hour_counts.index, ending_hour_counts.values)
    axes[1].set_title('Bus Arrivals by Hour')
    axes[1].set_xlabel('Hour of the Day')
    axes[1].set_ylabel('Number of Arrivals')
    
    plt.tight_layout()
    st.pyplot(fig)

if a == 'Starting Point Analysis':
    st.title('Starting Point Analysis')
    st.write('The starting point (e.g., TIRUPATHI) can be analyzed to understand which locations are generating more traffic. This can inform decisions on where to focus marketing efforts or add more buses.')
    andhra_df = pd.read_csv('andhra.csv')
    andhra_df = preprocess_data(andhra_df)
        
    # Group by starting point and count the number of buses
    starting_point_counts = andhra_df['Starting_point'].value_counts().reset_index()
    starting_point_counts.columns = ['Starting Point', 'Number of Buses']

    # Sort the data by the number of buses
    starting_point_counts = starting_point_counts.sort_values(by='Number of Buses', ascending=False)
    starting_point_counts = starting_point_counts[starting_point_counts['Starting Point']!='Not mentioned'].head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(starting_point_counts['Starting Point'], starting_point_counts['Number of Buses'], color='skyblue')
    ax.set_title('Number of Buses by Starting Point')
    ax.set_xlabel('Starting Point')
    ax.set_ylabel('Number of Buses')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


if a == 'Customer Preferences and Segmentation':
    st.title('Customer Preferences and Segmentation')
    st.write('By segmenting the data by bus type, fare, and ratings, you can understand different customer segments and their preferences. For example, budget-conscious travelers may prefer lower fares regardless of ratings.')

    andhra_df = pd.read_csv('andhra.csv')
    andhra_df = preprocess_data(andhra_df)
    def fare_segment(x):
        if x > 1000:
            return 'Costly'
        elif x > 500 and x<1000:
            return 'Medium'
        else:
            return 'Cheap'
    
    def rating_segment(rating):
        if rating < 3:
            return 'Low'
        elif rating <= 4:
            return 'Medium'
        else:
            return 'High'
    andhra_df.Bus_fare.astype('float')
    andhra_df.Ratings.astype('float')
    andhra_df['fare_segment'] = andhra_df.Bus_fare.apply(fare_segment)
    andhra_df['fare_segment'].value_counts()
    andhra_df['Rating_segment'] = andhra_df.Ratings.apply(rating_segment)
    bus_type_analysis = andhra_df.groupby('Bus_types').agg({'Bus_fare':'mean','Ratings':'mean'}).reset_index()
    fare_segment_analysis = andhra_df.groupby('fare_segment').agg({'Bus_fare':'mean','Ratings':'mean'}).reset_index()
    ratings_segment_analysis = andhra_df.groupby('Rating_segment').agg({'Bus_fare':'mean','Ratings':'mean'}).reset_index()
    ratings_segment_analysis[['Rating_segment','Bus_fare']].plot(kind='bar')
        # Plot the analysis
    plt.figure(figsize=(10, 6))
    bar_width = 0.35

    # Plot the analysis with dual y-axes
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot Bus_fare on ax1
    ax1.bar(ratings_segment_analysis['Rating_segment'], ratings_segment_analysis['Bus_fare'], width=0.4, align='center', color='skyblue', alpha=0.6)
    ax1.set_xlabel('Rating Segment')
    ax1.set_ylabel('Average Fare', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')

    # Create a second y-axis to plot Ratings
    ax2 = ax1.twinx()
    ax2.plot(ratings_segment_analysis['Rating_segment'], ratings_segment_analysis['Ratings'], color='orange', marker='o', linestyle='-', linewidth=2, label='Average Rating')
    ax2.set_ylabel('Average Rating', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    plt.title('Rating Segment Analysis')
    fig.tight_layout()
    plt.show()
    st.table(ratings_segment_analysis)


if a == 'Occupancy Rate':
    st.title('Occupancy Rate')
    st.write('By calculating the occupancy rate as (Total Seats - Available Seats) / Total Seats to see how full the buses typically are. This can help in optimizing bus capacity.')
    andhra_df = pd.read_csv('andhra.csv')
    andhra_df = preprocess_data(andhra_df)
    andhra_df['Total_seats'] = 50
    andhra_df['Occupancy_rate'] = round((andhra_df['Total_seats'] - andhra_df['Seats'])/andhra_df['Total_seats']*100,2)
    top_occupancy_rates = andhra_df[['Names','Occupancy_rate']].value_counts().head(10)
    top_occupancy_rates = pd.DataFrame(top_occupancy_rates)
    st.table(top_occupancy_rates)
        
    # Plot the top 10 occupancy rates using Pyplot
    fig, ax = plt.subplots(figsize=(10, 6))
    top_occupancy_rates.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Top 10 Occupancy Rates')
    ax.set_xlabel('Occupancy Rate (%)')
    ax.set_ylabel('Number of Buses')
    ax.set_xticklabels(top_occupancy_rates.index.astype(str), rotation=45)
    plt.tight_layout()
    plt.show()


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

if a == 'Project':
    selected_option = st.selectbox("Select any Question", list(options_data.keys()))
    selected_id = options_data[selected_option]

    query_(selected_id)










