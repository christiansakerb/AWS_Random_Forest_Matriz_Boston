from dash import Dash, html, dcc, callback, Output, Input,dash_table
import plotly.express as px
import pandas as pd

df = pd.read_csv('Archivo_para_tabler.csv')

app = Dash(__name__)

#define el diseño de la aplicacion 
#H1 es un encabezado y su titulo, además se define estilo y centrado
#Dropwdown es una lista desplegable, se define valor incial
#Graph es un grafico, en este caso cambiante según callback
app.layout = html.Div([
    html.H1(children='Dashboard Ciclo de Vida de Productos', style={'textAlign':'center'}),
    dcc.Dropdown(df.CALIFICACION.unique(), 'ESTRELLA', id='dropdown-selection'),
     html.Div([
        dcc.Graph(id='graph-content1'),
        dcc.Graph(id='graph-content2'),
    ], style={'display': 'flex'}),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)

])

#La función actualizará update_graph cuando cambie dropdown-selection
#Retornará un gráfico que se llamará graph-content
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.CALIFICACION==value].groupby('Semana de Fecha').sum().reset_index()
    
    figure1 = px.line(dff, x='Semana de Fecha', y='CONTRIBUCION', title='Graph 1')
    figure2 = px.line(dff, x='Semana de Fecha', y='CONTRIBUCION', title='Graph 2')

    return px.line(dff, x='Semana de Fecha', y='CONTRIBUCION')

if __name__ == '__main__':
    app.run(debug=True)