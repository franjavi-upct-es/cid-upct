import warnings
import datetime as dt
import pandas as pd
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# URLs y nombres de criptomonedas
urls = {
    "EOS": "https://www.cryptodatadownload.com/cdd/Bitfinex_EOSUSD_d.csv", 
    "EDO": "https://www.cryptodatadownload.com/cdd/Bitfinex_EDOUSD_d.csv",
    "BTC": "https://www.cryptodatadownload.com/cdd/Bitfinex_BTCUSD_d.csv",
    "ETH": "https://www.cryptodatadownload.com/cdd/Bitfinex_ETHUSD_d.csv",
    "LTC": "https://www.cryptodatadownload.com/cdd/Bitfinex_LTCUSD_d.csv",
    "BAT": "https://www.cryptodatadownload.com/cdd/Bitfinex_BATUSD_d.csv",
    "OMG": "https://www.cryptodatadownload.com/cdd/Bitfinex_OMGUSD_d.csv",
    "DAI": "https://www.cryptodatadownload.com/cdd/Bitfinex_DAIUSD_d.csv",
    "ETC": "https://www.cryptodatadownload.com/cdd/Bitfinex_ETCUSD_d.csv",
    "ETP": "https://www.cryptodatadownload.com/cdd/Bitfinex_ETPUSD_d.csv",
    "NEO": "https://www.cryptodatadownload.com/cdd/Bitfinex_NEOUSD_d.csv",
    "REP": "https://www.cryptodatadownload.com/cdd/Bitfinex_REPUSD_d.csv",
    "TRX": "https://www.cryptodatadownload.com/cdd/Bitfinex_TRXUSD_d.csv",
    "XLM": "https://www.cryptodatadownload.com/cdd/Bitfinex_XLMUSD_d.csv",
    "XMR": "https://www.cryptodatadownload.com/cdd/Bitfinex_XMRUSD_d.csv",
    "XVG": "https://www.cryptodatadownload.com/cdd/Bitfinex_XVGUSD_d.csv"
}
nombres_es = {
    "EOS": "EOS Coin (EOS)",
    "EDO": "Eidoo (EDO)",
    "BTC": "Bitcoin (BTC)",
    "ETH": "Ethereum (ETH)",
    "LTC": "Litecoin (LTC)",
    "BAT": "Basic Attention Token (BAT)",
    "OMG": "OmiseGO (OMG)",
    "DAI": "Dai (DAI)",
    "ETC": "Ethereum Classic (ETC)",
    "ETP": "Metaverse (ETP)",
    "NEO": "Neo (NEO)",
    "REP": "Augur (REP)",
    "TRX": "TRON (TRX)",
    "XLM": "Stellar (XLM)",
    "XMR": "Monero (XMR)",
    "XVG": "Verge (XVG)"
}

# Obtener fecha inicial a partir de Bitcoin
btc_df = pd.read_csv(urls["BTC"], header=1, parse_dates=["date"])
btc_df = btc_df.set_index("date")
btc_df = btc_df[~btc_df.index.duplicated(keep='first')]  # Evitar duplicados
btc_df.sort_index(inplace=True)

ventana_rsi = 14  # Ventana para el cálculo del RSI

fecha_inicio = btc_df.index.min()

def cargar_datos(urls, fecha_inicio, ventana):
    datos = {}
    fecha_inicio = pd.to_datetime(fecha_inicio)
    for sigla, url in urls.items():
        try:
            df = pd.read_csv(url, header=1, parse_dates=["date"])
            df = df.set_index("date")
            df = df[~df.index.duplicated(keep='first')]  # Eliminar fechas duplicadas
            df = df[['open','high','low','close','Volume USD']]
            df.sort_index(inplace=True)
            if fecha_inicio:
                df = df[df.index >= fecha_inicio]
            diff = df['close'].diff().dropna()
            ganancia = diff.where(diff > 0, 0.0)
            perdida = -diff.where(diff < 0, 0.0)
            media_g = ganancia.ewm(com=ventana-1, min_periods=ventana).mean()
            media_p = perdida.ewm(com=ventana-1, min_periods=ventana).mean()
            rs = media_g / media_p
            df['RSI'] = 100 - 100 / (1 + rs)
            datos[sigla] = df
        except Exception as e:
            print(f"Error al procesar {sigla}: {e}")
    return datos

datos_crypto = cargar_datos(urls, fecha_inicio, ventana_rsi)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard de Criptomonedas"

min_fecha = min(df.index.min() for df in datos_crypto.values())
max_fecha = dt.date.today()

filtros = dbc.Card([
    dbc.CardHeader(html.H5("Filtros y Exportación")),
    dbc.CardBody([
        html.Label("Seleccione criptomoneda:"),
        dcc.Dropdown(
            id='dropdown-criptomoneda',
            options=[{'label': nombres_es[k], 'value': k} for k in datos_crypto.keys()],
            value=list(datos_crypto.keys())[0]
        ),
        html.Br(),
        html.Label("Rango de fechas:"),
        dcc.DatePickerRange(
            id='selector-fechas',
            min_date_allowed=min_fecha,
            max_date_allowed=max_fecha,
            start_date=min_fecha,
            end_date=max_fecha
        ),
        html.Br(), html.Br(),
        dbc.Button("Exportar datos", id="btn-exportar", color="primary"),
        dcc.Download(id="descarga-datos")
    ])
])

area_graficos = dbc.Card([
    dbc.CardBody([
        dcc.Graph(id='grafico-velas'),
        dcc.Graph(id='grafico-precio')
    ])
])

app.layout = dbc.Container([
    html.H1("Dashboard Interactivo de Criptomonedas", className="text-center my-4"),
    dbc.Row([
        dbc.Col([filtros], width=12),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([area_graficos], width=12),
    ])
], fluid=True)

@app.callback(
    Output('grafico-velas','figure'),
    Output('grafico-precio','figure'),
    Input('dropdown-criptomoneda','value'),
    Input('selector-fechas','start_date'),
    Input('selector-fechas','end_date')
)
def actualizar_graficos(sigla, inicio, fin):
    inicio = pd.to_datetime(inicio)
    fin = pd.to_datetime(fin)
    df = datos_crypto[sigla].loc[inicio:fin]
    fig1 = go.Figure(go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close']))
    fig1.update_layout(title=f"Velas - {nombres_es[sigla]}")
    fig2 = go.Figure(go.Scatter(x=df.index, y=df['close'], mode='lines'))
    fig2.update_layout(title=f"Precio de Cierre - {nombres_es[sigla]}")
    return fig1, fig2

@app.callback(
    Output("descarga-datos","data"),
    Input("btn-exportar","n_clicks"),
    Input('dropdown-criptomoneda','value'),
    Input('selector-fechas','start_date'),
    Input('selector-fechas','end_date')
)
def exportar_csv(n, sigla, inicio, fin):
    if n:
        inicio = pd.to_datetime(inicio)
        fin = pd.to_datetime(fin)
        df = datos_crypto[sigla].loc[inicio:fin]
        return dcc.send_data_frame(df.to_csv, f"{sigla}_datos.csv")
    return None

if __name__ == '__main__':
    app.run(debug=True)