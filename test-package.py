import pandas as pd
from model.predict import make_prediction

sample_input_data = pd.DataFrame({'CODIGO':['X712','X712','X564','X537','X289'],
'FECHA ASIGNADO':['2023-10','2023-11','2023-08','2023-11','2023-09'],
'Semana de Fecha':[30,31,29,30,29],
'CONTRIBUCION':[0.103511,0.3033,0.107,0.1035,0.3033],
'ORDENES DE PEDIDO':[0.001848,0.4503,0.0055,0.000,0.0055],
'UNIDADES VENDIDAS':[0.004396,0.9,0.0065,0.004,00.6]})
sample_input_data.set_index('CODIGO',inplace=True)

result = make_prediction(input_data=sample_input_data)
print(result)