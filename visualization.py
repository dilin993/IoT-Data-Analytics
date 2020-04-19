import numpy as np
import pandas as pd
from preprocess import DataHandler, TellusData, DATA_TIMESTAMP, DATA_TEMPERATURE, SENSOR_LOCATION, DATA_HUMIDITY, \
DATA_CO2
from matplotlib.dates import drange
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter

room = 'TY'
data_handler = DataHandler('data/processed_data.csv', 'data/sensors.csv', 'data/area.txt', 'data/rooms.txt', 3, False)
# data_handler.save_data('data/processed_data.csv')
tellus_data = TellusData(data_handler, 1019, 552, room)
period = timedelta(hours=24)
start = tellus_data.start_time
end = start + period

fig, ax = plt.subplots()
count = 0
variable = DATA_CO2
for device_id in tellus_data.sensors:
    data = tellus_data.sensors[device_id]['data']
    date_filter = (data[DATA_TIMESTAMP] >= start) & (data[DATA_TIMESTAMP] < end)
    data = data.loc[date_filter]
    x = data[DATA_TIMESTAMP]
    y = data[variable]
    plt.plot(x, y, label=device_id)
    count = count + 1
    if count > 8:  # limit to 8 plots
        break

# beautify the x-labels
plt.gcf().autofmt_xdate()
myFmt = DateFormatter("%H:%M")
ax.xaxis.set_major_formatter(myFmt)
plt.legend()
plt.xlabel('Time of the day')
plt.ylabel(variable)
plt.title(variable + ' readings on ' + start.strftime('%Y-%m-%d') + ' at ' + room)
plt.show()
fig.savefig(variable + '-' + room + str(start.strftime('-%Y-%m-%d')) + '.png')
