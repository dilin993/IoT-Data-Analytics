import numpy as np
import pandas as pd
from preprocess import DataHandler, TellusData, DATA_TIMESTAMP, DATA_TEMPERATURE, SENSOR_LOCATION, DATA_HUMIDITY, \
DATA_CO2
from matplotlib.dates import drange
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter
from sklearn import preprocessing
from sklearn import linear_model

file = 'TY-2018-08-22_2018-09-21'
dstart = datetime(2018,8,21)
dstop = datetime(2018,9,21)
variable1 = DATA_CO2
variable2 = DATA_HUMIDITY
data = pd.read_csv(file + '.csv')
data = data.dropna()

x = data[variable1].to_numpy()
x_scaled = preprocessing.scale(x)
x_scaled = x_scaled.reshape(-1,1)
y = data[variable2].to_numpy()
y_scaled = preprocessing.scale(y)
y_scaled = y_scaled.reshape(-1,1)

reg = linear_model.LinearRegression()
reg.fit(x_scaled, y_scaled)
y_pred = reg.predict(x_scaled)

fig, ax = plt.subplots()
plt.scatter(x_scaled, y_scaled)
plt.plot(x_scaled, y_pred, color='red', linewidth=2)
plt.xlabel('normalized ' + variable1)
plt.ylabel('normalized ' + variable2)
plt.title(file + ' ' + variable1 + ' vs. ' + variable2)
plt.show()
fig.savefig(file + '_' + variable1 + '_' + variable2 + '.png')

