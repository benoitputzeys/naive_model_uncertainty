import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import datetime as dt

# Load the data into a dataframe called df.
load = pd.read_csv("processed_load.csv")
load = load.rename(columns={"Unnamed: 0": "Timestamp"}, errors="raise")
load = load.rename(columns={"0": "Load"}, errors="raise")

# Get rid of the seconds in the timestamp, only display up until minutes.
load["Timestamp"] = [dt.datetime.strptime(load.iloc[i,0][0:16], '%Y-%m-%d %H:%M') for i in range(len(load))]
load["Time"] = load["Timestamp"]
load = load.set_index(["Time"])

# Create date relevant features.
shift_load = pd.DataFrame()
shift_load["Predicted_load"] = load["Load"].shift(+48*7)

# Replace nan values with the mean from the respective column.
replace_nan = SimpleImputer(missing_values=np.nan, strategy='mean')
replace_nan.fit(shift_load)
shift_load = pd.DataFrame(replace_nan.transform(shift_load))

# Create date relevant features.
X = pd.DataFrame()
X["Settlement Period"] = load['Timestamp'].dt.hour*2+1+load['Timestamp'].dt.minute/30
X["Day of Week"] = load['Timestamp'].dt.weekday
X["Predicted_load"] = shift_load.values
X["Settlement Period"] = load['Timestamp'].dt.hour*2+1+load['Timestamp'].dt.minute/30

# Create the final y (output) values which is the actual load.
y = pd.DataFrame()
y["Settlement Period"] = load['Timestamp'].dt.hour*2+1+load['Timestamp'].dt.minute/30
y["Day of Week"] = load['Timestamp'].dt.weekday
y["Predicted_load"] = load["Load"].values
y["Settlement Period"] = load['Timestamp'].dt.hour*2+1+load['Timestamp'].dt.minute/30

# Save the final input/prediction (X) and output/ground truth (y) in csv files.
X.to_csv("X.csv")
y.to_csv("y.csv")
