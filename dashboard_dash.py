from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

#define el diseño de la aplicacion 
#H1 es un encabezado y su titulo, además se define estilo y centrado
#Dropwdown es una lista desplegable, se define valor incial
#Graph es un grafico, en este caso cambiante según callback
app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

#La función actualizará update_graph cuando cambie dropdown-selection
#Retornará un gráfico que se llamará graph-content
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)