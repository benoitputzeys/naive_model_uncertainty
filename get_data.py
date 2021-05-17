from entsoe import EntsoePandasClient
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Use the key provided by entsoe to access the data
client = EntsoePandasClient(api_key="b7a8a6e4-3d85-427a-8790-30ab56538691")

# Define the time interval from where the data should be loaded.
start = pd.Timestamp('20160101', tz="Europe/London")
end = pd.Timestamp('20200615', tz="Europe/London")
cc = "GB"

# Load the data into a variable.
raw_load = client.query_load(cc, start = start ,end = end)

# Create a csv file and save the load in it.
Path('data_preprocessing/raw_load.csv').touch()
raw_load.to_csv("data_preprocessing/raw_load.csv")

# Plot the raw data. Divide by 1000 to express everything in GW.
fig1, axs1=plt.subplots(1,1,figsize=(12,6))
axs1.plot(raw_load/1000, color = "blue", linewidth = 0.5)
axs1.set_ylabel("Load in the UK (Raw Data), GW",size = 16)
axs1.set_xlabel("Date", size = 16)
axs1.axes.tick_params(labelsize = 14)
axs1.grid(True)
fig1.show()
plt.show()

load_GB_processed = raw_load.copy()

# Shift the data by 1 SP.
not_shifted_raw = np.array(raw_load)[1:]
shifted_raw = load_GB_processed.shift(+1)[1:]

# Plot the difference in electricity load from one SP to the next.
fig21, axs21=plt.subplots(1,1,figsize=(12,6))
axs21.plot((shifted_raw-not_shifted_raw)/1000, color = "blue", linewidth = 0.5)
axs21.set_ylabel("Difference of the load, GW",size = 16)
axs21.set_xlabel("Date", size = 16)
axs21.axes.tick_params(labelsize = 14)
axs21.grid(True)
fig21.show()
plt.show()

counter = 0
# Filter some erroneous data out and replace by the load from the previous SP.
for i in range(1,len(load_GB_processed)-1):
    if (np.abs(load_GB_processed[i] - load_GB_processed[i - 1]) > 10000) & (np.abs(load_GB_processed[i] - load_GB_processed[i + 1])>10000):
        load_GB_processed[i] = load_GB_processed[i - 1]
        counter +=1

# Create plot of processed data.
fig2, axs2=plt.subplots(1,1,figsize=(12,6))
axs2.plot(load_GB_processed/1000, color = "blue", linewidth = 0.5)
axs2.set_ylabel("Load in the UK (Processed Data), GW",size = 16)
axs2.set_xlabel("Date", size = 16)
axs2.axes.tick_params(labelsize = 14)
axs2.grid(True)
fig2.show()
plt.show()