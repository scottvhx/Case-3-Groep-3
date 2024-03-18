
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#data

airport= pd.read_csv('airports-extended-clean.csv', sep = ';')
flight1= pd.read_excel('1Flight 1.xlsx')
flight2= pd.read_excel('1Flight 2.xlsx')
flight3= pd.read_excel('1Flight 3.xlsx')
flight4= pd.read_excel('1Flight 4.xlsx')
flight5= pd.read_excel('1Flight 5.xlsx')
flight6= pd.read_excel('1Flight 6.xlsx')
flight7= pd.read_excel('1Flight 7.xlsx')
flight31= pd.read_excel('30Flight 1.xlsx')
flight32= pd.read_excel('30Flight 2.xlsx')
flight33= pd.read_excel('30Flight 3.xlsx')
flight34= pd.read_excel('30Flight 4.xlsx')
flight35= pd.read_excel('30Flight 5.xlsx')
flight36= pd.read_excel('30Flight 6.xlsx')
flight37= pd.read_excel('30Flight 7.xlsx')
schedule= pd.read_csv('schedule_airport.csv')

# Controleren als NaN of - in de dataframe zit en anders veranderen naar de de nul

schedule[["DL1", "IX1", "DL2", "IX2"]] = schedule[["DL1", "IX1", "DL2", "IX2"]].replace("-", "0")
flight1['TRUE AIRSPEED (derived)'].fillna(0, inplace=True)
flight2[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']] = flight3[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']].fillna(0)
flight3[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']] = flight3[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']].fillna(0)
flight4['TRUE AIRSPEED (derived)'].fillna(0, inplace=True)
flight5['TRUE AIRSPEED (derived)'].fillna(0, inplace=True)
flight6['TRUE AIRSPEED (derived)'].fillna(0, inplace=True)
flight7[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']] = flight3[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']].fillna(0)
flight32[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']] = flight3[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']].fillna(0)
flight33[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']] = flight3[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']].fillna(0)
flight34[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']] = flight3[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']].fillna(0)
flight36[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']] = flight3[['TRUE AIRSPEED (derived)', '[3d Latitude]', '[3d Longitude]', '[3d Altitude M]', '[3d Altitude Ft]', '[3d Heading]']].fillna(0)


# Controleren op duplicaten in de dataframe 
scheduleclean= schedule.drop_duplicates()
airportclean= airport.drop_duplicates()
flight1clean= flight1.drop_duplicates()
flight2clean= flight2.drop_duplicates()
flight3clean= flight3.drop_duplicates()
flight4clean= flight4.drop_duplicates()
flight5clean= flight5.drop_duplicates()
flight6clean= flight6.drop_duplicates()
flight7clean= flight7.drop_duplicates()
flight31clean= flight31.drop_duplicates()
flight32clean= flight32.drop_duplicates()
flight33clean= flight33.drop_duplicates()
flight34clean= flight34.drop_duplicates()
flight35clean= flight35.drop_duplicates()
flight36clean= flight36.drop_duplicates()
flight37clean= flight37.drop_duplicates()




# In[ ]:


# Dit is het hoofd van de site
st.title(':blue[Vertraagde vluchten :airplane:]')

    
st.subheader('*Welkom bij onze luchtvaartanalysehub!*')

st.write('Ontdek welke luchtvaartroutes wereldwijd het meest worden getroffen door vertragingen.      Van drukke binnenlandse vluchten tot internationale avonturen, we laten je de routes zien die je misschien wilt vermijden als je op tijd op je bestemming wilt aankomen.')

# URL van de afbeelding
image_url = "https://xenforo.com/community/media/plane-jpg.2194/full"

# Afbeelding weergeven in Streamlit
st.image(image_url, caption='Airplane', width=650)


# tabs die worden verwezen naar de onderstaande arguments

tab1, tab2, tab3, tab4, = st.tabs([":blue[Data]", ":blue[Vertraagde vluchten]", ":blue[Voorspellingen]", ":red[Conclusie]"])

# Voeg inhoud toe aan elke tab
with tab1:
    st.header("Data")


    
with tab2:
    st.header("Mogelijke vertraagde vluchten") 
    st.subheader('*Verken de wereld met onze interactieve kaart:*') 
    st.write("Duik dieper in de luchtvaartwereld met onze interactieve kaart. Volg de routes met de     hoogste vertragingen en zoom in op specifieke regio's om te zien waar de problemen het grootst zijn.")
 
    st.subheader('*Barplot*') 

    # Laad en reinig de gegevens
    scheduleclean = pd.read_csv('schedule_airport.csv')
    scheduleclean['STA_STD_ltc'] = pd.to_datetime(scheduleclean['STA_STD_ltc'])
    scheduleclean['ATA_ATD_ltc'] = pd.to_datetime(scheduleclean['ATA_ATD_ltc'])
    scheduleclean['Arrival_Status'] = scheduleclean['ATA_ATD_ltc'] - scheduleclean['STA_STD_ltc'] > pd.Timedelta(0)
    scheduleclean['Departure_Status'] = scheduleclean['STA_STD_ltc'] - scheduleclean['ATA_ATD_ltc'] > pd.Timedelta(0)

    # Bereken aantallen voor de plot
    total_arrival_flights = len(scheduleclean[scheduleclean['LSV'].str.contains('L')])
    total_departure_flights = len(scheduleclean[scheduleclean['LSV'].str.contains('S')])
    arrival_delay_count = scheduleclean[scheduleclean['Arrival_Status'] & scheduleclean['LSV'].str.contains('L')].shape[0]
    arrival_ontime_count = total_arrival_flights - arrival_delay_count
    departure_delay_count = scheduleclean[scheduleclean['Departure_Status'] & scheduleclean['LSV'].str.contains('S')].shape[0]
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
    

    




