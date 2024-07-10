import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Charger les données
@st.cache_data
def load_data():
    return pd.read_csv("Agrofood_co2_emission.csv")

df = load_data()

st.title("Analyse des Émissions et de l'Utilisation des Terres")

st.write("""
Cette application présente une analyse visuelle des émissions, de l'utilisation des terres et des tendances démographiques à travers différentes régions et périodes. Explorez les graphiques interactifs ci-dessous pour découvrir des tendances fascinantes et des insights importants.
""")

# Fonction pour créer le graphique "Empreintes de Feu"
def create_fire_fingerprint_chart(df):
    areas = df['Area'].unique().tolist()
    fig = make_subplots(rows=1, cols=1)

    for area in areas:
        area_data = df[df['Area'] == area].sort_values('Year')
        
        for fire_type in ['Savanna fires', 'Forest fires', 'Fires in organic soils', 'Fires in humid tropical forests']:
            fig.add_trace(
                go.Scatter(
                    x=area_data['Year'],
                    y=area_data[fire_type],
                    name=fire_type,
                    mode='lines',
                    stackgroup='one',
                    groupnorm='percent',
                    visible=(area == areas[0])
                )
            )

    updatemenus = [
        dict(
            active=0,
            buttons=list([
                dict(label=area,
                     method="update",
                     args=[{"visible": [area == selected_area for selected_area in areas for _ in range(4)]},
                           {"title": f"Empreinte de Feu pour {area}"}])
                for area in areas
            ]),
        )
    ]

    fig.update_layout(
        updatemenus=updatemenus,
        title_text="Empreintes de Feu par Région",
        xaxis_title="Année",
        yaxis_title="Pourcentage du Total des Feux",
        legend_title="Types de Feux"
    )

    return fig

# Fonction pour créer le graphique "Flux Forestier"
def create_forest_flux_chart(df):
    areas = df['Area'].unique().tolist()
    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

    for area in areas:
        area_data = df[df['Area'] == area].sort_values('Year')
        
        fig.add_trace(
            go.Scatter(
                x=area_data['Year'],
                y=area_data['Forestland'],
                name='Zone Forestière',
                mode='lines',
                line=dict(color='green'),
                visible=(area == areas[0])
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=area_data['Year'],
                y=area_data['Net Forest conversion'],
                name='Conversion Forestière Nette',
                mode='lines',
                line=dict(color='red'),
                visible=(area == areas[0])
            ),
            secondary_y=True
        )

    updatemenus = [
        dict(
            active=0,
            buttons=list([
                dict(label=area,
                     method="update",
                     args=[{"visible": [area == selected_area for selected_area in areas for _ in range(2)]},
                           {"title": f"Flux Forestier pour {area}"}])
                for area in areas
            ]),
        )
    ]

    fig.update_layout(
        updatemenus=updatemenus,
        title_text="Flux Forestier par Région",
        xaxis_title="Année",
        legend_title="Métriques"
    )

    fig.update_yaxes(title_text="Zone Forestière", secondary_y=False)
    fig.update_yaxes(title_text="Conversion Forestière Nette", secondary_y=True)

    return fig

# Fonction pour créer le graphique "Chronologie de la Modernisation Agricole"
def create_agricultural_modernization_chart(df):
    areas = df['Area'].unique().tolist()
    fig = make_subplots(rows=1, cols=1)

    emission_types = {
        'Traditionnel': {'Manure left on Pasture': 'brown'},
        'Moderne': {
            'Fertilizers Manufacturing': 'blue',
            'Pesticides Manufacturing': 'red'
        }
    }

    for area in areas:
        area_data = df[df['Area'] == area].sort_values('Year')
        
        for category, emissions in emission_types.items():
            for emission, color in emissions.items():
                fig.add_trace(
                    go.Scatter(
                        x=area_data['Year'],
                        y=area_data[emission],
                        name=f"{emission} ({category})",
                        mode='lines',
                        line=dict(color=color),
                        visible=(area == areas[0])
                    )
                )

    updatemenus = [
        dict(
            active=0,
            buttons=list([
                dict(label=area,
                     method="update",
                     args=[{"visible": [area == selected_area for selected_area in areas for _ in range(len(emission_types['Traditionnel']) + len(emission_types['Moderne']))]},
                           {"title": f"Chronologie de la Modernisation Agricole pour {area}"}])
                for area in areas
            ]),
        )
    ]

    fig.update_layout(
        updatemenus=updatemenus,
        title_text="Chronologie de la Modernisation Agricole",
        xaxis_title="Année",
        yaxis_title="Émissions",
        legend_title="Types d'Émissions"
    )

    return fig

# Fonction pour créer le graphique "Évolution des Émissions Par Habitant"
def create_emissions_per_capita_chart(df):
    areas = df['Area'].unique().tolist()
    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

    for area in areas:
        area_data = df[df['Area'] == area].sort_values('Year')
        
        area_data['Population Totale'] = area_data['Rural population'] + area_data['Urban population']
        area_data['Pourcentage de Population Urbaine'] = area_data['Urban population'] / area_data['Population Totale'] * 100
        area_data['Émissions Par Habitant'] = area_data['total_emission'] / area_data['Population Totale']
        
        fig.add_trace(
            go.Scatter(
                x=area_data['Year'],
                y=area_data['Émissions Par Habitant'],
                name='Émissions Par Habitant',
                mode='lines',
                line=dict(color='red'),
                visible=(area == areas[0])
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=area_data['Year'],
                y=area_data['Pourcentage de Population Urbaine'],
                name='Pourcentage de Population Urbaine',
                mode='lines',
                line=dict(color='blue'),
                visible=(area == areas[0])
            ),
            secondary_y=True
        )

    updatemenus = [
        dict(
            active=0,
            buttons=list([
                dict(label=area,
                     method="update",
                     args=[{"visible": [area == selected_area for selected_area in areas for _ in range(2)]},
                           {"title": f"Évolution des Émissions Par Habitant pour {area}"}])
                for area in areas
            ]),
        )
    ]

    fig.update_layout(
        updatemenus=updatemenus,
        title_text="Évolution des Émissions Par Habitant",
        xaxis_title="Année",
        legend_title="Métriques"
    )

    fig.update_yaxes(title_text="Émissions Par Habitant", secondary_y=False)
    fig.update_yaxes(title_text="Pourcentage de Population Urbaine", secondary_y=True)

    return fig

# Afficher les graphiques
st.header("Empreintes de Feu")
st.write("""
Ce graphique montre la composition des différents types de feux (savane, forêt, sols organiques, forêts tropicales humides) au fil du temps pour chaque région. 
Il révèle des "empreintes de feu" uniques pour différentes régions, permettant d'identifier les tendances et les changements dans les modèles d'incendie.
""")
st.plotly_chart(create_fire_fingerprint_chart(df))

st.header("Flux Forestier")
st.write("""
Ce graphique visualise la conversion forestière nette par rapport aux changements de la zone forestière. 
Il permet d'identifier les régions qui connaissent une déforestation ou un reboisement, offrant des insights sur la gestion forestière et les changements environnementaux.
""")
st.plotly_chart(create_forest_flux_chart(df))

st.header("Chronologie de la Modernisation Agricole")
st.write("""
Ce graphique multi-lignes montre les tendances des émissions agricoles traditionnelles (par exemple, le fumier laissé sur les pâturages) par rapport aux émissions agricoles modernes (par exemple, la fabrication d'engrais et de pesticides) au fil du temps. 
Il illustre la transition des pratiques agricoles et son impact sur les émissions.
""")
st.plotly_chart(create_agricultural_modernization_chart(df))

st.header("Évolution des Émissions Par Habitant")
st.write("""
Ce graphique suit l'évolution des émissions par personne à mesure que les régions passent d'une population majoritairement rurale à une population urbaine. 
Il permet d'explorer la relation entre l'urbanisation et les émissions par habitant dans différentes régions.
""")
st.plotly_chart(create_emissions_per_capita_chart(df))

st.write("""
### Conclusion

Ces visualisations offrent un aperçu approfondi des tendances en matière d'émissions, d'utilisation des terres et de démographie dans différentes régions. 
Elles mettent en lumière les défis complexes liés au changement climatique, à la gestion des forêts et à la modernisation agricole. 
En explorant ces données, nous pouvons mieux comprendre les interactions entre les activités humaines et l'environnement, et potentiellement identifier des stratégies pour un développement plus durable.
""")