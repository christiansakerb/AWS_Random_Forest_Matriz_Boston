import typing as t

import numpy as np
import pandas as pd

from model import __version__ as _version #OK 
from model.config.core import config #OK - 80%
from model.processing.data_manager import load_pipeline #OK
from model.processing.data_processing import validate_inputs
from model.processing.descifrar_predict import decrypt_preds

#Este paso carga el archivo de joblib .pkl almacenado despues del entrenamiento
pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
modelo_matriz_clasif = load_pipeline(file_name=pipeline_file_name)

#Este paso crea la función que hace la predicción
def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    #Validate_inputs revisa que la información esté en el formato correcto
    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version, "errors": errors}


    if not errors:
        predictions = modelo_matriz_clasif.predict(
            validated_data[config.app_config.features].to_numpy()
        )
        predictions = decrypt_preds(predictions,clases = config.app_config.target)
        results = {
            "predictions": [pred for pred in predictions], 
            "version": _version,
            "errors": errors,
        }
    print(results)
    return results

#make_prediction(input_data = 
#                {'CODIGO':['X712','X712'],
#                              'FECHA ASIGNADO':['2023-10','2023-11'],
#                              'Semana de Fecha':[30,31],
#                              'CONTRIBUCION':[0.103511,0.3033],
#                              'ORDENES DE PEDIDO':[0.001848,0.4503],
#                              'UNIDADES VENDIDAS':[0.004396,0.9]})