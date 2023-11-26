from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError
from pathlib import Path

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
    print(input_data,input_data.columns)
    errors = None

    return input_data,errors
#
#aqui se debe revisar si hay un problema con las comillas..


validate_inputs(input_data = 
                pd.DataFrame({'CODIGO':['X548'],
                              'FECHA ASIGNADO':['2023-11'],
                              'Semana de Fecha':[4],
                              'CONTRIBUCION':[0.8],
                              'ORDENES DE PEDIDO':[1],
                              'UNIDADES VENDIDAS':[1]}))