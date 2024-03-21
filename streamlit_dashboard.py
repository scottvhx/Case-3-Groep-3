
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import data_cleaning
import flight_map
import plotly.express as px
import flight_analysis


st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.sidebar.title('🛬🛫 `Vertraagde Vluchten`')


    




# Dit is het hoofd van de site
st.title(':blue[Vertraagde vluchten :airplane:]')

    


# tabs die worden verwezen naar de onderstaande arguments

tab1, tab2, tab3, tab4, tab5= st.tabs([":blue[Welkom]", ":blue[Vertraagde vluchten]", ":blue[Voorspellingen]", ":red[Conclusie]", "blue[Bar-plot]"])

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
        st.write('*:blue[Conclusie uit de plot:]*')
        
        
        
        
        
        
        
        
        
       
        
        
####################

with tab3:
    st.header("Voorspellingen")
    st.subheader("*Voorspel vertragingen op je volgende vlucht:*")
    st.write("Ben je van plan om binnenkort te vliegen? Gebruik onze voorspellingsmodule om te zien hoeveel vertraging je kunt verwachten op jouw specifieke route. Met behulp van geavanceerde modellen kunnen we je een nauwkeurige inschatting geven, zodat je goed voorbereid op reis kunt gaan!")



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


with tab5: 

    st.write('test')


    



  










