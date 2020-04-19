import numpy as np
import pandas as pd
from preprocess import DataHandler, TellusData, DATA_TIMESTAMP, DATA_TEMPERATURE, SENSOR_LOCATION, DATA_HUMIDITY, \
DATA_CO2
from matplotlib.dates import drange
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter
file = 'TY-2018-08-22_2018-09-21'
dstart = datetime(2018,8,21)
dstop = datetime(2018,9,21)
variable = DATA_CO2
data = pd.read_csv(file + '.csv')
data = data.dropna()
x = pd.to_datetime(data[DATA_TIMESTAMP])
y = data[variable]
fig, ax = plt.subplots()
plt.scatter(x, y)
# beautify the x-labels
plt.gcf().autofmt_xdate()
plt.xlim(dstart, dstop)
myFmt = DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(myFmt)
# plt.legend()
plt.xlabel('Time of the day')
plt.ylabel(variable)
plt.title(file + ' ' + variable)
plt.show()
fig.savefig(file + '_' + variable + '.png')


