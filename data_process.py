import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

train_df = pd.read_csv('data/data.csv')
test_df = pd.read_csv('data/test_data.csv')

# Linear regression
lm = LinearRegression()
X = train_df[train_df.keys()[1:]]
Y = np.log(train_df['Y_(s,t)'])
lm.fit(X, Y)
Y_pred = lm.predict(X)

X_test = test_df[test_df.keys()[1:]]
Y_test = np.log(test_df['Y_(s,t)'])
Y_test_pred = lm.predict(X_test)

print('The model fit on training data is: ', lm.score(X,Y))   # R_squared
print('The model fit on testing data is: ', lm.score(X_test,Y_test))   # R_squared

# MLP
# Train the regression model with five hidden layers
regr = MLPRegressor(random_state=1, alpha=0.1, hidden_layer_sizes=(50,30,30,10,5), \
                    max_iter=10000).fit(X.values, Y.values.ravel())
Y_pred = regr.predict(X)

print('Mean squared error: %.2f'
      % mean_squared_error(Y, Y_pred))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(Y, Y_pred))

Y_test_pred = regr.predict(X_test)
print('Mean squared error: %.2f'
      % mean_squared_error(Y_test, Y_test_pred))
print('Coefficient of determination: %.2f'
      % r2_score(Y_test, Y_test_pred))