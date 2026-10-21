import numpy as np

# You're predicting vegetable prices (in rupees)
actual_prices  = np.array([50, 80, 120, 200, 90])
predicted      = np.array([55, 75, 130, 180, 95])

# Step 1: How far off is each prediction?
errors = predicted - actual_prices
print("Errors:", errors)

# Step 2: Square each error
squared_errors = errors ** 2
print("Squared errors:", squared_errors)

# Step 3: Take the average — this is MSE
mse = np.mean(squared_errors)
print("MSE:", mse)

# What if your predictions were almost perfect?
good_predictions = np.array([51, 79, 121, 198, 91])

good_errors = good_predictions - actual_prices
good_squared = good_errors ** 2
good_mse = np.mean(good_squared)

print("Good errors:", good_errors)
print("Good squared:", good_squared)
print("Good MSE:", good_mse)
print()
print(f"Bad MSE:  {mse}")
print(f"Good MSE: {good_mse}")
print(f"Good predictions have LOWER loss!")
def mse(actual, predicted):
    return np.mean((predicted - actual) ** 2)

# Test it
print("Bad predictions MSE:", mse(actual_prices, predicted))
print("Good predictions MSE:", mse(actual_prices, good_predictions))

def mae(actual, predicted):
    return np.mean(np.abs(predicted - actual))

print("Bad predictions MAE:", mae(actual_prices, predicted))
print("Good predictions MAE:", mae(actual_prices, good_predictions))

# The model predicts probabilities for a yes/no question
# Example: "Is this email spam?"

# Actual answer: YES it's spam (1)
actual = 1

# Model says: "I'm 90% sure it's spam"
confident_right = 0.9

# Model says: "I'm 10% sure it's spam" (thinks it's NOT spam)
confident_wrong = 0.1

# Cross-entropy loss for one prediction
import math

loss_right = -math.log(confident_right)
loss_wrong = -math.log(confident_wrong)

print(f"Model said 90% spam, it WAS spam → loss: {loss_right:.4f}")
print(f"Model said 10% spam, it WAS spam → loss: {loss_wrong:.4f}")

# What happens as the model's confidence changes?
probabilities = [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]

print("If the correct answer is YES (1):")
print(f"{'Model says':>12} | {'Loss':>8}")
print("-" * 25)
for p in probabilities:
    loss = -math.log(p)
    print(p, loss)

import math

print(math.log(1))
print(math.log(2))
print(math.log(5))
print(math.log(10))
print(math.log(100))
print(math.log(0.9))
print(math.log(0.5))
print(math.log(0.1))
print(math.log(0.01))

# Simplified: LLM has a vocabulary of 5 words
vocabulary = ["the", "cat", "sat", "on", "mat"]

# The actual next word is "mat" (index 4)
actual_word = "mat"
actual_index = 4

# BAD model: spreads probability evenly (it has no idea)
bad_model_probs = [0.2, 0.2, 0.2, 0.2, 0.2]

# GOOD model: puts most probability on "mat"
good_model_probs = [0.05, 0.02, 0.01, 0.02, 0.90]

# Loss = -log(probability assigned to the CORRECT word)
bad_loss = -math.log(bad_model_probs[actual_index])
good_loss = -math.log(good_model_probs[actual_index])

print(f"Actual next word: '{actual_word}'")
print(f"Bad model gave 'mat' {bad_model_probs[actual_index]:.0%} probability → loss: {bad_loss:.4f}")
print(f"Good model gave 'mat' {good_model_probs[actual_index]:.0%} probability → loss: {good_loss:.4f}")