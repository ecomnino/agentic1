import streamlit as st
import pandas as pd
import plotly.express as px

def generate_dummy_data():
    """
    Genereert een dummy dataset met namen en geslachten.
    
    Returns:
        pd.DataFrame: Een DataFrame met 5 rijen en kolommen 'Naam' en 'Geslacht'.
    """
    # Definieer de dummy data
    data = {
        'Naam': ['Alice', 'Bob', 'Charlie', 'Diana', 'Edward'],
        'Geslacht': ['Vrouw', 'Man', 'Man', 'Vrouw', 'Man']
    }
    
    # Maak een DataFrame aan
    df = pd.DataFrame(data)
    return df

def main():
    """
    Hoofdfunctie voor de Streamlit-app.
    """
    st.title("Dummy Dataset van Namen en Geslacht")
    st.sidebar.header("Navigatie")
    
    # Genereer de dummy data
    dummy_data = generate_dummy_data()
    
    # Sidebar opties
    st.sidebar.subheader("Dataset Weergave")
    show_data = st.sidebar.checkbox("Toon de dataset", value=True)
    
    if show_data:
        st.write("Hier is een dummy dataset met namen en geslachten:")
        st.dataframe(dummy_data)

    # Grafiek weergeven
    st.sidebar.subheader("Visualisatie")
    st.sidebar.write("Bekijk de verdeling van geslachten in de dataset.")
    
    # Tellen van geslachten
    gender_counts = dummy_data['Geslacht'].value_counts().reset_index()
    gender_counts.columns = ['Geslacht', 'Aantal']
    
    # Maak een Plotly grafiek
    fig = px.bar(gender_counts, x='Geslacht', y='Aantal', 
                 title='Aantal per Geslacht',
                 color='Geslacht',
                 labels={'Aantal': 'Aantal', 'Geslacht': 'Geslacht'},
                 text='Aantal')

    # Grafiek weergeven in de app
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()


### Uitleg van de wijzigingen:

# 1. **Sidebar**: We hebben een sidebar toegevoegd met een header en opties om de dataset weer te geven. Dit maakt de app interactiever en gebruiksvriendelijker.

# 2. **Checkbox**: Een checkbox in de sidebar laat de gebruiker toe om de dataset al dan niet weer te geven.

# 3. **Plotly Grafiek**: We hebben een staafdiagram toegevoegd dat het aantal mannen en vrouwen in de dataset weergeeft. Dit wordt gedaan met behulp van `plotly.express`.

# 4. **Data Verwerking**: We tellen het aantal mannen en vrouwen met `value_counts()` en maken een nieuwe DataFrame voor de grafiek.

# ### Hoe te gebruiken:
# 1. Zorg ervoor dat je `streamlit`, `pandas` en `plotly` hebt geïnstalleerd. Dit kan je doen met:
#    ```bash
#    pip install streamlit pandas plotly
#    ```

# 2. Sla de code op in een Python-bestand, bijvoorbeeld `app.py`.

# 3. Voer de Streamlit-app uit met het volgende commando:
#    ```bash
#    streamlit run app.py
#    ```

# 4. Open de aangegeven URL in je webbrowser om de app te bekijken. Je kunt de dataset bekijken en de grafiek zien die de verdeling van geslachten toont.