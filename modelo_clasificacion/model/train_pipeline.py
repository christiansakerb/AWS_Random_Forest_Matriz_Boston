import numpy as np
from config.core import config
import pandas as pd
from pipeline import matriz_pipeline
from imblearn.over_sampling import SMOTE
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


def run_training() -> None:
    """Train the model."""
    
    # read training data
    Ventas_Procesadas = load_dataset(file_name=config.app_config.data_train_test)

    Ventas_Procesadas['Semana de Fecha'] = Ventas_Procesadas['Semana de Fecha'].apply(lambda x: int(x[-2:]))
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

    Ventas_Procesadas = Ventas_Procesadas.dropna()

    Ventas_Procesadas = pd.get_dummies(Ventas_Procesadas,columns=['FECHA ASIGNADO','CATEGORIA','LINEA'],drop_first=True,dtype=float)
    Ventas_Procesadas = pd.get_dummies(Ventas_Procesadas,columns=['CALIFICACION'],dtype=float)

    X =Ventas_Procesadas[config.model_config.features]
    y = Ventas_Procesadas[config.model_config.target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.model_config.test_size, random_state=42)

    sm = SMOTE()  #Smote con parámetros por default
    smote = SMOTE(random_state=42)

    X_train_resampled, y_train_resampled = smote.fit_resample(X_train.to_numpy(), y_train.to_numpy())

    # fit model
    matriz_pipeline.fit(X_train_resampled, y_train_resampled,random_state = config.model_config.random_state)

    # persist trained model
    save_pipeline(pipeline_to_persist=matriz_pipeline)


if __name__ == "__main__":
    run_training()
