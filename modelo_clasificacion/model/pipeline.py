from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

from config.core import config
## PIPELINE COMPLETO

matriz_pipeline = Pipeline([("Random Forest",MultiOutputClassifier(
    RandomForestClassifier(max_features=config.app_config.max_features,
                           n_estimators=config.app_config.n_estimators,
                           random_state=config.app_config.random_state,)),),])
