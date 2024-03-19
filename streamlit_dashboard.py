
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import data_cleaning
import flight_map
import plotly.express as px
import plost


st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.sidebar.header('🛬🛫 `Vertraagde Vluchten`')
st.sidebar.subheader(' Barplot')

    




# Dit is het hoofd van de site
st.title(':blue[Vertraagde vluchten :airplane:]')

    


# tabs die worden verwezen naar de onderstaande arguments

tab1, tab2, tab3, tab4, tab5= st.tabs([":blue[Data]", ":blue[Vertraagde vluchten]", ":blue[Voorspellingen]", ":red[Conclusie]", "blue[Bar-plot]"])

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
        data = {
            'Vlucht Status': ['Vertraagd bij Aankomst', 'Aankomst op Tijd', 'Vertraagd bij Vertrek', 'Tijdig Vertrek'],
            'Aantal Vluchten': [arrival_delay_count, arrival_ontime_count, departure_delay_count, departure_ontime_count],
            'Percentage': [arrival_delay_percent, arrival_ontime_percent, departure_delay_percent, departure_ontime_percent]
        }
        df = pd.DataFrame(data)

        # Define colors
        delay_color = '#069AF3'
        ontime_color = '#13EAC9'

        # Create the plot using Plotly Express
        fig = px.bar(df, x='Vlucht Status', y='Aantal Vluchten', text='Percentage',
                     color='Vlucht Status', color_discrete_map={'Vertraagd bij Aankomst': delay_color,
                                                                   'Aankomst op Tijd': ontime_color,
                                                                   'Vertraagd bij Vertrek': delay_color,
                                                                   'Tijdig Vertrek': ontime_color},
                     labels={'Aantal Vluchten': 'Aantal Vluchten', 'Percentage': 'Percentage'},
                     title='Aantal Vluchten Verdeeld over Aankomst/Vertrek Status')

        # Display the plot in Streamlit
        st.plotly_chart(fig)


        st.write('*:blue[Conclusie uit de barplot:]*')
        st.write('Vertraging is vaker veroorzaakt op outstations, arrival delays/on time is 51.4%/48.6%. Grondafhandeling in ZRH is goed! Het aantal departure delays is namelijk erg verminderd tot een verhouding van ongeveer 20.8%/79.2%')
        
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

   

    # Subheader voor de Barplot in de zijbalk
    st.sidebar.subheader('Barplot')

    # Selectbox voor kleurselectie
    selected_color = st.sidebar.selectbox('Kies een kleur', ['Blauw', 'Groen', 'Rood'], key='color_discrete_map')

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

    # Gegevens voor de plot
    data = {
        'Vlucht Status': ['Vertraagd bij Aankomst', 'Aankomst op Tijd', 'Vertraagd bij Vertrek', 'Tijdig Vertrek'],
        'Aantal Vluchten': [arrival_delay_count, arrival_ontime_count, departure_delay_count, departure_ontime_count],
        'Percentage': [arrival_delay_percent, arrival_ontime_percent, departure_delay_percent, departure_ontime_percent]
    }

    # Maak de plot met Plotly Express
    fig = px.bar(pd.DataFrame(data), 
                 x='Vlucht Status', y='Aantal Vluchten', text='Percentage', 
                 color='Vlucht Status', 
                 color_discrete_map={'Vertraagd bij Aankomst': 'red', 'Aankomst op Tijd': 'green', 
                                     'Vertraagd bij Vertrek': 'red', 'Tijdig Vertrek': 'green'}, 
                 labels={'Aantal Vluchten': 'Aantal Vluchten', 'Percentage': 'Percentage'}, 
                 title='Aantal Vluchten Verdeeld over Aankomst/Vertrek Status')

    # Toon de plot in de zijbalk
    st.sidebar.plotly_chart(fig)




