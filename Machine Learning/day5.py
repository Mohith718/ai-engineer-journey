import pandas as pd

url = "https://raw.githubusercontent.com/GrandmaCan/ML/main/Resgression/Salary_Data.csv"
df = pd.read_csv(url)

print("Shape:", df.shape)
print("\nColumn names:", list(df.columns))
print("\nFirst 10 rows:")
print(df.head(10))
print("\nBasic stats:")
print(df.describe().round(2))

from sklearn.model_selection import train_test_split
import numpy as np

X = df[['YearsExperience']].values  # double brackets = keeps it as a table
y = df['Salary'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training people:", len(X_train))
print("Testing people:", len(X_test))
print("\nTest set years:", X_test.ravel().round(1))
print("Test set salaries:", y_test.round(1))

from sklearn.metrics import mean_squared_error

# The dumbest model: just predict the average salary for everyone
avg_salary = np.mean(y_train)
print(f"Average training salary: {avg_salary:.1f}k")

# Predict the same number for every test person
dumb_predictions = np.full(len(X_test), avg_salary)

print("\nTest predictions vs actual:")
for i in range(len(X_test)):
    print(f"  {X_test[i][0]:.1f} years → Predicted: {dumb_predictions[i]:.1f}k | Actual: {y_test[i]:.1f}k")

train_loss = mean_squared_error(y_train, np.full(len(X_train), avg_salary))
test_loss = mean_squared_error(y_test, dumb_predictions)
print(f"\nTrain MSE: {train_loss:.1f}")
print(f"Test MSE:  {test_loss:.1f}")

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

print(f"Learned: salary = {model.coef_[0]:.2f} × years + {model.intercept_:.2f}")

good_predictions = model.predict(X_test)

print("\nTest predictions vs actual:")
for i in range(len(X_test)):
    print(f"  {X_test[i][0]:.1f} years → Predicted: {good_predictions[i]:.1f}k | Actual: {y_test[i]:.1f}k")

train_loss = mean_squared_error(y_train, model.predict(X_train))
test_loss = mean_squared_error(y_test, good_predictions)
print(f"\nTrain MSE: {train_loss:.1f}")
print(f"Test MSE:  {test_loss:.1f}")