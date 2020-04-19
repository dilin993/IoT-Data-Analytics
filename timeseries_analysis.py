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
variable = DATA_TEMPERATURE
data = pd.read_csv(file + '.csv')
data = data.dropna()
data[DATA_TIMESTAMP] = pd.to_datetime(data[DATA_TIMESTAMP])
dstart = data[DATA_TIMESTAMP].iloc[0]
days = 7
x = data[(data[DATA_TIMESTAMP] > dstart) & (data[DATA_TIMESTAMP] < dstart + timedelta(days=1))][variable].to_numpy()
dstart = dstart + timedelta(days=days)
y = data[(data[DATA_TIMESTAMP] >= dstart) & (data[DATA_TIMESTAMP] < dstart + timedelta(days=1))][variable].to_numpy()
n = min(len(x), len(y))
x = x[0:n].reshape(-1,1)
y = y[0:n].reshape(-1,1)
reg = linear_model.LinearRegression()
reg.fit(x, y)
y_pred = reg.predict(x)
fig, ax = plt.subplots()
plt.scatter(x, y)
plt.plot(x, y_pred, color='red', linewidth=2)
plt.xlabel(variable + '(t-' + str(days) + ')')
plt.ylabel(variable + '(t)')
plt.title('time series (t-' + str(days) + ')')
plt.show()
fig.savefig(variable + '_' + 'time_series _t-' + str(days) + '.png')
