import numpy as np
import pandas as pd
from functions import plot_figure

# Get the processed data.
y = pd.read_csv('data/data_preprocessing/y.csv')
y = y.set_index("Time")
dates = y.index
series = y.iloc[:, -1]/1000

# Compute the mean for each week
mean_each_week = series.copy()
counter = 0
for i in range(len(y)-1):
    mean_each_week[i-counter:i+1] = np.mean(series[i-counter:i+1])
    counter = counter + 1
    if (y["Day of Week"][i] == 6) & (y["Day of Week"][i+1]==0):
        counter = 0
mean_each_week.iloc[-1]=mean_each_week.iloc[-2]

# Plot weekly mean
ticks = ["2016-01", "2016-05", "2016-09",
        "2017-01", "2017-06", "2017-11",
        "2018-02", "2018-06", "2018-11",
        "2019-03", "2019-07", "2019-12", "2020-04"]
plot_figure.plot_single_fig(dates, mean_each_week, "Date", "Weekly Average, GW", ticks)

# Shift the load so that every week has a mean load of 0W
shifted_load = series - mean_each_week

# Modify the SP to go from 1 to 336 for each week (instead of 1 to 48 for each day)
shifted_load = pd.DataFrame({'SP': y['Settlement Period']+(48*y["Day of Week"]), 'Load': shifted_load.values})

# Split the data int training and test set
shifted_load_train = shifted_load.iloc[31238:62476]
shifted_load_test = shifted_load.iloc[62476:62476+7810]

# Compute the mean and variation for each x.
df_stats_train = pd.DataFrame({'Index': np.linspace(1, 336, 336), 'Mean': np.linspace(1, 336, 336), 'Stddev': np.linspace(1, 336, 336)})
df_stats_test = pd.DataFrame({'Index': np.linspace(1, 336, 336), 'Mean': np.linspace(1, 336, 336), 'Stddev': np.linspace(1, 336, 336)})

# Fill the respective dataframe with the mean/stddev of the respective settlement period (SP)
for i in range(1,337):
    df_stats_train.iloc[i-1, 1] = np.mean(shifted_load_train[shifted_load_train["SP"] == i].iloc[:, -1])
    df_stats_train.iloc[i-1, 2] = np.std(shifted_load_train[shifted_load_train["SP"] == i].iloc[:, -1])

for i in range(1, 337):
    df_stats_test.iloc[i-1, 1] = np.mean(shifted_load_test[shifted_load_test["SP"] == i].iloc[:, -1])
    df_stats_test.iloc[i-1, 2] = np.std(shifted_load_test[shifted_load_test["SP"] == i].iloc[:, -1])

# Plot training
ylabel = "Electricity Load Training Set, GW"
plot_figure.plot_band(df_stats_train.iloc[:, 0], (+df_stats_train.iloc[:, 2]), ylabel, "blue", 0.2)

# Plot test data
ylabel = "Electricity Load Test Set, GW"
plot_figure.plot_band(df_stats_test.iloc[:, 0], (+df_stats_test.iloc[:, 2]), ylabel, "black", 0.2)

# Plot both train and test data
# TODO put the dates of the stddevs
ylabel_train = "Electricity Load Train Set, GW"
ylabel_test = "Electricity Load Test Set, GW"
plot_figure.plot_superposed_band(df_stats_test.iloc[:, 0],
                                 (+df_stats_train.iloc[:, 2]),
                                 (+df_stats_test.iloc[:, 2]),
                                 ylabel_train,
                                 ylabel_test,
                                 "blue",
                                 "black",
                                 0.2)

# Save training and test data
df_stats_train.to_csv("data/mean_and_stddevs_train_set.csv")
df_stats_test.to_csv("data/mean_and_stddevs_test_set.csv")
