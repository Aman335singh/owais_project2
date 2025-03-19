import numpy as np
import matplotlib.pyplot as plt
import json

# Load JSON data
with open("results/intent_report.json", "r") as file:
    data = json.load(file)

# Filter valid intents only (exclude non-intent keys like accuracy, avg, etc.)
labels = [intent for intent in data if isinstance(data[intent], dict)]

# Initialize confusion matrix
matrix = np.zeros((len(labels), len(labels)), dtype=int)

# Fill the confusion matrix
for i, intent in enumerate(labels):
    for confused_intent, count in data[intent].get("confused_with", {}).items():
        if confused_intent in labels:
            j = labels.index(confused_intent)
            matrix[i][j] = count

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
plt.imshow(matrix, cmap='Blues')
plt.title('Confusion Matrix')
plt.colorbar()
plt.xticks(np.arange(len(labels)), labels, rotation=45)
plt.yticks(np.arange(len(labels)), labels)
plt.xlabel('Predicted')
plt.ylabel('Actual')

# Display values inside the cells
for i in range(len(labels)):
    for j in range(len(labels)):
        plt.text(j, i, matrix[i, j], ha='center', va='center', color='black')

plt.tight_layout()
plt.show()
