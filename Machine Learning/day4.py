import numpy as np

np.random.seed(42)
X=np.random.uniform(0,10,20)
y=4*X+10+np.random.normal(0,1,20)

# w = 0.0
# b = 0.0
# learning_rate = 0.0001  # very tiny steps

# for step in range(500):
#     predictions = w * X + b
#     loss = np.mean((predictions - y) ** 2)
#     dw = (2/n) * np.sum((predictions - y) * X)
#     db = (2/n) * np.sum(predictions - y)
#     w = w - learning_rate * dw
#     b = b - learning_rate * db
    
#     if step % 100 == 0:
#         print(f"Step {step:3d} | Loss: {loss:8.2f} | w: {w:.4f} | b: {b:.4f}")

# print(f"\nFinal: w={w:.4f} (target: 4), b={b:.4f} (target: 10)")

w = 0.0
b = 0.0
learning_rate = 0.01
batch_size = 5

for step in range(500):
    indices = np.random.choice(len(X), batch_size)
    X_batch = X[indices]
    y_batch = y[indices]
    
    predictions = w * X_batch + b
    loss = np.mean((predictions - y_batch) ** 2)
    dw = (2/batch_size) * np.sum((predictions - y_batch) * X_batch)
    db = (2/batch_size) * np.sum(predictions - y_batch)
    w = w - learning_rate * dw
    b = b - learning_rate * db
    
    if step % 100 == 0:
        full_loss = np.mean((w * X + b - y) ** 2)
        print(f"Step {step:3d} | Full Loss: {full_loss:8.2f} | w: {w:.4f} | b: {b:.4f}")

print(f"\nFinal: w={w:.4f} (target: 4), b={b:.4f} (target: 10)")
print(X_batch, y_batch)