import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import tree
from sklearn.datasets import load_iris
import graphviz

with open('users_IA_clases.json') as file:
    data_users_entrenamiento = json.load(file)

with open('users_IA_predecir.json') as file:
    data_users_prueba = json.load(file)

data_x = []
data_y = []

for user in data_users_entrenamiento["usuarios"]:
    data_y.append([user["vulnerable"]])
    if user["emails_phishing_recibidos"] != 0:
        data_x.append([user["emails_phishing_clicados"],  user["emails_phishing_recibidos"]])
    else:
        data_x.append([0, 0])

# REGRESION LINEAL

# Split the data into training/testing sets
data_x_train = data_x[:-20]
data_x_test = data_x[-20:]
# Split the targets into training/testing sets
data_y_train = data_y[:-20]
data_y_test = data_y[-20:]
# Create linear regression object
regr = linear_model.LinearRegression()
# Train the model using the training sets
regr.fit(data_x_train, data_y_train)

m = regr.coef_      # m[0][0] = 0.01271246 ; m[0][1] = -0.00539587
b = regr.intercept_ # b = 0.61693166
x = data_x_test

# Make predictions using the testing set
data_y_pred = regr.predict(np.array(data_x_test))
for i in range (0, len(data_y_pred)):
    if data_y_pred[i] < 0.5:
        data_y_pred[i] = 0
    else:
        data_y_pred[i] = 1

# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(data_y_test, data_y_pred))

x_real = []
for i in x:
    if (i[1]==0):
        i[1] = 0.01
    x_real.append(i[0]/i[1])
x = x_real

# Plot outputs
plt.scatter(np.array(x), np.array(data_y_test), color="black")
plt.plot((m[0][0]*np.array(x))+b, np.array(x))
plt.show()


# DECISION TREE

#Split data
clf = tree.DecisionTreeClassifier()
clf = clf.fit(data_x_train, data_y_train)

# Código que muestra el grafo en la consola de comandos
text_representation = tree.export_text(clf)
print(text_representation)

# Código de internet para mostrar el grafo
#fig = plt.figure(figsize=(25,20))
#imagen = tree.plot_tree(clf, feature_names=str(data_x_test), class_names=str(data_y_test), filled=True)
#fig.savefig("decistion_tree.png")

# Código diapositivas

#Predict
#clf_model = tree.DecisionTreeClassifier()
#clf_model.fit(data_x_train, data_y_train)

#Print plot
#dot_data = tree.export_graphviz(clf, out_file=None)
#graph = graphviz.Source(dot_data)



