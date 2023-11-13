import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore", category=FutureWarning)
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier

experiment = mlflow.set_experiment("sklearn-matriz")

Clasificacion = pd.read_excel('Data.xlsx',sheet_name='Datos')
Ventas_cerrado = pd.read_excel('Data.xlsx',sheet_name='Datos mes cerrados')
Ventas_semanales = pd.read_excel('Data.xlsx',sheet_name='Datos_mes_dia')

Ventas_Procesadas = Ventas_semanales.merge(Ventas_cerrado,how='left',on=['FECHA ASIGNADO','CODIGO'])
Ventas_Procesadas = Ventas_Procesadas.merge(Clasificacion,how='left',on=['FECHA ASIGNADO','CODIGO'])
Ventas_Procesadas.set_index('CODIGO',inplace=True)
Ventas_Procesadas.drop(columns='FECHA',inplace=True)
Ventas_Procesadas.head()

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

X =Ventas_Procesadas.iloc[:,:-4]
y = Ventas_Procesadas.iloc[:,-4:]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

sm = SMOTE()  #Smote con parámetros por default
smote = SMOTE(random_state=42)

X_train_resampled, y_train_resampled = smote.fit_resample(X_train.to_numpy(), y_train.to_numpy())



# Hacer predicciones

with mlflow.start_run(experiment_id=experiment.experiment_id):
    # defina los parámetros del modelo
    n_estimators = 200 
    max_depth = 6
    max_features = 4
    # Cree el modelo con los parámetros definidos y entrénelo
    boosting = MultiOutputClassifier(GradientBoostingClassifier())

    # Entrena el modelo
    boosting.fit(X_train_resampled, y_train_resampled)

    y_pred = boosting.predict(X_test.to_numpy())

    # Calcular la precisión
    accuracy = accuracy_score(y_test.to_numpy(), y_pred)
    print(f'Precisión: {accuracy}')

    # Realice predicciones de prueba
    y_pred = boosting.predict(X_test.to_numpy())
  
    # Registre los parámetros
    mlflow.log_param("num_trees", n_estimators)
    mlflow.log_param("maxdepth", max_depth)
    mlflow.log_param("max_feat", max_features)
  
    # Registre el modelo
    mlflow.sklearn.log_model(boosting, "Gradient-Boosting-model")
  
    # Cree y registre la métrica de interés
    accuracy = accuracy_score(y_test.to_numpy(), y_pred)

    mlflow.log_metric("accuracy", accuracy)
    print(accuracy)