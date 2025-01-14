# %%
# todo acount for coagulation and dillution

import numpy as np
from matplotlib import pyplot as plt, dates
import pytz
from scipy.optimize import curve_fit
import os
from datetime import datetime
import json
from datacula.lake.datalake import DataLake
from datacula.lake import processer, plot
from datacula import loader
from datacula.time_manage import time_str_to_epoch

# preferred settings for plotting
plt.rcParams.update({'text.color': "#333333",
                     'axes.labelcolor': "#333333",
                     "figure.figsize": (6,4),
                     "font.size": 14,
                     "axes.edgecolor": "#333333",
                     "axes.labelcolor": "#333333",
                     "xtick.color": "#333333",
                     "ytick.color": "#333333",
                     "pdf.fonttype": 42,
                     "ps.fonttype": 42})

#%%
data_path = 'C:\\Users\\kkgor\\OneDrive\\Projects\\epcape\\server_files'
# make plots folder
plot_path = os.path.join(data_path, 'plots')
if not os.path.exists(plot_path):
    os.makedirs(plot_path)


# epoch_start = datetime.fromisoformat('2023-04-16T00:00').timestamp()
# epoch_end = datetime.fromisoformat('2023-04-28T00:00').timestamp()


# # load json file with lake settings
# lake_settings_path = os.path.join(data_path, 'lake_settings.json')

settings = {
   "GCVI_data": {
        "instrument_name": "GCVI",
        "data_stream_name": "GCVI",
        "data_loading_function": "general_load",
        "relative_data_folder": "GCVI_data",
        "last_file_processed": "",
        "last_timestamp_processed": "",
        "skipRowsDict": 0,
        "Time_shift_sec": 0,
        "timezone_identifier": "UTC",
        "data_checks": {
            "characters": [100,300],
            "skip_rows": 11,
            "skip_end": 0,
            "char_counts": { "/": 2}
        },
        "data_header": [
            "visibility",
            "Cloud_Sample",
            "precp_stat",
            "air_speed",
            "Humidity_[%]",
            "Temperature_[C]",
        ],
        "data_column": [
            2,
            3,
            4,
            5,
            6,
            7,
        ],
        "time_column": [0, 1],
        "time_format": "%y/%m/%d %H:%M:%S",
        "filename_regex": "GCVI*.dat",
        "base_interval_sec": 1,
        "data_delimiter": "\t"
        }
}

# Initialize the data lake
my_lake = DataLake(settings=settings, path=data_path)

my_lake.update_datastream()
my_lake.info()
# %% calculate mean properties of smps 2d data 
# my_lake = processer.sizer_mean_properties(my_lake, "smps_2D")



# time range
time_format = "%m/%d/%Y %H:%M:%S"
epoch_start = time_str_to_epoch('10/18/2023 00:0:00', time_format, 'UTC')
epoch_end = time_str_to_epoch('11/01/2023 06:00:00', time_format, 'UTC')
# epoch_start = datetime.fromisoformat('2023-09-26T013:00').timestamp()
# epoch_end = datetime.fromisoformat('2023-09-26T15:00').timestamp()
timezone = pytz.timezone('UTC')


my_lake.reaverage_datastreams(60*1, epoch_start=epoch_start, epoch_end=epoch_end)

fig, ax = plt.subplots()
plot.timeseries(
    ax,
    my_lake,
    'GCVI',
    'visibility',
    label='GCVI',
    shade=False)

ax.minorticks_on()
plt.tick_params(rotation=-25)
ax.set_ylabel('Visibility (km?)')
# ax.set_xlim((epoch_start, epoch_end))
ax.set_xlabel('UTC Time')
ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d', tz=timezone))
# ax.xaxis.set_minor_formatter(dates.DateFormatter('%d', tz=mdt_timezone))
ax.set_ylim((0,20000))
ax.grid()
ax.legend()
fig.tight_layout()
fig.savefig(plot_path + '\\visiblity.png', dpi=300)

fig, ax = plt.subplots()
plot.timeseries(
    ax,
    my_lake,
    'GCVI',
    'Cloud_Sample',
    label='GCVI',
    shade=False)

ax.minorticks_on()
plt.tick_params(rotation=-25)
ax.set_ylabel('Cloud Sample')
# ax.set_xlim((epoch_start, epoch_end))
ax.set_xlabel('UTC Time')

ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d', tz=timezone))
# ax.xaxis.set_minor_formatter(dates.DateFormatter('%d', tz=mdt_timezone))
# ax.set_ylim((0,2000))
ax.grid()
ax.legend()
fig.tight_layout()
fig.savefig(plot_path + '\\Cloud.png', dpi=300)

fig, ax = plt.subplots()
plot.timeseries(
    ax,
    my_lake,
    'GCVI',
    'Humidity_[%]',
    label='GCVI',
    shade=False)

ax.minorticks_on()
plt.tick_params(rotation=-25)
ax.set_ylabel('Humidity (%)')
# ax.set_xlim((epoch_start, epoch_end))
ax.set_xlabel('UTC Time')

ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d', tz=timezone))
# ax.xaxis.set_minor_formatter(dates.DateFormatter('%d', tz=mdt_timezone))
# ax.set_ylim((0,2000))
ax.grid()
ax.legend()
fig.tight_layout()
fig.savefig(plot_path + '\\GCVI_humidity.png', dpi=300)




# %%
