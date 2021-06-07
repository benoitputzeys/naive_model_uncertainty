import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from functions import plot_figure

# Get the X (containing the features) and y (containing the labels) values
X = pd.read_csv('data/data_preprocessing/X.csv', delimiter = ',')
y = pd.read_csv('data/data_preprocessing/y.csv', delimiter = ',')
dates = X.iloc[:, 0]

# Split data into train set and test set.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1, shuffle = False)

# Calculate the errors between prediction and true values
error_train = X_train.iloc[:, -1] - y_train.iloc[:, -1]
error_test = X_test.iloc[:, -1] - y_test.iloc[:, -1]

# Calculate mean and standard deviations of the errors
error_df = pd.DataFrame({'SP': X['Settlement Period']+(48*X["Day of Week"]),
                         'Error': error_train})
error_df_train = error_df.iloc[:62476]

# Compute the mean and variation for each x.
error_stats = pd.DataFrame({'Index': np.linspace(1, 336, 336), 'Mean': np.linspace(1, 336, 336), 'Stddev': np.linspace(1, 336, 336)})

for i in range(1,337):
    error_stats.iloc[i-1, 1] = np.mean(error_df_train[error_df_train["SP"] == i].iloc[:, -1])
    error_stats.iloc[i-1, 2] = np.std(error_df_train[error_df_train["SP"] == i].iloc[:, -1])

# Plot training
ylabel = "Electricity Load Training Set, GW"
plot_figure.plot_prediction_w_band(dates.iloc[-len(X_test):-len(X_test) + 48 * 7],
                                   X_test.iloc[:48*7, 3] / 1000,
                                   y_test.iloc[:48*7, 1] / 1000,
                                   error_test.iloc[:48*7] / 1000,
                                   error_stats.iloc[:, 2] / 1000)

# Compare stddev from the errors from the model and from stddev derived from true values
df_stats_train = pd.read_csv("data/mean_and_stddevs_train_set.csv")
ylabel_model = "Standard deviations from the model, GW"
ylabel_data = "Standard deviations from the data, GW"
plot_figure.plot_superposed_band(dates.iloc[-len(X_test):-len(X_test) + 48 * 7],
                                 error_stats.iloc[:, 2],
                                 df_stats_train.iloc[:, 3],
                                 ylabel_model,
                                 ylabel_data,
                                 "orange",
                                 "blue",
                                 0.2)
