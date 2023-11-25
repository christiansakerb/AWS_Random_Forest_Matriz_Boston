
#En el archivo de data-manager se guarda toda la configuracion de como se hace:
#-- Carga de archivos para entrenamiento o muestra en tablero
#-- Carga y guardado de modelos
#-- etc.. lo que se ocurra

import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from model import __version__ as _version
from model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config

#Cargamos el dataframe , en este caso nos servirá para llamar Data.xlsx a
#a la función que preprocesa los datos


######ESTA FUNCIÓN SE LLAMA EN ??????????
def load_dataset(*, file_name: str) -> pd.DataFrame:
    #El cambio aquí corresponnde a que son 3 cargas, tal como está en notebook.
    
    Clasificacion = pd.read_excel(Path(f"{DATASET_DIR}/{file_name}"),sheet_name='Datos')
    Ventas_cerrado = pd.read_excel(Path(f"{DATASET_DIR}/{file_name}"),sheet_name='Datos mes cerrados')
    Ventas_semanales = pd.read_excel(Path(f"{DATASET_DIR}/{file_name}"),sheet_name='Datos_mes_dia')

    #Hacemos algo de procesamiento para cargar ya la data en un solo df
    Ventas_Procesadas = Ventas_semanales.merge(Ventas_cerrado,how='left',on=['FECHA ASIGNADO','CODIGO'])
    Ventas_Procesadas = Ventas_Procesadas.merge(Clasificacion,how='left',on=['FECHA ASIGNADO','CODIGO'])
    Ventas_Procesadas.set_index('CODIGO',inplace=True)
    Ventas_Procesadas.drop(columns='FECHA',inplace=True)
    Ventas_Procesadas.head()

    return Ventas_Procesadas

#Hasta aquí está ajustada

#### ESTA FUNCIÓN SE LLAMA EN ????????????????????
def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """Persist the pipeline.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name

    #Guardamos el nombre que llevará el modelo en joblib
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


#### ESTA FUNCIÓN SE LLAMA EN **PREDICT.py**
def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model

#### ESTA FUNCIÓN SE LLAMA AQUI EN SAVE_PIPELINE
def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
