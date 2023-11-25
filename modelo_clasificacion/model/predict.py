import typing as t

import numpy as np
import pandas as pd

from model import __version__ as _version #OK 
from model.config.core import config #OK - 80%
from model.processing.data_manager import load_pipeline #OK
from model.processing.data_processing import validate_inputs #PENDIENTE

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
            X=validated_data[config.model_config.features]
        )
        results = {
            "predictions": [pred for pred in predictions], 
            "version": _version,
            "errors": errors,
        }

    return results
