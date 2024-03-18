
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import data_cleaning
import flight_map

# Dit is het hoofd van de site
st.title(':blue[Vertraagde vluchten :airplane:]')

    


# tabs die worden verwezen naar de onderstaande arguments

tab1, tab2, tab3, tab4, tab5= st.tabs([":blue[Data]", ":blue[Vertraagde vluchten]", ":blue[Voorspellingen]", ":red[Conclusie]", "blue[Bar-plot]"])

# Voeg inhoud toe aan elke tab
with tab1:
    st.subheader('*Welkom bij onze luchtvaartanalysehub!*')

    st.write('Ontdek welke luchtvaartroutes wereldwijd het meest worden getroffen door vertragingen.      Van drukke binnenlandse vluchten tot internationale avonturen, we laten je de routes zien die je misschien wilt vermijden als je op tijd op je bestemming wilt aankomen.')

# URL van de afbeelding
    image_url = "https://xenforo.com/community/media/plane-jpg.2194/full"

# Afbeelding weergeven in Streamlit
    st.image(image_url, caption='Airplane', width=650)



    
with tab2:
    st.title("Flight Mapper")
    folium_static(flight_map.m, width=650, height=650)

    st.header("Mogelijke vertraagde vluchten") 
    st.subheader('*Verken de wereld met onze interactieve kaart:*') 
    st.write("Duik dieper in de luchtvaartwereld met onze interactieve kaart. Volg de routes met de     hoogste vertragingen en zoom in op specifieke regio's om te zien waar de problemen het grootst zijn.")
 
    st.subheader('*Barplot*') 

    # Laad en reinig de gegevens
    #scheduleclean = pd.read_csv('schedule_airport.csv')
    data_cleaning.scheduleclean['STA_STD_ltc'] = pd.to_datetime(data_cleaning.scheduleclean['STA_STD_ltc'])
    data_cleaning.scheduleclean['ATA_ATD_ltc'] = pd.to_datetime(data_cleaning.scheduleclean['ATA_ATD_ltc'])
    data_cleaning.scheduleclean['Arrival_Status'] = data_cleaning.scheduleclean['ATA_ATD_ltc'] - data_cleaning.scheduleclean['STA_STD_ltc'] > pd.Timedelta(0)
    data_cleaning.scheduleclean['Departure_Status'] = data_cleaning.scheduleclean['STA_STD_ltc'] - data_cleaning.scheduleclean['ATA_ATD_ltc'] > pd.Timedelta(0)

    # Bereken aantallen voor de plot
    total_arrival_flights = len(data_cleaning.scheduleclean[data_cleaning.scheduleclean['LSV'].str.contains('L')])
    total_departure_flights = len(data_cleaning.scheduleclean[data_cleaning.scheduleclean['LSV'].str.contains('S')])
    arrival_delay_count = data_cleaning.scheduleclean[data_cleaning.scheduleclean['Arrival_Status'] & data_cleaning.scheduleclean['LSV'].str.contains('L')].shape[0]
    arrival_ontime_count = total_arrival_flights - arrival_delay_count
    departure_delay_count = data_cleaning.scheduleclean[data_cleaning.scheduleclean['Departure_Status'] & data_cleaning.scheduleclean['LSV'].str.contains('S')].shape[0]
    departure_ontime_count = total_departure_flights - departure_delay_count

    # Set kleuren voor de balken
    delay_color = '#069AF3'
    ontime_color = '#13EAC9'

    # Maak de plot
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(['Vertraagd bij Aankomst', 'Aankomst op Tijd', 'Vertraagd bij Vertrek', 'Tijdig Vertrek'], 
                  [arrival_delay_count, arrival_ontime_count, departure_delay_count, departure_ontime_count],
                  color=[delay_color, ontime_color, delay_color, ontime_color])
    ax.set_xlabel('Vlucht Status')
    ax.set_ylabel('Aantal Vluchten')
    ax.set_title('Aantal Vluchten Verdeeld over Aankomst/Vertrek Status')

    # Voeg percentages toe aan de balken
    for bar in bars[:2]:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height / total_arrival_flights:.1%}', ha='center', va='bottom')
    for bar in bars[2:]:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height / total_departure_flights:.1%}', ha='center', va='bottom')

    # Toon de plot in Streamlit
    st.pyplot(fig)
    
    st.write('*:blue[Conclusion out of the graph:]*')
    st.write('Vertraging is vaker veroorzaakt op outstations, arrival delays/on time is 51.4%/48.6%. Grondafhandeling in ZRH is goed! Het aantal departure delays is namelijk erg verminderd tot een verhouding van ongeveer 20.8%/79.2%')

with tab3:
    st.header("Voorspellingen")
    st.subheader("*Voorspel vertragingen op je volgende vlucht:*")
    st.write("Ben je van plan om binnenkort te vliegen? Gebruik onze voorspellingsmodule om te zien hoeveel vertraging je kunt verwachten op jouw specifieke route. Met behulp van geavanceerde modellen kunnen we je een nauwkeurige inschatting geven, zodat je goed voorbereid op reis kunt gaan!")



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
    
 
# Load aircraft types and max passenger capacity from Excel file
    aircraft_capacity = pd.read_excel('data/AC-MaxPassengers.xlsx')  # Update with your file path

# Assuming avg_delay_per_aircraft_type DataFrame contains 'ACT' and 'Average_Delay_hours' columns

# Group aircraft types based on max passenger capacity
    grouped_aircraft = aircraft_capacity.groupby('Max passengers')

# Create dropdown menu options
    dropdown_options = ['All Small Aircraft', 'All Narrow Aircraft', 'All Wide Aircraft']
    dropdown_options.extend(grouped_aircraft.groups.keys())

# Create a dropdown menu widget
    selected_category = st.selectbox('Select Aircraft Category:', dropdown_options)

    def plot_delay_per_aircraft_category(category):
        if category.startswith('All'):
            # Plot all aircraft types
            if category == 'All Small Aircraft':
                filtered_data = avg_delay_per_aircraft_type[avg_delay_per_aircraft_type['ACT'].isin(aircraft_capacity[aircraft_capacity['Max passengers'] <= 100]['Aircraft'])]
            elif category == 'All Narrow Aircraft':
                filtered_data = avg_delay_per_aircraft_type[avg_delay_per_aircraft_type['ACT'].isin(aircraft_capacity[(aircraft_capacity['Max passengers'] > 100) & (aircraft_capacity['Max passengers'] <= 250)]['Aircraft'])]
            elif category == 'All Wide Aircraft':
                filtered_data = avg_delay_per_aircraft_type[avg_delay_per_aircraft_type['ACT'].isin(aircraft_capacity[aircraft_capacity['Max passengers'] > 250]['Aircraft'])]
        else:
            # Plot specific aircraft type
            filtered_data = avg_delay_per_aircraft_type[avg_delay_per_aircraft_type['ACT'].isin(grouped_aircraft.get_group(category)['Aircraft'])]

        # Create a bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='ACT', y='Average_Delay_hours', data=filtered_data)
        plt.title('Average Delay per Aircraft Type')
        plt.xlabel('Aircraft Type')
        plt.ylabel('Average Delay (hours)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        st.pyplot()


    # Call the function to plot the initial graph
    plot_delay_per_aircraft_category(selected_category)

