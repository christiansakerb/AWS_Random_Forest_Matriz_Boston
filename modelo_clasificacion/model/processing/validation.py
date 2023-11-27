from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from model.config.core import config

#PENDIENTE
def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.model_config.features
        if validated_data[var].isnull().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data
#

#REVISION
def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""
    
    relevant_data = input_data[config.model_config.features].copy()
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors
#
class DataInputSchema(BaseModel):
    CODIGO: Optional[str]
    FECHA_ASIGNADO: Optional[str]
    Semana_de_Fecha: Optional[int]
    CONTRIBUCION: Optional[float]
    ORDENES_DE_PEDIDO: Optional[float]
    UNIDADES_VENDIDAS: Optional[float]


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]
