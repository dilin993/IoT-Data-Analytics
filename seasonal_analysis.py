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
period = timedelta(minutes=15)
start = tellus_data.start_time
end = start + period
stop = start + timedelta(days=2)

variables = [DATA_CO2, DATA_HUMIDITY, DATA_TEMPERATURE]
columns = [DATA_TIMESTAMP, DATA_CO2, DATA_HUMIDITY, DATA_TEMPERATURE]
df = pd.DataFrame(columns=columns)
while start < stop:
    print('analysing time: ', start)
    readings = np.zeros((len(variables), 1), dtype=float)
    count = 0
    for device_id in tellus_data.sensors:
        data = tellus_data.sensors[device_id]['data']
        date_filter = (data[DATA_TIMESTAMP] >= start) & (data[DATA_TIMESTAMP] < end)
        data = data.loc[date_filter]
        if len(data) > 0:
            for i in range(len(variables)):
                y0 = data[variables[i]].to_numpy()
                readings[i] = readings[i] + y0[0]
            count = count + 1
    dic = {DATA_TIMESTAMP: start.strftime('%Y-%m-%d %H:%M:%S.%f')}
    for i in range(len(variables)):
        readings[i] = readings[i]/count
        dic[variables[i]] = readings[i][0]
    df = df.append(dic, ignore_index=True)
    start = start + period
    end = end + period
df.to_csv(room + str(tellus_data.start_time.strftime('-%Y-%m-%d')) + '_' + stop.strftime('%Y-%m-%d') + '.csv')
# x = range(len(y))
# fig, ax = plt.subplots()
# plt.plot(x, y)
# # beautify the x-labels
# # plt.gcf().autofmt_xdate()
# # myFmt = DateFormatter("%H:%M")
# # ax.xaxis.set_major_formatter(myFmt)
# # plt.legend()
# plt.xlabel('Time of the day')
# plt.ylabel(variable)
# plt.title(variable + ' readings from' + start.strftime('%Y-%m-%d') + ' to ' + end.strftime('%Y-%m-%d') +
#           ' at ' + room)
# plt.show()
# fig.savefig(variable + '-' + room + str(start.strftime('-%Y-%m-%d')) + '_' + end.strftime('%Y-%m-%d') + '.png')
