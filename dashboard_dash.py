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
    html.H2(children='Filtros', style={'textAlign':'center'}),
    html.Hr(),
    html.Div([
    html.P("Selecciona aquí la clasificación que quieres ver:",
           style={'textAlign': 'center', 'margin-bottom': '10px'}),
    dcc.Dropdown(df.CALIFICACION.unique(), 
                 'ESTRELLA', 
                 id='dropdown-selection',
                 style={'width': '50%'}),
    html.P("Selecciona aquí la Métrica que quieres analizar:",
           style={'textAlign': 'center', 'margin-bottom': '10px'}),
    dcc.Dropdown(['CONTRIBUCION','ORDENES DE PEDIDO','UNIDADES VENDIDAS'], 
                 'CONTRIBUCION', 
                 id='dropdown-selection_2',
                 style={'width': '50%'})
    ],style={'display': 'flex'}),
    html.H2(children='Gráficos', style={'textAlign':'center'}),
     html.Div([
        dcc.Graph(id='graph-content1',style={'width': '33.33%'}),
        dcc.Graph(id='graph-content2',style={'width': '33.33%'}),
        dcc.Graph(id='graph-content3',style={'width': '33.33%'})
    ], style={'display': 'flex'}),
    html.H2(children='Tabla de detalle por Productos', style={'textAlign':'center'}),
    html.Hr(),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)

])

#La función actualizará update_graph cuando cambie dropdown-selection
#Retornará un gráfico que se llamará graph-content
@callback(
    Output('graph-content1', 'figure'),
    Output('graph-content2', 'figure'),
    Output('graph-content3', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('dropdown-selection_2', 'value')
)
def update_graph(value,value_2):
    dff = df[df['CALIFICACION']==value].groupby('Semana de Fecha').sum().reset_index()
    df_clasificacion = df.groupby('CALIFICACION').sum().reset_index()
    df_productos = df.groupby('CODIGO').sum().reset_index().sort_values(by=value_2)
    df_meses = df.groupby('FECHA_ASIGNADO').sum().reset_index().sort_values(by='FECHA_ASIGNADO')

    figure1 = px.pie(df_clasificacion, names='CALIFICACION', values=value_2, title='Distribución de Calificaciones')
    figure2 = px.bar(df_productos.head(15), x=value_2, y='CODIGO',orientation='h', text=value_2,title='Ventas por Producto')
    figure3 = px.bar(df_meses, x='FECHA_ASIGNADO', y=value_2,text=value_2, title='Datos por meses')
    return figure1,figure2,figure3

if __name__ == '__main__':
    app.run(debug=True)