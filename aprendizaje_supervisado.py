from pathlib import WindowsPath
from subprocess import call
import matplotlib.pyplot as plt
import numpy as np
import json
from sklearn import linear_model, tree
from sklearn.metrics import mean_squared_error
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

#Predict
X,y = data_x_train, data_y_train
clf = tree.DecisionTreeClassifier()
clf = clf.fit(data_x_train, data_y_train)
print(clf.predict(np.array(data_x_test)))


dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("decisionTree")
dot_data = tree.export_graphviz(clf, out_file=None, filled=True, rounded=True, special_characters=True)
graph = graphviz.Source(dot_data)
graph.render('decisionTree.gv', view=True).replace('\\', '/')
call([WindowsPath('dot'), '-Kdot', '-Tpdf', '-o', 'decisionTree'])

'''
# RANDOM FOREST
X,y = data_x_train, data_y_train
clf = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
clf = clf.fit(data_x_train, data_y_train)
print(str(X[0]) + " " + str(y[0]))
print(clf.predict([X[0]]))

for i in range(len(clf.estimators_)):
    estimator = clf.estimators_[i]
    export_graphviz(estimator, out_file='RandomForest.dot', rounded=True, proportion=False,precision=2, filled=True)
    call(['dot','-Tpng', 'RandomForest.dot','-o','RandomForest'+str(i)+'.png','-Gdpi=600'])
'''


