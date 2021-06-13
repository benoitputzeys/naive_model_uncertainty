from entsoe import EntsoePandasClient
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def get_data():
    # Use the key provided by entsoe to access the data
    client = EntsoePandasClient(api_key="b7a8a6e4-3d85-427a-8790-30ab56538691")

    # Define the time interval from where the data should be loaded.
    start = pd.Timestamp('20160101', tz="Europe/London")
    end = pd.Timestamp('20200615', tz="Europe/London")
    cc = "GB"

    # Load the data into a variable.
    raw_load = client.query_load(cc, start=start, end=end)

    # Create a csv file and save the load in it.
    Path('data_preprocessing/raw_load.csv').touch()
    raw_load.to_csv("data_preprocessing/raw_load.csv")

    print("Data successfully saved in a csv file.")
    return raw_load

def get_processed_data(raw_load):
    # Shift the data by 1 SP.
    not_shifted_raw = np.array(raw_load)[1:]
    load_GB_processed = raw_load.copy()
    shifted_raw = load_GB_processed.shift(+1)[1:]

    # Plot the difference in electricity load from one SP to the next.
    fig21, axs21 = plt.subplots(1, 1, figsize=(12, 6))
    axs21.plot((shifted_raw - not_shifted_raw) / 1000, color="blue", linewidth=0.5)
    axs21.set_ylabel("Difference of the load, GW", size=16)
    axs21.set_xlabel("Date", size=16)
    axs21.axes.tick_params(labelsize=14)
    axs21.grid(True)
    fig21.show()
    plt.show()

    counter = 0
    # Filter some erroneous data out and replace by the load from the previous SP.
    for i in range(1, len(load_GB_processed) - 1):
        if (np.abs(load_GB_processed[i] - load_GB_processed[i - 1]) > 10000) & (
                np.abs(load_GB_processed[i] - load_GB_processed[i + 1]) > 10000):
            load_GB_processed[i] = load_GB_processed[i - 1]
            counter += 1

    # In case of duplicates, delete them.
    load_GB_processed = load_GB_processed.loc[~load_GB_processed.index.duplicated(keep='first')]

    # For long periods, use loads from previous week
    load_GB_processed[60894:60896] = raw_load[60894 - 48 * 7:60896 - 48 * 7]
    counter += 60896 - 60894

    load_GB_processed[60397:60423] = raw_load[60397 - 48 * 7:60423 - 48 * 7]
    counter += abs(60423 - 60397)

    load_GB_processed[62431:62439] = raw_load[62431 - 48 * 7:62439 - 48 * 7]
    counter += abs(62439 - 62431)

    load_GB_processed[62382:62391] = raw_load[62382 - 48 * 7:62391 - 48 * 7]
    counter += abs(62391 - 62382)

    load_GB_processed[56370:56372] = raw_load[56370 - 48 * 7:56372 - 48 * 7]
    counter += abs(56372 - 56370)

    load_GB_processed[51772:51784] = raw_load[51772 - 48 * 7:51784 - 48 * 7]
    counter += abs(51784 - 51772)

    load_GB_processed[59273:59280] = raw_load[59273 - 48 * 7:59280 - 48 * 7]
    counter += abs(59280 - 59273)

    load_GB_processed[56272:56274] = raw_load[56272 - 48 * 7:56274 - 48 * 7]
    counter += abs(56274 - 56272)

    load_GB_processed[56738:56739] = raw_load[56738 - 48 * 7:56739 - 48 * 7]
    counter += abs(56739 - 56738)

    # Show how many SPs were changed with respect to the initial data.
    percentage = counter / len(raw_load) * 100
    print("The number of processed SPs is", counter, "which corresponds to", round(percentage, 2),
          "% of the initial dataset.")
    return load_GB_processed

def main():

    raw_load = get_data()

    # Plot the raw data. Divide by 1000 to express everything in GW.
    fig1, axs1 = plt.subplots(1, 1, figsize=(12, 6))
    axs1.plot(raw_load / 1000, color="blue", linewidth=0.5)
    axs1.set_ylabel("Load in the UK (Raw Data), GW", size=16)
    axs1.set_xlabel("Date", size=16)
    axs1.axes.tick_params(labelsize=14)
    axs1.grid(True)
    fig1.show()
    plt.show()

    load_GB_processed = get_processed_data(raw_load)

    # Create plot of processed data.
    fig2, axs2 = plt.subplots(1, 1, figsize=(12, 6))
    axs2.plot(load_GB_processed / 1000, color="blue", linewidth=0.5)
    axs2.set_ylabel("Load in the UK (Processed Data), GW", size=16)
    axs2.set_xlabel("Date", size=16)
    axs2.axes.tick_params(labelsize=14)
    axs2.grid(True)
    fig2.show()
    plt.show()

    # Create a csv file and save the load in it.
    Path('data_preprocessing/processed_load.csv').touch()
    load_GB_processed.to_csv("data_preprocessing/processed_load.csv")

    print("Processed data successfully saved in a csv file.")

if __name__ == '__main__':
    main()