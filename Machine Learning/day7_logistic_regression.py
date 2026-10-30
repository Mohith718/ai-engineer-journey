import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

url="https://raw.githubusercontent.com/GrandmaCan/ML/main/Resgression/Salary_Data.csv"
df=pd.read_csv(url)

# print(df.head())
df["Highearner"]=(df["Salary"]>70).astype(int)

print(df.head(15))
print(df.shape)
print(df["Highearner"].sum())
print(len(df)-df["Highearner"].sum())
print(df[df["Highearner"]==1])

import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))
print("Input →  Sigmoid output")
for z in [-10, -5, -2, 0, 2, 5, 10]:
    print(f"  {z:4d}  →  {sigmoid(z):.4f}")

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

x = df[["YearsExperience"]].values
y = df["Highearner"].values

train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(train_x, train_y)

predictions = model.predict(test_x)
print("Predictions:", predictions)
print("Actuals:    ", test_y)
test=mean_squared_error(test_y, predictions)
print(f"Test MSE: {test:.1f}")
print(f"Accuracy: {accuracy_score(test_y, predictions):.2f}")

probabilities = model.predict_proba(test_x)

print("\nDetailed predictions:")
for i in range(len(test_x)):
    prob_high = probabilities[i][1]
    print(f"  {test_x[i][0]:.1f} years → {prob_high:.1%} chance of high earner → Predicted: {predictions[i]} | Actual: {test_y[i]}")