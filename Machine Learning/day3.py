import numpy as np

# We know the real relationship: y = 4x + 10
# The model will try to DISCOVER this by learning w=4 and b=10

np.random.seed(42)
X = np.random.uniform(0, 10, 20)  # 20 random numbers between 0-10
y = 4 * X + 10 + np.random.normal(0, 1, 20)  # add small noise

print("First 5 X values:", X[:5])
print("First 5 y values:", y[:5].round(2))

# The model will learn: y = w * X + b
# True answer: w=4, b=10
# But the model starts with random guesses

w = 0.0  # weight (should become ~4)
b = 0.0  # bias (should become ~10)

print(f"Starting weights: w={w}, b={b}")
print(f"Target weights:   w=4, b=10")
print(f"The model currently thinks: y = {w}*X + {b}")
print(f"Which means: y = 0  (predicts zero for everything!)")

# Predict with current weights (w=0, b=0)
predictions = w * X + b

# How wrong are we?
loss = np.mean((predictions - y) ** 2)  # MSE from yesterday!

print("First 5 predictions:", predictions[:5].round(2))
print("First 5 actual:     ", y[:5].round(2))
print(f"\nLoss (MSE): {loss:.2f}")

# How many data points
n = len(X)

# Gradient for w: how much does loss change if we nudge w?
dw = (2/n) * np.sum((predictions - y) * X)

# Gradient for b: how much does loss change if we nudge b?
db = (2/n) * np.sum(predictions - y)

print(f"Gradient for w (dw): {dw:.2f}")
print(f"Gradient for b (db): {db:.2f}")

learning_rate = 0.01

# Update weights
w = w - learning_rate * dw
b = b - learning_rate * db

print(f"Updated weights: w={w:.4f}, b={b:.4f}")
print(f"Target:          w=4.0000, b=10.0000")

# New predictions with updated weights
predictions = w * X + b
loss = np.mean((predictions - y) ** 2)

print(f"Loss after 1 step: {loss:.2f}")
print(f"Loss before:       926.96")

# Reset to starting point
w = 0.0
b = 0.0
learning_rate = 0.01

# Run 50 steps of gradient descent
for step in range(50):
    # 1. Predict
    predictions = w * X + b
    
    # 2. Compute loss
    loss = np.mean((predictions - y) ** 2)
    
    # 3. Compute gradients
    dw = (2/n) * np.sum((predictions - y) * X)
    db = (2/n) * np.sum(predictions - y)
    
    # 4. Update weights
    w = w - learning_rate * dw
    b = b - learning_rate * db
    
    # Print every 10 steps
    if step % 10 == 0:
        print(f"Step {step:2d} | Loss: {loss:8.2f} | w: {w:.4f} | b: {b:.4f}")

print(f"\nFinal: w={w:.4f} (target: 4), b={b:.4f} (target: 10)")

w = 0.0
b = 0.0
learning_rate = 0.01

for step in range(500):
    predictions = w * X + b
    loss = np.mean((predictions - y) ** 2)
    dw = (2/n) * np.sum((predictions - y) * X)
    db = (2/n) * np.sum(predictions - y)
    w = w - learning_rate * dw
    b = b - learning_rate * db
    
    if step % 100 == 0:
        print(f"Step {step:3d} | Loss: {loss:8.2f} | w: {w:.4f} | b: {b:.4f}")

print(f"\nFinal: w={w:.4f} (target: 4), b={b:.4f} (target: 10)")