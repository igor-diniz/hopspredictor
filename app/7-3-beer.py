#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle




beer_data = pd.read_csv('../data/7-3-beer.csv')

beer_data = beer_data.astype(float)

#beer_data['citrus'] = beer_data['citrus'].astype(float)
beer_data["citrus"].fillna(beer_data["citrus"].mean(), inplace=True)
beer_data["herbal (herbaceous)"].fillna(beer_data["herbal (herbaceous)"].mean(), inplace=True)
beer_data["overall hoppy intensity"].fillna(beer_data["overall hoppy intensity"].mean(), inplace=True)
beer_data["geraniol (cis)"].fillna(beer_data["geraniol (cis)"].mean(), inplace=True)
beer_data["linalool"].fillna(beer_data["linalool"].mean(), inplace=True)
beer_data["myrcene"].fillna(beer_data["myrcene"].mean(), inplace=True)
beer_data["α-humulene"].fillna(beer_data["α-humulene"].mean(), inplace=True)
beer_data["β-caryophyllene"].fillna(beer_data["β-caryophyllene"].mean(), inplace=True)
beer_data["β-pinene"].fillna(beer_data["β-pinene"].mean(), inplace=True)
beer_data["trans-β-farnesene"].fillna(beer_data["trans-β-farnesene"].mean(), inplace=True)

X = beer_data.drop(columns=['citrus', 'herbal (herbaceous)', 'overall hoppy intensity'])
y = beer_data.drop(columns=['geraniol (cis)', 'linalool', 'myrcene', 'trans-β-farnesene', 'α-humulene', 'β-caryophyllene', 'β-pinene'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


model = MultiOutputRegressor(LinearRegression())
model.fit(X_train, y_train)

predictions = model.predict(X_test)

y_test = y_test.values


predictions = predictions.flatten()
y_test = y_test.flatten()

print(predictions)
print(y_test)

pickle.dump(model, open('../models/beer_model.pkl', 'wb'))
