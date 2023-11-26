import numpy as np
from model.config.core import config
import pandas as pd 

def decrypt_preds(predicciones,clases = config.app_config.target):
    df = pd.DataFrame(predicciones,columns=clases)
    df = pd.from_dummies(df).rename(columns={'':'CALIF'})
    df['CALIF'] = df['CALIF'].str.replace('CALIFICACION_', '').str.strip()

    records = df['CALIF'].to_list()
    return records

#    for col in config.app_config.target:
#        columna_verdadera = predicciones[:,1]