import pandas as pd
import pickle
from sklearn.tree import DecisionTreeClassifier

def train_and_save():
    df = pd.read_csv("dataset.csv")

    X = df.drop("disease", axis=1)
    y = df["disease"]

    model = DecisionTreeClassifier(max_depth=6)
    model.fit(X, y)

    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)