import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
import cv2

DATA_TIMESTAMP = 'timestamp'
DATA_ID = 'id'
DATA_PIR = 'pir'
DATA_TEMPERATURE = 'temperature'
DATA_HUMIDITY = 'humidity'
DATA_CO2 = 'co2'

SENSOR_DEVICE_ID = 'Device ID'
SENSOR_LOCATION = 'Locations'
SENSOR_LATITUDE = 'Latitude'
SENSOR_LONGITUDE = 'Longitude'



class DataHandler:
    data = None
    rooms = {}

    def __init__(self, data_csv, sensor_csv, area_file, rooms_file, months, large=True):
        # read sensor locations
        self.sensors = pd.read_csv(sensor_csv)

        # read sensor readings
        if large:
            current_record = 1
            for df in pd.read_csv(data_csv, iterator=True, chunksize=1000):
                print('Read ', current_record, 'x 1000 records')
                current_record = current_record + 1
                df = df.dropna()
                df[DATA_TIMESTAMP] = pd.to_datetime(df[DATA_TIMESTAMP])
                end_date = datetime(year=2018, month=11, day=20)  # 2018-11-20
                start_date = end_date - timedelta(days=30 * months)
                date_filter = (df[DATA_TIMESTAMP] > start_date)
                df = df.loc[date_filter]
                if self.data is None:
                    self.data = df
                else:
                    self.data = pd.concat([self.data, df])
        else:
            self.data = pd.read_csv(data_csv)

        # read room ids
        rooms_file = open(rooms_file, 'r')
        for room in rooms_file.readlines():
            room = room.split('=')
            self.rooms[room[0]] = room[1]
        rooms_file.close()

        # read grid locations
        self.area = pd.read_csv(area_file, header=None)

    def save_data(self, output_file):
        self.data.to_csv(output_file)


class TellusData:
    sensors = {}  # store data per sensor
    grid_width = 0
    grid_height = 0
    start_time = None
    end_time = None
    max_pir = 0

    def __init__(self, data_handler, grid_width, grid_height, room_filter=None):
        self.grid_width = grid_width
        self.grid_height = grid_height
        p1a = [data_handler.area.iloc[0, 0], data_handler.area.iloc[0, 1]]
        p2a = [data_handler.area.iloc[1, 0], data_handler.area.iloc[1, 1]]
        p3a = [data_handler.area.iloc[2, 0], data_handler.area.iloc[2, 1]]
        p4a = [data_handler.area.iloc[3, 0], data_handler.area.iloc[3, 1]]
        p1b = [0, 0]
        p2b = [0, grid_height]
        p3b = [grid_width, grid_height]
        p4b = [grid_width, 0]
        pa = np.array([p1a,p2a,p3a,p4a], np.float32)
        pb = np.array([p1b, p2b, p3b, p4b], np.float32)
        self.perspectiveMatrix = cv2.getPerspectiveTransform(pa, pb)

        self.start_time = datetime.strptime(min(data_handler.data[DATA_TIMESTAMP]), '%Y-%m-%d %H:%M:%S.%f')
        self.end_time = datetime.strptime(max(data_handler.data[DATA_TIMESTAMP]), '%Y-%m-%d %H:%M:%S.%f')
        data_handler.data[DATA_TIMESTAMP] = pd.to_datetime(data_handler.data[DATA_TIMESTAMP])
        self.max_pir = max(data_handler.data[DATA_PIR])

        if room_filter is not None:
            data_handler.sensors = \
                data_handler.sensors[data_handler.sensors[SENSOR_LOCATION].str.contains(room_filter)]
        for idx, row in data_handler.sensors.iterrows():
            device_id = row[1].lower()
            device_id = '-'.join([device_id[2*x:2*x + 2] for x in range(round(len(device_id)/2))])
            location = row[2]
            x, y = self.get_coordinate(row[3], row[4])
            id_filter = data_handler.data[DATA_ID] == device_id
            self.sensors[device_id] = {'location': location, 'x': x, 'y': y, 'data': data_handler.data.loc[id_filter]}

    def get_coordinate(self, latitude, longitude):
        sourcePoint = np.array([[latitude, longitude]],np.float32)
        destPoint = cv2.perspectiveTransform(sourcePoint[None,:,:], self.perspectiveMatrix)
        return destPoint[0,0,0],destPoint[0,0,1]






