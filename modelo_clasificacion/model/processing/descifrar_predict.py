import numpy as np
from model.config.core import config
import pandas as pd 


def keep_first_one(row):
    found_first_one = False
    for i, value in enumerate(row):
        if value == 1 and not found_first_one:
            found_first_one = True
        else:
            row.iat[i] = 0
    return row



def decrypt_preds(predicciones,clases = config.app_config.target):
    df = pd.DataFrame(predicciones,columns=clases)
    
    df = df.apply(keep_first_one, axis=1)

    df = pd.from_dummies(df).rename(columns={'':'CALIF'})
    df['CALIF'] = df['CALIF'].str.replace('CALIFICACION_', '').str.strip()

    records = df['CALIF'].to_list()
    print(records)
    return records

