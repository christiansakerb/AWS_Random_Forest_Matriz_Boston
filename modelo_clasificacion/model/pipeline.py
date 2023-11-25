from feature_engine.selection import DropFeatures
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier

from model.config.core import config
from model.processing import features as pp

abandono_pipe = Pipeline(
    [
        # Drop features 
        #("drop_features", 
        # DropFeatures(
        #     features_to_drop=[config.model_config.temp_features]
        #     )
        #),
        # Mappers
        #(
        #    "mapper_qual",
        #    pp.Mapper(
        #        variables=config.model_config.qual_vars,
        #        mappings=config.model_config.qual_mappings,
        #    ),
        #),
        # Scaler
        ("scaler", MinMaxScaler()
         ),
        # Random forest 
        ("Random Forest",
            RandomForestClassifier(
                n_estimators = config.model_config.n_estimators, 
                max_depth = config.model_config.max_depth,
                random_state=config.model_config.random_state,
            ),
        ),
    ]
)
