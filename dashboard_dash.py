from dash import Dash, html, dcc, callback, Output, Input,dash_table,State
import dash
import plotly.express as px
import pandas as pd
from loguru import logger
import requests
import json

import os


df = pd.read_csv('Archivo_para_tabler.csv')
estilos_titulos = {'textAlign':'center', 'color': 'white','fontWeight': 'bold','border': 'white'}
app = Dash(__name__)

condition = [
    {
        'if': {
            'filter_query': '{CUADRANTE_NUEVO} != {CALIFICACION}'
        },
        'backgroundColor': 'red'
    }
]


api_url = os.getenv('API_URL')
api_url = "http://{}:8001/api/v1/predict".format(api_url)


#define el diseño de la aplicacion 
#H1 es un encabezado y su titulo, además se define estilo y centrado
#Dropwdown es una lista desplegable, se define valor incial
#Graph es un grafico, en este caso cambiante según callback
app.layout = html.Div([
        html.H1(children='Dashboard Ciclo de Vida de Productos', style=estilos_titulos),
    html.Hr(),
        html.H2(children='Filtros', style={'textAlign':'center', 'color': 'white','fontWeight': 'bold'}),
    html.Div([   
    
        html.P("clasificación:    ",style={'textAlign': 'center', 'margin-bottom': '5px'}),       
        dcc.Dropdown(list(df['CALIFICACION'].unique()), 'ESTRELLA', id='dropdown-selection',style={'width': '50%'}),
        
        html.P("Métrica  :",style={'textAlign': 'center', 'margin-bottom': '10px'}),
        dcc.Dropdown(['CONTRIBUCION','ORDENES DE PEDIDO','UNIDADES VENDIDAS'], 'CONTRIBUCION', id='dropdown-selection_2',style={'width': '50%'})
    
    ],style={'display': 'flex'}),
    
    html.Hr(),
        html.H2(children='Gráficos', style=estilos_titulos),
    
    html.Div([
        html.Div([
            dcc.Graph(id='graph-content1',style={'width': '100%','backgroundColor': '#1EAEDB', 'color': 'white'}),
            html.P("El gráfico de torta de DISTRIBUCIÓN DE CALIFICACIONES representa la participación de la métrica seleccionada por cuadrante de la matriz",style={'textAlign': 'left', 'margin-bottom': '10px'})
        ],style={'width': '33.33%','border': '#1EAEDB'}),

        html.Div([
            dcc.Graph(id='graph-content2',style={'width': '100%','backgroundColor': '#1EAEDB', 'color': 'white'}),
            html.P("El gráfico de barras de VENTAS POR PRODUCTOS muestra datos de los 15 productos con mayor valor en la métrica seleccionada ",style={'textAlign': 'left', 'margin-bottom': '10px'})
        ],style={'width': '33.33%','border': '#1EAEDB'}),

        html.Div([
            dcc.Graph(id='graph-content3',style={'width': '100%','backgroundColor': '#1EAEDB', 'color': 'white'}),
            html.P("El gráfico de barras de DATOS POR MESES muestra la tendencia por mes de la métrica seleccionada",style={'textAlign': 'left', 'margin-bottom': '10px'})
        ],style={'width': '33.33%','border': '#1EAEDB'}),
    
    ], style={'display': 'flex','border': '#1EAEDB'}),
    
    html.Hr(),
        html.H2(children='Tabla de detalle por Productos', style=estilos_titulos),
    html.Hr(),
    
    html.Div([
    
        dash_table.DataTable(data=df.to_dict('records'), page_size=15,style_table={'margin-right': '50px'},style_data_conditional=condition),

        html.Div([
            html.P("Predice en que cuadrante estará el producto el próximo mes",style={'textAlign': 'center','width': '100%','color': 'black','fontWeight': 'bold'}),

            html.Div([
                html.P("Codigo:",style={'textAlign': 'center','left': '100%'}),
                dcc.Dropdown(list(df['CODIGO'].unique()), 'X429', id='dropdown-cod',style={'width': '100%','color':'black'}),
            ], style={'display': 'flex'}),

            html.Div([
                html.P("Fecha para estimación:",style={'textAlign': 'left','width': '100%'}),
                dcc.Dropdown(list(df['FECHA_ASIGNADO'].unique()), '2023-08', id='dropdown-fecha',style={'width': '100%','color':'black'}),
            ], style={'display': 'flex'}),

            html.Div([
                html.P("Semana en el año:",style={'textAlign': 'left','width': '100%'}),
                dcc.Dropdown([23,24,25,26,27,28,29,30], 28, id='dropdown-semana',style={'width': '100%','color':'black'}),
            ], style={'display': 'flex'}),

            html.Div([
                html.P("Contribución:",style={'textAlign': 'left','width': '100%'}),
                dcc.Input(id='input_c', value=0.1063834821329253,type='number',step=0.05,min=0,max=1, style={'width': '100%'})
            ], style={'display': 'flex'}),

            html.Div([
                html.P("Unidades:",style={'textAlign': 'left','width': '100%'}),
                dcc.Input(id='input_u', value=0.1063834821329253,type='number',step=0.05,min=0,max=1, style={'width': '100%'})
            ], style={'display': 'flex'}),

            html.Div([
                html.P("Ordenes de Pedido:",style={'textAlign': 'left','width': '100%'}),
                dcc.Input(id='input_o', value=0.1063834821329253,type='number',step=0.05,min=0,max=1, style={'width': '100%'})
            ], style={'display': 'flex'}),

            html.Hr(),
            html.Button('Predecir Cuadrante Nuevo', id='calcular-btn', n_clicks=0,style={'width':'100%'}),
            html.Hr(),

            html.H6(html.Div(id='resultado'),style={'fontSize': 15})
            ], style={'backgroundColor': '#1EAEDB', 'color': 'white'}),
        ], style={'display': 'flex'})    

], style={'backgroundColor': 'lightblue', 'font-family': "Times New Roman"})  # Cambia el color de fondo de la página web

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
    if value =='':
        dff = df
    else:
        dff = df[df['CALIFICACION']==value]

    df_clasificacion = df.groupby('CALIFICACION').sum().reset_index()
    df_productos = dff.groupby('CODIGO').sum().reset_index().sort_values(by=value_2)
    df_meses = dff.groupby('FECHA_ASIGNADO').sum().reset_index().sort_values(by='FECHA_ASIGNADO')

    figure1 = px.pie(df_clasificacion, names='CALIFICACION', values=value_2, title='Distribución de Calificaciones')
    figure2 = px.bar(df_productos.head(15), x=value_2, y='CODIGO',orientation='h', text=value_2,title='Ventas por Producto')
    figure3 = px.bar(df_meses, x='FECHA_ASIGNADO', y=value_2,text=value_2, title='Datos por meses')
    return figure1,figure2,figure3

@app.callback(
    [Output(component_id='resultado', component_property='children'),
    Output('calcular-btn', 'n_clicks')],
    [Input(component_id='calcular-btn', component_property='n_clicks')],
    [State(component_id='dropdown-cod', component_property='value'), 
     State(component_id='dropdown-fecha', component_property='value'), 
     State(component_id='dropdown-semana', component_property='value'), 
     State(component_id='input_c', component_property='value'),
     State(component_id='input_u', component_property='value'),
     State(component_id='input_o', component_property='value')]
)
def update_output_div(n_clicks,CODIGO, FECHA_ASIGNADO, Semana_de_Fecha, CONTRIBUCION, ORDENES_DE_PEDIDO,UNIDADES_VENDIDAS):

    if n_clicks is None:
        return dash.no_update, 0  # No actualizar si no se ha hecho clic

    myreq = {
        "inputs": [
            {
                "CODIGO": CODIGO,
                "FECHA_ASIGNADO": FECHA_ASIGNADO,
                "Semana_de_Fecha": Semana_de_Fecha,
                "CONTRIBUCION": CONTRIBUCION,
                "ORDENES_DE_PEDIDO": ORDENES_DE_PEDIDO,
                "UNIDADES_VENDIDAS": UNIDADES_VENDIDAS
            }
        ]
      }
    headers =  {"Content-Type":"application/json", "accept": "application/json"}

    # POST call to the API
    response = requests.post(api_url, data=json.dumps(myreq), headers=headers)
    data = response.json()
    logger.info("Response: {}".format(data))

    # Pick result to return from json format
    result = 'Clasificación predicha -> ' + data["predictions"][0]
    
    return result ,0


if __name__ == '__main__':
    app.run(debug=True)