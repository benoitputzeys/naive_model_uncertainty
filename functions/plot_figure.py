import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

def single_fig(X, y, xlabel, ylabel, ticks):
	# Plot the weekly average
	fig, axs = plt.subplots(1, 1, figsize = (15, 6))

	axs.plot(X, y, color = "blue", linewidth = 1)
	axs.set_ylabel(xlabel, size = 18)
	axs.set_xlabel(ylabel, size = 18)
	loc = plticker.MultipleLocator(base = 48 * 130)  # this locator puts ticks at regular intervals
	axs.grid(True)
	axs.xaxis.set_major_locator(loc)
	axs.tick_params(axis = "both", labelsize = 14)
	fig.autofmt_xdate(rotation = 15)
	plt.xticks(np.arange(1, len(X), 48 * 130), ticks)
	plt.show()

def band(X, y, ylabel, y_axis_label, color, alpha):
	zeros = np.zeros((336,))
	# Plot the mean and variation for each x.
	fig, axs = plt.subplots(1, 1, figsize = (12, 6))
	axs.fill_between(X,
					zeros,
					y,
	                alpha = alpha, color = color, label = ylabel)
	axs.set_ylabel(y_axis_label, size = 14)
	axs.grid(b = True, which = 'major'), axs.grid(b = True, which = 'minor', alpha = 0.2)
	axs.legend(loc = (0.4, 1.02),ncol=2)
	axs.set_xticks(np.arange(1, 385, 24))
	axs.set_xticklabels(["00:00\nMonday", "12:00",
	                    "00:00\nTuesday", "12:00",
	                    "00:00\nWednesday", "12:00",
	                    "00:00\nThursday", "12:00",
	                    "00:00\nFriday", "12:00",
	                    "00:00\nSaturday", "12:00",
	                    "00:00\nSunday", "12:00",
	                    "00:00", " "])
	axs.minorticks_on()
	axs.set_axisbelow(True)
	plt.show()

def model_and_data_bands(x_values, y_1, y_2, ylabel_1, ylabel_2, color_train, color_test, alpha):
	zeros = np.zeros((336,))
	# Plot the mean and variation for each x.
	fig, axs = plt.subplots(1, 1, figsize = (12, 6))
	axs.fill_between(x_values,
	                 zeros,
	                 y_1,
	                 alpha = alpha, color = color_train, label = ylabel_1)
	axs.fill_between(x_values,
	                 zeros,
	                 y_2,
	                 alpha = alpha, color = color_test, label = ylabel_2)
	axs.set_ylabel("Standard Deviations\nin the Electricity Load, GW", size = 14)
	axs.grid(b = True, which = 'major'), axs.grid(b = True, which = 'minor', alpha = 0.2)
	axs.legend(loc = (0.1, 1.02),ncol=2)
	axs.set_xticks(np.arange(1, 385, 24))
	axs.set_xticklabels(["00:00\nMonday", "12:00",
	                    "00:00\nTuesday", "12:00",
	                    "00:00\nWednesday", "12:00",
	                    "00:00\nThursday", "12:00",
	                    "00:00\nFriday", "12:00",
	                    "00:00\nSaturday", "12:00",
	                    "00:00\nSunday", "12:00",
	                    "00:00", " "])
	axs.minorticks_on()
	axs.set_axisbelow(True)
	plt.show()

def band_w_mean(x_values, stddevs, mean_errors, color, alpha):
	zeros = np.zeros((336,))
	# Plot the mean and variation for each x.
	fig, axs = plt.subplots(1, 1, figsize = (12, 6))
	axs.fill_between(x_values,
	                 zeros,
	                 stddevs,
	                 alpha = alpha, color = color, label = "Standard deviations of all projected errors")
	axs.plot(x_values, mean_errors, color = color, label = "Mean of all projected errors")
	axs.set_ylabel("Naive Method: Errors during training, GW", size = 14)
	axs.grid(b = True, which = 'major'), axs.grid(b = True, which = 'minor', alpha = 0.2)
	axs.legend(loc = (0.2, 1.02), ncol = 2)
	axs.set_xticks(np.arange(1, 385, 24))
	axs.set_xticklabels(["00:00\nMonday", "12:00",
	                    "00:00\nTuesday", "12:00",
	                    "00:00\nWednesday", "12:00",
	                    "00:00\nThursday", "12:00",
	                    "00:00\nFriday", "12:00",
	                    "00:00\nSaturday", "12:00",
	                    "00:00\nSunday", "12:00",
	                    "00:00", " "])
	axs.minorticks_on()
	axs.set_axisbelow(True)
	plt.show()


#def plot_prediction_w_band(X, prediction, true_load, stddev, errors, prediction_color, band_color, truth_color, alpha):
def prediction_w_band(dates, prediction, true_load, errors, stddev):
	zeros = np.zeros((336,))
	# Plot the result with the truth in blue/black and the predictions in orange.
	fig, axs = plt.subplots(2, 1, figsize = (12, 6))
	axs[0].grid(True)
	axs[0].plot(dates, prediction, label = "Naive prediction", color = "orange")

	# Use the orange band from Friday 00:30 to Sunday 23:30 (start at SP 194, end at SP 336)
	axs[0].fill_between(dates.iloc[:143],
						prediction[:143].values + stddev[193:].values,
	                    prediction[:143].values - stddev[193:].values,
	                    alpha = 0.2, color = "orange")

	# Use the orange band from Monday 00:00 (SP = 1) to Thursday 13:30 (SP=173)
	axs[0].fill_between(dates.iloc[143:],
						prediction[143:].values + stddev[:193].values,
	                    prediction[143:].values - stddev[:193].values,
	                    label = "+-1 x\nStandard Deviation", alpha = 0.2, color = "orange")
	axs[0].plot(dates,
	            true_load,
	            label = "Test set", color = "black")
	axs[0].set_ylabel("Load, GW", size = 14)
	loc = plticker.MultipleLocator(base = 47)  # Puts ticks at regular intervals
	axs[0].xaxis.set_major_locator(loc)
	axs[0].plot(30, 30, label = "Absolute error", color = "red")

	# plot the errors
	axs[1].grid(True)
	axs[1].plot(dates,
	            abs(errors),
	            label = "Absolute error", alpha = 1, color = "red")
	axs[1].set_xlabel('2019', size = 14)
	axs[1].set_ylabel('Error, GW', size = 14)

	# Use the orange band from Friday 00:30 to Sunday 23:30 (start at SP 194, end at SP 336)
	axs[1].fill_between(dates.iloc[:143],
	                     zeros[:143] + stddev[193:].values,
	                     alpha = 0.2, color = "orange")

	# Use the orange band from Monday 00:00 (SP = 1) to Thursday 13:30 (SP=173)
	axs[1].fill_between(dates.iloc[143:],
	                     zeros[143:] + stddev[:193].values,
	                     label = "1 x\nStandard Deviation", alpha = 0.2, color = "orange")

	# Include additional details such as tick intervals, rotation, legend positioning and grid on.
	axs[0].grid(True), axs[1].grid(True)
	loc = plticker.MultipleLocator(base = 48)  # Puts ticks at regular intervals
	axs[0].xaxis.set_major_locator(loc), axs[1].xaxis.set_major_locator(loc)
	fig.autofmt_xdate(rotation = 0)
	axs[0].legend(loc = (0.1, 1.09),ncol=4)
	axs[0].set_axisbelow(True), axs[1].set_axisbelow(True)
	plt.xticks(np.arange(1, 338, 48), ["00:00\nJune-01", "00:00\nJune-01", "00:00\nJune-02",
	                                   "00:00\nJune-03", "00:00\nJune-04", "00:00\nJune-05",
	                                   "00:00\nJune-06", "00:00\nJune-07"])
	plt.show()

def superposed_bands(x_values, y_1, y_2, ylabel_1, ylabel_2, y_axis_label, color_train, color_test, alpha):
	zeros = np.zeros((336,))
	# Plot the mean and variation for each x.
	fig, axs = plt.subplots(1, 1, figsize = (12, 6))
	axs.fill_between(x_values,
	                 zeros,
	                 y_1,
	                 alpha = alpha, color = color_train, label = ylabel_1)
	axs.fill_between(x_values,
	                 zeros,
	                 y_2,
	                 alpha = alpha, color = color_test, label = ylabel_2)
	axs.set_ylabel(y_axis_label, size = 14)
	axs.grid(b = True, which = 'major'), axs.grid(b = True, which = 'minor', alpha = 0.2)
	axs.legend(loc = (0.15, 1.02),ncol=2)
	axs.set_xticks(np.arange(1, 385, 24))
	axs.set_xticklabels(["00:00\nMonday", "12:00",
	                    "00:00\nTuesday", "12:00",
	                    "00:00\nWednesday", "12:00",
	                    "00:00\nThursday", "12:00",
	                    "00:00\nFriday", "12:00",
	                    "00:00\nSaturday", "12:00",
	                    "00:00\nSunday", "12:00",
	                    "00:00", " "])
	axs.minorticks_on()
	axs.set_axisbelow(True)
	plt.show()

def change_in_stddev(dates, change_1, change_2, y_axis_label, ylabel_train, ylabel_test):
	fig, axs = plt.subplots(1, 1, figsize = (15, 6))

	axs.plot(dates, change_1, color = "blue", linewidth = 1, label = ylabel_train)
	axs.plot(dates, change_2, color = "black", linewidth = 1, label = ylabel_test)
	axs.grid(b = True, which = 'major'), axs.grid(b = True, which = 'minor', alpha = 0.2)
	axs.legend(loc = (0.1, 1.02), ncol = 2)
	axs.set_xticks(np.arange(1, 385, 24))
	axs.set_ylabel(y_axis_label, size = 14)
	axs.set_xticklabels(["00:00\nMonday", "12:00",
	                     "00:00\nTuesday", "12:00",
	                     "00:00\nWednesday", "12:00",
	                     "00:00\nThursday", "12:00",
	                     "00:00\nFriday", "12:00",
	                     "00:00\nSaturday", "12:00",
	                     "00:00\nSunday", "12:00",
	                     "00:00", " "])
	axs.minorticks_on()
	axs.set_axisbelow(True)
	plt.show()