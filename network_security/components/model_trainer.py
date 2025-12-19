from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from network_security.entity.config_entity import ModelTrainerConfig
import sys
import os
import numpy as np
from sklearn.metrics import accuracy_score
from network_security.utils.ml_utils.metric.classification_metric import get_classification_scores
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from network_security.utils.main_utils.utils import save_object, save_numpy_array_data, load_object, load_numpy_array_data
from network_security.utils.ml_utils.model.estimator import NetworkModel

SAVED_MODEL_DIR = "saved_models"
MODEL_FILE_NAME = "model.pkl"

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, x_train, y_train, x_test, y_test):
        models = {
            "RandomForest": RandomForestClassifier(),
            "AdaBoost": AdaBoostClassifier(),
            "GradientBoost": GradientBoostingClassifier(),
            "LogisticRegression": LogisticRegression(max_iter=1000),
            "DecisionTree": DecisionTreeClassifier(),
        }

        best_model = None
        best_score = 0.0

        for model_name, model in models.items():
            logging.info(f"Training model: {model_name}")
            model.fit(x_train, y_train)

            y_test_pred = model.predict(x_test)
            metric = get_classification_scores(y_true=y_test, y_pred=y_test_pred)

            logging.info(f"{model_name} F1 score: {metric.f1_score}")

            if metric.f1_score > best_score:
                best_model = model
                best_score = metric.f1_score

        return best_model

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("Loading transformed arrays")

            train_array = load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_array = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )
            preprocessor = load_object(
                self.data_transformation_artifact.transformed_object_file_path
            )

            x_train, y_train = train_array[:, :-1], train_array[:, -1]
            x_test, y_test = test_array[:, :-1], test_array[:, -1]

            model_config_file_path = os.path.join(
                self.model_trainer_config.model_trainer_dir,
                SAVED_MODEL_DIR,
                MODEL_FILE_NAME
            )

            os.makedirs(os.path.dirname(model_config_file_path), exist_ok=True)

            model = self.train_model(x_train, y_train, x_test, y_test)

            network_model = NetworkModel(
                preprocessor=preprocessor,
                model=model
            )

            save_object(model_config_file_path, network_model)

            train_metric = get_classification_scores(
                y_true=y_train,
                y_pred=network_model.predict(x_train)
            )
            test_metric = get_classification_scores(
                y_true=y_test,
                y_pred=network_model.predict(x_test)
            )

            return ModelTrainerArtifact(
                trained_model_file_path=model_config_file_path,
                train_metric_artifact=train_metric,
                test_metric_artifact=test_metric
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)
