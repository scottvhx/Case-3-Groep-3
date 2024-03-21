
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import data_cleaning
import flight_map
import plotly.express as px
import flight_analysis
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.sidebar.title('🛬🛫 `Vertraagde Vluchten`')


    




# Dit is het hoofd van de site
st.title(':blue[Vertraagde vluchten :airplane:]')

    


# tabs die worden verwezen naar de onderstaande arguments

tab1, tab2, tab3, tab4, tab5= st.tabs([":blue[Welkom]", ":blue[Vlucht data]", ":blue[Voorspellingen]", ":red[Conclusie]"])

############################

# Voeg inhoud toe aan elke tab
with tab1:
    st.subheader('*Welkom bij onze luchtvaartanalysehub!*')

    st.write('Ontdek welke luchtvaartroutes wereldwijd het meest worden getroffen door vertragingen.      Van drukke binnenlandse vluchten tot internationale avonturen, we laten je de routes zien die je misschien wilt vermijden als je op tijd op je bestemming wilt aankomen.')

# URL van de afbeelding
    image_url = "https://xenforo.com/community/media/plane-jpg.2194/full"

# Afbeelding weergeven in Streamlit
    st.image(image_url, caption='Airplane', width=650)


##########################
    
with tab2:
        st.header("Mogelijke vertraagde vluchten") 
        st.subheader('*Verken de wereld met onze interactieve kaart:*') 
        st.write("Duik dieper in de luchtvaartwereld met onze interactieve kaart. Volg de routes met de  hoogste vertragingen en zoom in op specifieke regio's om te zien waar de problemen het grootst zijn.")
    
        st.header("Flight Mapper")
        folium_static(flight_map.m, width=650, height=650)
#############################

        st.header('*Lijndiagram*') 

        # Laad de gegevens en converteer STD kolom naar datetime met het juiste formaat

        data_cleaning.scheduleclean['STD'] = pd.to_datetime(data_cleaning.scheduleclean['STD'], format="%d/%m/%Y")

        # Filter de data om alleen binnenkomende vluchten te krijgen
        inbound_flights = data_cleaning.scheduleclean[data_cleaning.scheduleclean['LSV'].str.contains('L', na=False)]

        # Groepeer per maand en tel het aantal vluchten
        monthly_flights = inbound_flights.groupby(pd.Grouper(key='STD', freq='M')).size()

        # Creëer een interactieve lijngrafiek
        fig = go.Figure()

        # Voeg een lijn trace toe voor het aantal vliegtuigen
        fig.add_trace(go.Scatter(x=monthly_flights.index, y=monthly_flights.values, mode='lines', name='Aircraft Count'))

        # Update layout om een slider te bevatten voor het wijzigen van het tijdsinterval
        fig.update_layout(
            title='Aantal vliegtuigen per maand',
            xaxis=dict(
                title='Maand',
                type='date',
                rangeslider=dict(
                    visible=True
                )
            ),
            yaxis=dict(
                title='Aantal vliegtuigen'
            )
        )

        # Toon de grafiek in Streamlit
        st.plotly_chart(fig)
        st.write('*:blue[Conclusie uit de lijndiagram:]*')
        st.write('Het lijndiagram toont een herstel in juli 2020, na de impact van de COVID-19-pandemie vanaf januari 2020. Echter, in de herfst- en wintermaanden is er weer een afname te zien.')


#############################
        st.header('*Barplot*') 
  
        # Load and clean the data
        data_cleaning.scheduleclean['STA_STD_ltc'] = pd.to_datetime(data_cleaning.scheduleclean['STA_STD_ltc'])
        data_cleaning.scheduleclean['ATA_ATD_ltc'] = pd.to_datetime(data_cleaning.scheduleclean['ATA_ATD_ltc'])
        data_cleaning.scheduleclean['Arrival_Status'] = data_cleaning.scheduleclean['ATA_ATD_ltc'] - data_cleaning.scheduleclean['STA_STD_ltc'] > pd.Timedelta(0)
        data_cleaning.scheduleclean['Departure_Status'] = data_cleaning.scheduleclean['STA_STD_ltc'] - data_cleaning.scheduleclean['ATA_ATD_ltc'] > pd.Timedelta(0)

        # Calculate counts for the plot
        total_arrival_flights = len(data_cleaning.scheduleclean[data_cleaning.scheduleclean['LSV'].str.contains('L')])
        total_departure_flights = len(data_cleaning.scheduleclean[data_cleaning.scheduleclean['LSV'].str.contains('S')])
        arrival_delay_count = data_cleaning.scheduleclean[data_cleaning.scheduleclean['Arrival_Status'] & data_cleaning.scheduleclean['LSV'].str.contains('L')].shape[0]
        arrival_ontime_count = total_arrival_flights - arrival_delay_count
        departure_delay_count = data_cleaning.scheduleclean[data_cleaning.scheduleclean['Departure_Status'] & data_cleaning.scheduleclean['LSV'].str.contains('S')].shape[0]
        departure_ontime_count = total_departure_flights - departure_delay_count

        # Calculate percentages
        arrival_delay_percent = round(arrival_delay_count / total_arrival_flights * 100, 1)
        arrival_ontime_percent = round(arrival_ontime_count / total_arrival_flights * 100, 1)
        departure_delay_percent = round(departure_delay_count / total_departure_flights * 100, 1)
        departure_ontime_percent = round(departure_ontime_count / total_departure_flights * 100, 1)

        # Create a DataFrame for the plot
        data_arrival = {
            'Vlucht Status': ['Vertraagd bij Aankomst', 'Aankomst op Tijd'],
            'Aantal Vluchten': [arrival_delay_count, arrival_ontime_count],
            'Percentage': [arrival_delay_percent, arrival_ontime_percent]
        }
        df_arrival = pd.DataFrame(data_arrival)

        data_departure = {
            'Vlucht Status': ['Vertraagd bij Vertrek', 'Tijdig Vertrek'],
            'Aantal Vluchten': [departure_delay_count, departure_ontime_count],
            'Percentage': [departure_delay_percent, departure_ontime_percent]
        }
        df_departure = pd.DataFrame(data_departure)

        # Define colors
        delay_color = '#069AF3'
        ontime_color = '#13EAC9'

        # Sidebar
        with st.sidebar:
            st.subheader('Barplot')
            selected_option = st.selectbox('Kies een optie', ['Aankomst', 'Vertrek'])

        # Map opties naar kleuren
        color_map_arrival = {'Vertraagd bij Aankomst': delay_color, 'Aankomst op Tijd': ontime_color}
        color_map_departure = {'Vertraagd bij Vertrek': delay_color, 'Tijdig Vertrek': ontime_color}

        # Create the plot using Plotly Express
        if selected_option == 'Aankomst':
            fig = px.bar(df_arrival, x='Vlucht Status', y='Aantal Vluchten', text='Percentage',
                         color='Vlucht Status',
                         color_discrete_map=color_map_arrival,
                         labels={'Aantal Vluchten': 'Aantal Vluchten', 'Percentage': 'Percentage'},
                         title='Aantal Vluchten Verdeeld over Aankomst Status')
        else:
            fig = px.bar(df_departure, x='Vlucht Status', y='Aantal Vluchten', text='Percentage',
                         color='Vlucht Status',
                         color_discrete_map=color_map_departure,
                         labels={'Aantal Vluchten': 'Aantal Vluchten', 'Percentage': 'Percentage'},
                         title='Aantal Vluchten Verdeeld over Vertrek Status')

        # Show the plot
        st.plotly_chart(fig)

        st.write('*:blue[Conclusie uit de barplot:]*')
        st.write('Vertraging is vaker veroorzaakt op outstations, arrival delays/on time is 51.4%/48.6%. Grondafhandeling in ZRH is goed! Het aantal departure delays is namelijk erg verminderd tot een verhouding van ongeveer 20.8%/79.2%')

         # Convert 'STA_STD_ltc' and 'ATA_ATD_ltc' to datetime format
        data_cleaning.scheduleclean['STA_STD_ltc'] = pd.to_datetime(data_cleaning.scheduleclean['STA_STD_ltc'])
        data_cleaning.scheduleclean['ATA_ATD_ltc'] = pd.to_datetime(data_cleaning.scheduleclean['ATA_ATD_ltc'])

        # Calculate the delay in seconds
        data_cleaning.scheduleclean['Delay_seconds'] = (data_cleaning.scheduleclean['ATA_ATD_ltc'] - data_cleaning.scheduleclean['STA_STD_ltc']).dt.total_seconds()

        # Convert delay to timedeltas with custom formatting
        data_cleaning.scheduleclean['Delay'] = pd.to_timedelta(data_cleaning.scheduleclean['Delay_seconds'], unit='s')

        # Add '+' or '-' sign manually based on delay
        data_cleaning.scheduleclean['Delay'] = data_cleaning.scheduleclean['Delay'].apply(lambda x: ('+' if x >= pd.Timedelta(0) else '-') + str(abs(x)))

        # Drop the temporary column
        data_cleaning.scheduleclean.drop(columns=['Delay_seconds'], inplace=True)

        # Convert 'Delay' column to numeric format (hours)
        data_cleaning.scheduleclean['Delay_hours'] = pd.to_timedelta(data_cleaning.scheduleclean['Delay']).dt.total_seconds() / 3600

        # Grouping by Location and calculating the average Delay
        avg_delay_per_location = data_cleaning.scheduleclean.groupby('Org/Des')['Delay_hours'].mean().reset_index()

        # Renaming the columns for clarity
        avg_delay_per_location.columns = ['Org/Des', 'Average_Delay_hours']

        st.header('*Scatterplot*') 

        # Filter the dataset for values with 'S' in the 'LSV' column
        departure_data = data_cleaning.scheduleclean[data_cleaning.scheduleclean['LSV'] == 'S']

        # Filter the dataset for values with a '+' sign in the 'Delay' column
        positive_delay_data = departure_data[departure_data['Delay'].str.startswith('+')]

        # Extract departure time in minutes past midnight
        departure_time_minutes = positive_delay_data['ATA_ATD_ltc'].dt.hour * 60 + positive_delay_data['STA_STD_ltc'].dt.minute

        # Extract delay minutes from the 'Delay' column
        delay_minutes = positive_delay_data['Delay'].str.extract(r'\+(\d+) days (\d+):(\d+):').astype(float)
        delay_minutes = delay_minutes[1] * 60 + delay_minutes[2]  # Convert hours to minutes and add minutes

        # Calculate mean delay
        mean_delay = delay_minutes.mean()

        # Create dataframe for Plotly scatterplot
        scatter_data = pd.DataFrame({'Departure_Time': departure_time_minutes, 'Delay': delay_minutes})

        # Create interactive scatterplot
        fig = px.scatter(scatter_data, x='Departure_Time', y='Delay', color='Delay', labels={'Departure_Time': 'Vertrektijd (uren)', 'Delay': 'Vertraging (minuten)'},
                         title='Relatie tussen vertraging en vertrektijd',
                         hover_data={'Departure_Time': False, 'Delay': True}, trendline='ols')  

        # Change color of trend line to red
        fig.update_traces(line=dict(color='red'))

        # Add mean line
        fig.add_hline(y=mean_delay, line_dash="dash", line_color="orange", annotation_text=f"Mean Delay: {mean_delay:.2f} minuten", annotation_position="bottom right", annotation_y=0.6)

        # Customize x-axis tick values and labels
        tick_values = list(range(int(departure_time_minutes.min()), int(departure_time_minutes.max()) + 1, 120))  # Every 2 hours
        tick_labels = [f"{h//60:02d}:{h%60:02d}" for h in tick_values]  # Format tick labels as HH:MM
        fig.update_xaxes(tickvals=tick_values, ticktext=tick_labels)

        # Update layout to make the graph bigger
        fig.update_layout(height=600, width=800, showlegend=False)

        # Display the plot in Streamlit
        st.plotly_chart(fig)
        st.write('*:blue[Conclusie uit de plot:]*')
        
##################        
        
        st.header('*Scatterplot*') 

        # Filter the dataset for values with 'S' in the 'LSV' column
        departure_data = data_cleaning.scheduleclean[data_cleaning.scheduleclean['LSV'] == 'L']

        # Filter the dataset for values with a '+' sign in the 'Delay' column
        positive_delay_data = departure_data[departure_data['Delay'].str.startswith('+')]

        # Extract departure time in minutes past midnight
        departure_time_minutes = positive_delay_data['ATA_ATD_ltc'].dt.hour * 60 + positive_delay_data['STA_STD_ltc'].dt.minute

        # Extract delay minutes from the 'Delay' column
        delay_minutes = positive_delay_data['Delay'].str.extract(r'\+(\d+) days (\d+):(\d+):').astype(float)
        delay_minutes = delay_minutes[1] * 60 + delay_minutes[2]  # Convert hours to minutes and add minutes

        # Calculate mean delay
        mean_delay = delay_minutes.mean()

        # Create dataframe for Plotly scatterplot
        scatter_data = pd.DataFrame({'Departure_Time': departure_time_minutes, 'Delay': delay_minutes})

        # Create interactive scatterplot
        fig = px.scatter(scatter_data, x='Departure_Time', y='Delay', color='Delay', labels={'Departure_Time': 'Aankomsttijd (uren)', 'Delay': 'Vertraging (minuten)'},
                         title='Relatie tussen vertraging en aankomsttijd',
                         hover_data={'Departure_Time': False, 'Delay': True}, trendline='ols')  

        # Change color of trend line to red
        fig.update_traces(line=dict(color='red'))

        # Add mean line
        fig.add_hline(y=mean_delay, line_dash="dash", line_color="orange", annotation_text=f"Mean Delay: {mean_delay:.2f} minuten", annotation_position="bottom right", annotation_y=0.6)

        # Customize x-axis tick values and labels
        tick_values = list(range(int(departure_time_minutes.min()), int(departure_time_minutes.max()) + 1, 120))  # Every 2 hours
        tick_labels = [f"{h//60:02d}:{h%60:02d}" for h in tick_values]  # Format tick labels as HH:MM
        fig.update_xaxes(tickvals=tick_values, ticktext=tick_labels)

        # Update layout to make the graph bigger
        fig.update_layout(height=600, width=800, showlegend=False)

        # Display the plot in Streamlit
        st.plotly_chart(fig)
        st.write('*:blue[Conclusie uit de plot:]*')       
        

        
        st.header('*Barplot*')
         # Grouping by Aircraft Type (ACT) and calculating the average Delay
        avg_delay_per_aircraft_type =data_cleaning.scheduleclean.groupby('ACT')['Delay_hours'].mean().reset_index()

        # Renaming the columns for clarity
        avg_delay_per_aircraft_type.columns = ['ACT', 'Average_Delay_hours']

        # Create bar plot with Plotly Express
        fig = px.bar(avg_delay_per_aircraft_type, x='ACT', y='Average_Delay_hours', 
                     title='Gemiddelde Vertraging per Vliegtuigtype',
                     labels={'ACT': 'Vliegtuigtype', 'Average_Delay_hours': 'Gemiddelde Vertraging (uren)'},
                     template='plotly_white')  # Use 'plotly_white' template for light background

        # Rotate x-axis labels for better readability
        fig.update_xaxes(tickangle=45)

        # Display checkboxes for selecting aircraft types
        selected_aircraft_types = st.multiselect("Selecteer vliegtuigtype", avg_delay_per_aircraft_type['ACT'])

        # Filter the data based on selected aircraft types
        if selected_aircraft_types:
            filtered_data = avg_delay_per_aircraft_type[avg_delay_per_aircraft_type['ACT'].isin(selected_aircraft_types)]
        else:
            filtered_data = avg_delay_per_aircraft_type  # Show all aircraft types if nothing selected


        # Update the plot with filtered data
        fig.update_traces(x=filtered_data['ACT'], y=filtered_data['Average_Delay_hours'])

        # Show the plot using Streamlit
        st.plotly_chart(fig)
        
        
        
#######################        
        st.header('*Location*')

        # Convert 'STA_STD_ltc' and 'ATA_ATD_ltc' to datetime format
        data_cleaning.scheduleclean['STA_STD_ltc'] = pd.to_datetime(data_cleaning.scheduleclean['STA_STD_ltc'])
        data_cleaning.scheduleclean['ATA_ATD_ltc'] = pd.to_datetime(data_cleaning.scheduleclean['ATA_ATD_ltc'])

        # Calculate the delay in seconds
        data_cleaning.scheduleclean['Delay_seconds'] = (data_cleaning.scheduleclean['ATA_ATD_ltc'] - data_cleaning.scheduleclean['STA_STD_ltc']).dt.total_seconds()

        # Convert delay to timedeltas with custom formatting
        data_cleaning.scheduleclean['Delay'] = pd.to_timedelta(data_cleaning.scheduleclean['Delay_seconds'], unit='s')

        # Add '+' or '-' sign manually based on delay
        data_cleaning.scheduleclean['Delay'] = data_cleaning.scheduleclean['Delay'].apply(lambda x: ('+' if x >= pd.Timedelta(0) else '-') + str(abs(x)))

        # Drop the temporary column
        data_cleaning.scheduleclean.drop(columns=['Delay_seconds'], inplace=True)

        # Convert 'Delay' column to numeric format (hours)
        data_cleaning.scheduleclean['Delay_hours'] = pd.to_timedelta(data_cleaning.scheduleclean['Delay']).dt.total_seconds() / 3600

        # Grouping by Location and calculating the average Delay
        avg_delay_per_location = data_cleaning.scheduleclean.groupby('Org/Des')['Delay_hours'].mean().reset_index()

        # Renaming the columns for clarity
        avg_delay_per_location.columns = ['Org/Des', 'Average_Delay_hours']

        # Dropdown menu to select which location to display
        st.sidebar.subheader('Location')
        selected_location = st.sidebar.selectbox('Selecteer een locatie', avg_delay_per_location['Org/Des'].unique())

        # Filter data for the selected location
        selected_data = avg_delay_per_location[avg_delay_per_location['Org/Des'] == selected_location]

        # Display selected data
        if not selected_data.empty:
            st.write(f"Gemiddelde vertraging voor locatie '{selected_location}': {selected_data.iloc[0]['Average_Delay_hours']:.2f} uur")
        else:
            st.write("Geen gegevens beschikbaar voor deze locatie.")        

        
####################

with tab3:
    st.header("Voorspellingen")
    st.subheader("*Voorspel vertragingen op je volgende vlucht:*")
    st.write("Ben je van plan om binnenkort te vliegen? Gebruik onze voorspellingsmodule om te zien hoeveel vertraging je kunt verwachten op jouw specifieke route. Met behulp van geavanceerde modellen kunnen we je een nauwkeurige inschatting geven, zodat je goed voorbereid op reis kunt gaan!")

     # Filter the dataset based on your conditions
    filtered_data = data_cleaning.scheduleclean[(data_cleaning.scheduleclean['Delay'].str.contains('\+')) & (data_cleaning.scheduleclean['LSV'].str.contains('S'))]

    # Create a new DataFrame with the filtered data
    flightdelays = pd.DataFrame(filtered_data)

    # Remove '+' and 'days' from the Delay column
    flightdelays['Delay'] = flightdelays['Delay'].str.replace('+', '').str.replace(' days', '')

    # Now 'Delay' column should only contain numerical values in the format '00:00:00'

    # Create a new DataFrame with the modified data
    flightdelays2 = pd.DataFrame(flightdelays)

    # Now you have a new DataFrame containing only the modified and filtered data

    # List of columns to remove
    columns_to_remove = ['ATA_ATD_ltc', 'TAR', 'GAT', 'DL1', 'IX1', 'DL2', 'IX2', 'RWY', 'RWC', 'Identifier']

    # Drop the specified columns
    flightdelays2 = flightdelays2.drop(columns=columns_to_remove)

    # Convert 'STD' column to datetime format
    flightdelays2['STD'] = pd.to_datetime(flightdelays2['STD'], format='%d/%m/%Y')

    # Convert 'STA_STD_ltc' column to datetime format
    flightdelays2['STA_STD_ltc'] = pd.to_datetime(flightdelays2['STA_STD_ltc'], format='%H:%M:%S')

    # Remove initial '0' and space from 'Delay' column
    flightdelays2['Delay'] = flightdelays2['Delay'].str[2:]

    # Check the first few rows to verify the changes
    print(flightdelays2.head())

    flightdelays3 = pd.DataFrame(flightdelays2)

    # Check for NaN values in the entire DataFrame
    nan_values = flightdelays3.isna().any()

    # If you want to count the total number of NaN values in each column, you can use sum()
    nan_count = flightdelays3.isna().sum()

    # Remove rows with NaN values in the 'Org/Des' column
    flightdelays3 = flightdelays3.dropna(subset=['Org/Des'])

    # Convert 'STD' column to datetime format
    flightdelays3['STD'] = pd.to_datetime(flightdelays3['STD'], format='%d/%m/%Y')

    # Convert 'STA_STD_ltc' column to datetime format
    flightdelays3['STA_STD_ltc'] = pd.to_datetime(flightdelays3['STA_STD_ltc'], format='%H:%M:%S')

    # Convert 'Delay'
    flightdelays3['Delay'] = pd.to_datetime(flightdelays3['Delay'], format='%H:%M:%S')

    # Check the data types of each column
    print(flightdelays3.dtypes)

    


    # Assuming flightdelays3 is your dataset
    # Features for prediction: 'Org/Des'
    # Target variable: 'Delay'
    # Replace flightdelays3 with your actual dataset
    X = flightdelays3[['Org/Des']]
    y = flightdelays3['Delay_hours']

    # Step 1: Split the Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 2: Feature Encoding (One-Hot Encoding for categorical feature 'Org/Des')
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_train_encoded = encoder.fit_transform(X_train[['Org/Des']])
    X_test_encoded = encoder.transform(X_test[['Org/Des']])

    # Step 3: Model Selection and Training (using Random Forest)
    model = RandomForestRegressor()  # Initialize Random Forest regressor
    model.fit(X_train_encoded, y_train)

    # Step 4: Model Evaluation
    predictions = model.predict(X_test_encoded)
    mae = mean_absolute_error(y_test, predictions)
    print("Mean Absolute Error:", mae)

    # Step 5: Prediction (for specific ICAO destination)
    icao_code = input("Enter the ICAO code for the destination: ")

    # Convert ICAO code to one-hot encoded format
    new_data = pd.DataFrame({'Org/Des': [icao_code]})
    new_data_encoded = encoder.transform(new_data[['Org/Des']])

    # Make prediction for the specific destination
    predicted_delay = model.predict(new_data_encoded)

    # Display the predicted delay
    print(f"Predicted delay for {icao_code}: {predicted_delay[0]}")




#################
with tab4:
    st.write("Conclusie")
    expander = st.expander("Filter items")
    red = expander.checkbox("Show red items.", True)
    blue = expander.checkbox("Show blue items.", True)

    if red:
        st.write(":red[This is a red item.]")
    if blue:
        st.write(":blue[This is a blue item.]")





    



  










