import streamlit as st


# In[ ]:



st.title('Vertraagde vluchten :airplane:')

    
st.subheader(' Welkom bij onze luchtvaartanalysehub!')

st.write('Top 10 routes met de meeste vertraging: Ontdek welke luchtvaartroutes wereldwijd het meest worden getroffen door vertragingen. Van drukke binnenlandse vluchten tot internationale avonturen, we laten je de routes zien die je misschien wilt vermijden als je op tijd op je bestemming wilt aankomen.')



tab1, tab2, tab3 = st.tabs(["Vertraagde vluchten", "Voorspellingen", "Conclusie"])

# Voeg inhoud toe aan elke tab
with tab1:
    st.header("Mogelijke vertraagde vluchten")
    st.subheader('Verken de wereld met onze interactieve kaart:') 
    st.write("Duik dieper in de luchtvaartwereld met onze interactieve kaart. Volg de routes met de     hoogste vertragingen en zoom in op specifieke regio's om te zien waar de problemen het grootst zijn.")

with tab2:
    st.header("Voorspellingen")
    st.subheader("Voorspel vertragingen op je volgende vlucht:")
    st.write("Ben je van plan om binnenkort te vliegen? Gebruik onze voorspellingsmodule om te zien hoeveel vertraging je kunt verwachten op jouw specifieke route. Met behulp van geavanceerde modellen kunnen we je een nauwkeurige inschatting geven, zodat je goed voorbereid op reis kunt gaan!")

with tab3:
    st.write("Conclusie")
    expander = st.expander("Filter items")
red = expander.checkbox("Show red items.", True)
blue = expander.checkbox("Show blue items.", True)

if red:
    st.write(":red[This is a red item.]")
if blue:
    st.write(":blue[This is a blue item.]")
    




