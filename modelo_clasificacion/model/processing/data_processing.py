from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError
from pathlib import Path
from model import __version__ as _version #OK 
from model.processing.data_manager import load_pipeline #OK

from model.config.core import config
from model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config

#FECHA DEBE SER LA FECHA AL QUE CORRESPONDE EL MES ACTUAL
def Traer_ventas_anteriores(df):
    Clasificacion = pd.read_excel(Path(f"{DATASET_DIR}/{config.app_config.data_train_test}"),sheet_name='Datos')
    Ventas_cerrado = pd.read_excel(Path(f"{DATASET_DIR}/{config.app_config.data_train_test}"),sheet_name='Datos mes cerrados')
    df = df.merge(Ventas_cerrado, how='left',on=['FECHA ASIGNADO','CODIGO'])
    return df.merge(Clasificacion,how='left',on=['FECHA ASIGNADO','CODIGO'])
    
#REVISION
def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""
    input_data.set_index('CODIGO',inplace=True)
    
    #Colocamos datos anteriores
    input_data = Traer_ventas_anteriores(input_data)

    Diccionario_semanas_transformacion = f"{config.app_config.pipeline_save_file_dict}{_version}.pkl"
    Diccionario_semanas_transformacion = load_pipeline(file_name=Diccionario_semanas_transformacion)

    input_data['Semana de Fecha'] = input_data['Semana de Fecha'].apply(lambda x: Diccionario_semanas_transformacion[x])
    #Asumimos que no va a haber faltantes en el código
    input_data.drop(columns='CALIFICACION',inplace=True)
    input_data = pd.get_dummies(input_data,columns=['FECHA ASIGNADO','CATEGORIA','LINEA'],dtype=float)
    #Ajuste para entrada al modelo
    for col in config.app_config.features:
    # Si la columna no existe en el DataFrame, la agrega con valores NaN
        if col not in input_data.columns:
            input_data[col] = 0
    input_data = input_data[config.app_config.features]


    print(input_data,input_data.columns)
    errors = None

    return input_data,errors
#
#aqui se debe revisar si hay un problema con las comillas..


validate_inputs(input_data = 
                pd.DataFrame({'CODIGO':['X548'],
                              'FECHA ASIGNADO':['2023-11'],
                              'Semana de Fecha':[24],
                              'CONTRIBUCION':[0.8],
                              'ORDENES DE PEDIDO':[1],
                              'UNIDADES VENDIDAS':[1]}))