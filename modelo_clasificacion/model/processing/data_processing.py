from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from model.config.core import config


#REVISION
def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""
    
    #Selección de variables de interes
    Ventas_Procesadas = input_data[config.model_config.features].copy()
    
    Ventas_Procesadas['Semana de Fecha'] = Ventas_Procesadas['Semana de Fecha'].apply(lambda x: int(x[-2:]))
    #Preprocesamiento semanas
    Ventas_Procesadas = Ventas_Procesadas.sort_values(by='Semana de Fecha',ascending=True)
    Ventas_Procesadas.head()
    Diccionario_semanas_transformacion = {}
    for mes in Ventas_Procesadas['FECHA ASIGNADO'].unique():
        Auxiliar = Ventas_Procesadas[Ventas_Procesadas['FECHA ASIGNADO']==mes]
        Semanas = Auxiliar['Semana de Fecha'].unique()
        Semana_nueva = np.arange(0,Semanas.shape[0],1)
        for indice in Semana_nueva:
            Diccionario_semanas_transformacion[Semanas[indice]]=Semana_nueva[indice]+1
    Ventas_Procesadas['Semana de Fecha'] = Ventas_Procesadas['Semana de Fecha'].apply(lambda x: Diccionario_semanas_transformacion[x])
    #eliminación de nulos
    Ventas_Procesadas = Ventas_Procesadas.dropna()
    #Codificación One-HOT     #Selección de variables de interes

    X = pd.get_dummies(Ventas_Procesadas,columns=['FECHA ASIGNADO','CATEGORIA','LINEA'],drop_first=True,dtype=float)

    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleDataInputs(
            inputs=X.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return X, errors
#
#aqui se debe revisar si hay un problema con las comillas..
class DataInputSchema(BaseModel):
  "FECHA ASIGNADO": Optional[int]
  "Semana de Fecha": Optional[int]
  CONTRIBUCION: Optional[float]
  "ORDENES DE PEDIDO": Optional[float]
  "UNIDADES VENDIDAS": Optional[float]
  "CONTRIBUCION-2": Optional[float]
  "ORDENES DE PEDIDO-2": Optional[float]
  "UNIDADES VENDIDAS-2": Optional[float]
  "CONTRIBUCION-3": Optional[float]
  "ORDENES DE PEDIDO-3": Optional[float]
  "UNIDADES VENDIDAS-3": Optional[float]
  CATEGORIA: Optional[int]
  LINEA: Optional[int]
  CALIFICACION: Optional[int]


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]
