from typing import Any, List, Optional
from pydantic import BaseModel
from model.processing.validation import DataInputSchema

# Esquema de los resultados de predicción
class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[str]]

# Esquema para inputs múltiples
class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]


        
    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "CODIGO": "X712",
                        "FECHA_ASIGNADO": "2023-10",
                        "Semana_de_Fecha": 30,
                        "CONTRIBUCION": 0.103511,
                        "ORDENES_DE_PEDIDO": 0.001848,
                        "UNIDADES_VENDIDAS": 0.004396
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