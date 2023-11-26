from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

from model.config.core import config
## PIPELINE COMPLETO
print(config.model_config.max_features)
matriz_pipeline = Pipeline([("Random Forest",MultiOutputClassifier(
    RandomForestClassifier(max_features=config.model_config.max_features,
                           n_estimators=config.model_config.n_estimators,
                           random_state=config.model_config.random_state,)),),])
