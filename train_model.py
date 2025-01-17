import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Load data from pickle file
data_dict = pickle.load(open('./data.pickle', 'rb'))

# Check if all the data items have the same shape
data = data_dict['data']
labels = data_dict['labels']

# Print the shape of each data element to ensure consistency
print("Checking data shape consistency:")
for i, element in enumerate(data):
    print(f"Element {i} shape: {np.shape(element)}")



# Reshape all elements to have exactly 42 features
# Example: If original data is more than 42, we select the first 42
padded_data = [item[:42] for item in data]  # Assuming data has at least 42 features

# Convert padded_data and labels to numpy arrays
data = np.array(padded_data)
labels = np.asarray(labels)

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, shuffle=True, stratify=labels)

# Initialize RandomForest model
model = RandomForestClassifier()

# Train the model
model.fit(x_train, y_train)

# Predict on the test data
y_predict = model.predict(x_test)

# Calculate accuracy
score = accuracy_score(y_test, y_predict)
print(f'{score * 100:.2f}% Accuracy!')

# Save the trained model to a file
with open('model1.p', 'wb') as f:
    pickle.dump({'model1': model}, f)
