from typing import Any, List, Optional
from pydantic import BaseModel

# Esquema de los resultados de predicción
class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[float]]

# Esquema para inputs múltiples
class MultipleDataInputs(BaseModel):
    CODIGO: Optional[str]
    FECHA_ASIGNADO: Optional[str]
    Semana_de_Fecha: Optional[int]
    CONTRIBUCION: Optional[float]
    ORDENES_DE_PEDIDO: Optional[float]
        
    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "CODIGO": "X712",
                        "FECHA ASIGNADO": "2023-10",
                        "Semana de Fecha": 30,
                        "CONTRIBUCION": 0.103511,
                        "ORDENES DE PEDIDO": 0.001848,
                        "UNIDADES VENDIDAS": 0.004396
                    }
                ]
            }
        }


#make_prediction(input_data = 
#                {'CODIGO':['X712','X712'],
#                              'FECHA ASIGNADO':['2023-10','2023-11'],
#                              'Semana de Fecha':[30,31],
#                              'CONTRIBUCION':[0.103511,0.3033],
#                              'ORDENES DE PEDIDO':[0.001848,0.4503],
#                              'UNIDADES VENDIDAS':[0.004396,0.9]})