"""File for AdaptProposalModel class"""
import base64
from io import BytesIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


class AdaptProposalModel:
    """Wrapper class for all functionalities related to
    training, predicting and visualizing the decision tree"""

    @staticmethod
    def __train_random_forest(drivers_data):
        """
        trains RandomForestClassifier using the generated data
        :param drivers_data: dataframe with prepared generated driver data
        :return: trained model and used encoders
        """
        # Convert Object values to Integers
        categorical_columns = drivers_data.select_dtypes(include=['object']).columns
        label_encoders = {}
        for column in categorical_columns:
            label_encoders[column] = LabelEncoder()
            drivers_data[column] = label_encoders[column].fit_transform(drivers_data[column])

        X = drivers_data.drop(columns=['car'])
        y = drivers_data['car']

        # Split data into training and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=45)

        random_forest = RandomForestClassifier(random_state=6345)
        random_forest.fit(X_train.values, y_train)

        # Evaluate accuracy
        y_pred_random_forest = random_forest.predict(X_test.values)
        accuracy_random_forest = accuracy_score(y_test, y_pred_random_forest)
        print(f"Accuracy of the Random Forest Classifier: {accuracy_random_forest:.2f}")

        return random_forest, label_encoders

    @staticmethod
    def train_model(data):
        """
        prepares data for training, calls training method
        :param data: dataframe with prepared driver data
        :return: trained model and used encoders
        """
        try:
            drivers_data = data.copy()
            drivers_data.drop(columns=['driver'], inplace=True)

            return AdaptProposalModel.__train_random_forest(drivers_data)

        except Exception as e:
            raise RuntimeError("Error during model training!") from e

    @staticmethod
    def retrain_model(data, accumulated_data):
        """
        prepares data for retraining with collected data
        :param data: dataframe with driver data
        :param accumulated_data: data send to the app since the last training
        :return: updated model, updated encoders
        """
        try:
            drivers_data = data.copy()
            accumulated_df = pd.DataFrame(accumulated_data)

            # Add accumulated data to original dataframe
            combined_data = pd.concat([drivers_data, accumulated_df], ignore_index=True)

            combined_data.drop(columns=['driver'], inplace=True)

            return AdaptProposalModel.__train_random_forest(combined_data)

        except Exception as e:
            raise RuntimeError("Error during model retraining!") from e

    @staticmethod
    def predict(trained_model, label_encoders, new_driver_data):
        """
        predict on the trained RandomForestClassifier
        :param trained_model: model trained by train or retrain method
        :param label_encoders: encoders created by train or retrain method
        :param new_driver_data: preferences json posted to the application
        :return: predicted car, list of top three predicted cars, likelihoods in percentage
        """
        new_driver_data_mapped = new_driver_data.copy()

        for key, value in new_driver_data_mapped.items():
            # Convert Object values to Integers
            if key in label_encoders:
                new_driver_data_mapped[key] = label_encoders[key].transform([value])[0]

        prediction = trained_model.predict([list(new_driver_data_mapped.values())])
        predicted_car = label_encoders['car'].inverse_transform(prediction)[0]

        # Get probability scores for every car
        prediction_probabilities = trained_model.predict_proba([list(new_driver_data_mapped.values())])[0]
        prediction_probabilities_list = prediction_probabilities.tolist()

        # Show Top 3 Results
        top3_indices = np.argsort(prediction_probabilities)[::-1][:3]

        # Get corresponding cars
        top3_cars = label_encoders['car'].inverse_transform(top3_indices)
        top3_cars_list = top3_cars.tolist()

        return predicted_car, top3_cars_list, prediction_probabilities_list

    @staticmethod
    def visualize_nth_tree(random_forest, data, n):
        """
        Visualize a single tree in the random forest
        :param random_forest: trained model
        :param data: generated drivers data
        :param n: index of tree to visualize
        :return: png of visualized tree
        """
        # extract feature names from data
        data.drop(columns=['driver'], inplace=True)
        data.drop(columns=['car'], inplace=True)
        feature_names = data.columns

        num_estimators = len(random_forest.estimators_)
        estimator = random_forest.estimators_[n - 1]
        plt.figure(figsize=(16, 8))
        plot_tree(
            estimator,
            feature_names=feature_names,
            max_depth=3,
            fontsize=10,
            filled=False
        )
        plt.title("Decision Tree " + str(n) + "/" + str(num_estimators))
        # Save the plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plt.close()

        # Encode the image as base64
        img_data = base64.b64encode(img.read()).decode()

        return img_data

    @staticmethod
    def visualize_feature_importance(random_forest, data):
        """
        Visualize the feature importance in the random forest
        :param random_forest: trained model
        :param data: generated drivers data
        :return:  png of feature importance bar chart
        """
        # extract feature names from data
        data.drop(columns=['driver'], inplace=True)
        data.drop(columns=['car'], inplace=True)
        feature_names = data.columns

        importance = random_forest.feature_importances_
        # times 100 for conversion to %
        importance_map = pd.Series(importance * 100, feature_names)
        plt.figure(figsize=(6, 6))
        importance_map.sort_values().plot.barh()
        plt.title("Feature Importance")
        plt.xlabel("%")

        # Save the plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plt.close()

        # Encode the image as base64
        img_data = base64.b64encode(img.read()).decode()

        return img_data

    @staticmethod
    def visualize_confusion_matrix(random_forest, data):
        """
        Visualize the confucion matrix of the random forest
        :param random_forest: trained model
        :param data: generated drivers data
        :return: png of confusion matrix
        """
        categorical_columns = data.select_dtypes(include=['object']).columns
        label_encoders = {}
        for column in categorical_columns:
            label_encoders[column] = LabelEncoder()
            data[column] = label_encoders[column].fit_transform(data[column])

        data.drop(columns=['driver'], inplace=True)

        # Split data into training and test set, exactly the same split as in train model
        _, X_test, _, y_test = train_test_split(data.drop(columns=['car']),
                                                data['car'],
                                                test_size=0.2,
                                                random_state=45)

        y_pred_random_forest = random_forest.predict(X_test.values)
        accuracy_random_forest = accuracy_score(y_test, y_pred_random_forest)

        cm = confusion_matrix(y_test, y_pred_random_forest)
        cmd = ConfusionMatrixDisplay(confusion_matrix=cm)
        _, ax = plt.subplots(figsize=(8, 8))
        cmd.plot(ax=ax)

        plt.title("Confusion Matrix, Accuracy: " + str(accuracy_random_forest))
        # Save the plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plt.close()

        # Encode the image as base64
        img_data = base64.b64encode(img.read()).decode()

        return img_data
