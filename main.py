import numpy as np
import pandas as pd
from preprocess import DataHandler, TellusData, DATA_TIMESTAMP
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from skimage import io
from matplotlib import cm
from datetime import datetime, timedelta
from matplotlib.colors import Normalize
matplotlib.use("Agg")
color_map = cm.jet

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Test', artist='Matplotlib',
                comment='Movie support!')
writer = FFMpegWriter(fps=5, metadata=metadata)

fig = plt.figure()
img = io.imread('data/tellus-map.png')
plt.imshow(img)
plt.colorbar(cm.ScalarMappable(cmap=color_map, norm=Normalize(0, 30.0)))
l, = plt.plot([], [], 'k-o')


x0, y0 = 0, 0

data_handler = DataHandler('data/processed_data.csv', 'data/sensors.csv', 'data/area.txt', 'data/rooms.txt', 3, False)
# data_handler.save_data('data/processed_data.csv')
tellus_data = TellusData(data_handler, 1019, 552)
period = timedelta(hours=24)
start = tellus_data.start_time
end = start + period

circles = {}
for device_id in tellus_data.sensors:
    val = 0
    circle = plt.Circle((tellus_data.sensors[device_id]['x'], tellus_data.sensors[device_id]['y']),
                        15, color=color_map(round(val * 255 / 30)), alpha=0.3)
    circles[device_id] = circle
    plt.gca().add_patch(circle)


with writer.saving(fig, "writer_test.mp4", 100):
    while start < tellus_data.end_time:
        print('analysing day: ', start)
        for device_id in tellus_data.sensors:
            data = tellus_data.sensors[device_id]['data']
            date_filter = (data[DATA_TIMESTAMP] >= start) & (data[DATA_TIMESTAMP] < end)
            data = data.loc[date_filter]
            if len(data) != 0:
                val = max(data['pir'])
                circles[device_id].set_color(color_map(round(val * 255 / 30)))
        plt.title(start)
        start = start + period
        end = start + period
        writer.grab_frame()