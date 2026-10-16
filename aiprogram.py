import pandas as pd
import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report





# ---------------------------------------------------
# 1. Create Dataset
# ---------------------------------------------------

data = {
    'Age': [22, 25, 28, 35, 40, 45, 50, 55, 60, 30,
            27, 48, 52, 33, 38],

    'Salary': [20000, 25000, 30000, 40000, 50000, 55000,
               60000, 70000, 80000, 35000, 28000, 58000,
               65000, 42000, 48000],

    'Experience': [1, 2, 3, 5, 8, 10, 12, 15, 18, 4,
                   2, 11, 14, 6, 7],

    'Buys': [0, 0, 0, 1, 1, 1, 1, 1, 1, 0,
             0, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

print("======================================")
print("           DATASET")
print("======================================")
print(df)


# ---------------------------------------------------
# 2. Separate Input and Output
# ---------------------------------------------------

X = df[['Age', 'Salary', 'Experience']]
y = df['Buys']


# ---------------------------------------------------
# 3. Split Dataset into Training and Testing
# ---------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

print("\n======================================")
print("          TRAINING DATA")
print("======================================")
print(X_train)

print("\n======================================")
print("           TESTING DATA")
print("======================================")
print(X_test)


# ---------------------------------------------------
# 4. Create Decision Tree Model
# ---------------------------------------------------

model = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=4,
    random_state=42
)


# ---------------------------------------------------
# 5. Train Model
# ---------------------------------------------------

model.fit(X_train, y_train)

print("\nDecision Tree trained successfully.")


# ---------------------------------------------------
# 6. Predict Test Data
# ---------------------------------------------------

y_pred = model.predict(X_test)

print("\n======================================")
print("          ACTUAL VALUES")
print("======================================")
print(list(y_test))

print("\n======================================")
print("        PREDICTED VALUES")
print("======================================")
print(list(y_pred))


# ---------------------------------------------------
# 7. Calculate Accuracy
# ---------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n======================================")
print("             ACCURACY")
print("======================================")
print("Accuracy:", accuracy * 100, "%")


# ---------------------------------------------------
# 8. Confusion Matrix
# ---------------------------------------------------

cm = confusion_matrix(y_test, y_pred)

print("\n======================================")
print("        CONFUSION MATRIX")
print("======================================")
print(cm)


# ---------------------------------------------------
# 9. Classification Report
# ---------------------------------------------------

print("\n======================================")
print("      CLASSIFICATION REPORT")
print("======================================")
print(classification_report(y_test, y_pred, zero_division=0))


# ---------------------------------------------------
# 10. Predict New Customer
# ---------------------------------------------------

new_customer = pd.DataFrame(
    [[32, 45000, 5]],
    columns=['Age', 'Salary', 'Experience']
)

prediction = model.predict(new_customer)

print("\n======================================")
print("         NEW CUSTOMER")
print("======================================")
print("Age        = 32")
print("Salary     = 45000")
print("Experience = 5 years")

if prediction[0] == 1:
    print("Prediction: Customer will BUY")
else:
    print("Prediction: Customer will NOT BUY")


# ---------------------------------------------------
# 11. Display Decision Tree
# ---------------------------------------------------

plt.figure(figsize=(15, 8))

plot_tree(
    model,
    feature_names=['Age', 'Salary', 'Experience'],
    class_names=['No', 'Yes'],
    filled=True,
    rounded=True
)

plt.title("Decision Tree - Customer Purchase Prediction")
plt.tight_layout()
plt.show()
