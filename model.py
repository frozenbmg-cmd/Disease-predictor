import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

def train_and_save():
    df = pd.read_csv("dataset.csv")

    X = df.drop("disease", axis=1)
    y = df["disease"]

    # Better than DecisionTree for this task
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_leaf=2,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X, y)

    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)
