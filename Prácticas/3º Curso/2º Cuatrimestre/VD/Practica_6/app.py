import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.express.colors import qualitative

# Dataset de ejemplo
df = px.data.gapminder()

# Clasificación por región cultural/geográfica
def clasificar_region(row):
    if row['continent'] == 'Europe': 
        if row['country'] in ['France', 'Italy', 'Spain', 'Portugal', 'Romania']:
            return 'Europa Latina'
        elif row['country'] in ['Germany', 'Austria', 'Switzerland', 'Netherlandas', 'Belgium', 'United Kingdom', 'Ireland', 'Norway', 'Sweden', 'Denmark']:
            return "Europa Germánica"
        elif row['country'] in ['Poland', 'Czech Republic', 'Slovakia', 'Bulgaria', 'Russia', 'Ukraine', 'Belarus']:
            return 'Europa del Este'
        elif row['country'] in ['Greece', 'Albania', 'Serbia', 'Croatia', 'Bosnia and Herzegovina', "North Macedonia", "Montenegro", "Slovenia"]:
            return "Balcanes"
        else:
            return 'Otros'
    elif row["continent"] == "Americas":
            if row["country"] in ["Mexico", "Argentina", "Colombia", "Chile", "Peru", "Venezuela", "Ecuador", "Bolivia", "Paraguay", "Uruguay"]:
                return "Latinoamérica Hispana"
            elif row["country"] == "Brazil":
                return "Brasil"
            elif row["country"] in ["United States", "Canada"]:
                return "América Anglosajona"
            else:
                return "Caribe"
    elif row["continent"] == "Asia":
        if row["country"] in ["Turkey", "Israel", "Saudi Arabia", "Iran", "Iraq", "Jordan", "Syria", "Lebanon", "Yemen", "Oman", "Qatar", "United Arab Emirates", "Bahrain", "Kuwait"]:
            return "Asia Occidental"
        elif row["country"] in ["Kazakhstan", "Uzbekistan", "Turkmenistan", "Kyrgyzstan", "Tajikistan"]:
            return "Asia Central"
        elif row["country"] in ["China", "Japan", "South Korea", "North Korea", "Mongolia", "Taiwan"]:
            return "Asia Oriental"
        elif row["country"] in ["India", "Pakistan", "Bangladesh", "Sri Lanka", "Nepal", "Bhutan", "Maldives"]:
            return "Asia del Sur"
        elif row["country"] in ["Thailand", "Vietnam", "Indonesia", "Malaysia", "Philippines", "Singapore", "Myanmar", "Cambodia", "Laos", "Brunei", "Timor-Leste"]:
            return "Asia Sudoriental"
        else:
            return "Otros"
    else:
        return row["continent"]

df['region_custom'] = df.apply(clasificar_region, axis=1)

# Inicializar la app con un tema de Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de la app
app.layout = dbc.Container([
    html.H1("Dashboard Interactivo con Dash y Plotly", className="my-4", style={"textAlign": "center"}),

    html.P("En este gráfico interactivo se exploran los datos del dataset Gapminder permitiendo filtrar los datos por continente, regiones de países y los diferentes indicadores económicos y sociales, como el PIB per cápita, la esperanza de vida y la población. El gráfico de líneas muestra la evolución de cada país a lo largo de los años y el mapa representa de forma visual los países que se encuentran en la región seleccionada."),

    dbc.Row([
        dbc.Col([
            html.Label("Selecciona un continente:"),
            dcc.Dropdown(
                id="continente-dropdown",
                options=[{"label": c, "value": c} for c in df["continent"].unique()],
                value="Europe"
            )
        ], width=4),
        dbc.Col([
            html.Label('Selecciona una región:'),
            dcc.Dropdown(id='region-dropdown', value='Europa Latina', multi=False)
        ], width=4),
        dbc.Col([
            html.Label("Selecciona un dato:"),
            dcc.Dropdown(
                id="dato-dropdown",
                options=[
                    {"label": "PBI per Capita", "value": "gdpPercap"},
                    {"label": "Esperanza de vida", "value": "lifeExp"},
                    {"label": "Población", "value": "pop"}
                ],
                value="pop"
            )
        ], width=4)
    ]),

    html.Hr(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='mapa-paises')
        ], width=4),
        dbc.Col([
            dcc.Graph(id="grafico-pais")
        ], width=8)
    ])
], fluid=True)

# Callback para actualizar opciones de región
@app.callback(
    Output('region-dropdown', 'options'),
    Input('continente-dropdown', 'value')
)
def update_region_options(continente):
    regiones = df[df['continent'] == continente]['region_custom'].unique()
    return [{'label': r, 'value': r} for r in sorted(regiones)]

# Callback para seleccionar región por defecto
@app.callback(
    Output('region-dropdown', 'value'),
    Input('region-dropdown', 'options')
)
def set_default_region(options):
    return options[0]['value'] if options else None

@app.callback(
    Output('grafico-pais', 'figure'),
    Output('mapa-paises', 'figure'),
    [Input('continente-dropdown', 'value'),
     Input('region-dropdown', 'value'),
     Input('dato-dropdown', 'value')]
)
def update_graph_and_map(continent, region, dato):
    filtered_df = df[(df['continent'] == continent) & (df["region_custom"] == region)]

    # Asignar colores por país
    paises = sorted(filtered_df["country"].unique())
    colores = qualitative.Plotly
    color_map = {pais: colores[i % len(colores)] for i, pais, in enumerate(paises)}

    # Gráfico de líneas
    fig_lineas = go.Figure()
    for pais in paises:
        df_pais = filtered_df[filtered_df["country"] == pais]
        fig_lineas.add_trace(go.Scatter(
            x=df_pais['year'],
            y=df_pais[dato],
            mode='lines+markers',
            name=pais,
            line=dict(color=color_map[pais])
        ))
    fig_lineas.update_layout(title=f"Progresión de {dato} en {region}", xaxis_title='Año', yaxis_title=dato)

    # Mapa con zoom al continente
    latest_year = df['year'].max()
    df_mapa = filtered_df[filtered_df['year'] == latest_year]

    fig_mapa = go.Figure()
    for _, row in df_mapa.iterrows():
        fig_mapa.add_trace(go.Choropleth(
            locations=[row['country']],
            locationmode='country names',
            z=[1], # Valor dummy
            showscale=False,
            marker=dict(line=dict(color='white', width=0.5)),
            name=row['country'],
            colorscale=[[0, color_map[row['country']]], [1, color_map[row['country']]]]
        ))

    # Zoom automático por continente 
    scope_dict = {
        'Europe': "europe",
        "Asia": "asia",
        "Africa": "africa",
        "Americas": "world",
        "Oceania": "world"
    }
    fig_mapa.update_geos(scope=scope_dict.get(continent, 'world'))

    fig_mapa.update_layout(
        title=f"{dato} en {region} ({latest_year})",
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig_lineas, fig_mapa

if __name__ == "__main__":
    app.run(debug=True)
