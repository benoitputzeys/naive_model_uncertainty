import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

def plot_single_fig(X, y, xlabel, ylabel, ticks):
	# Plot the weekly average
	fig, axs = plt.subplots(1, 1, figsize = (15, 6))

	axs.plot(X, y, color = "blue", linewidth = 1)
	axs.set_ylabel(xlabel, size = 18)
	axs.set_xlabel(ylabel, size = 18)
	loc = plticker.MultipleLocator(base = 48 * 130)  # this locator puts ticks at regular intervals
	axs.grid(True)
	axs.xaxis.set_major_locator(loc)
	axs.tick_params(axis = "both", labelsize = 14)
	fig.autofmt_xdate(rotation = 0)
	plt.xticks(np.arange(1, len(X), 48 * 130), ticks)
	plt.show()

def plot_band(X, y, ylabel, color, alpha):
	zeros = np.zeros((336,))
	# Plot the mean and variation for each x.
	fig, axs = plt.subplots(1, 1, figsize = (12, 6))
	axs.fill_between(X,
					zeros,
					y/1000,
	                alpha = alpha, color = color, label = ylabel)
	axs.set_ylabel("Electricity Load Training Set, GW", size = 14)
	axs.grid(b = True, which = 'major'), axs.grid(b = True, which = 'minor', alpha = 0.2)
	axs.legend(fontsize = 12)
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
	axs.set_ylim([0, 6])
	plt.show()

def plot_superposed_band(dates, y_1, y_2, ylabel_1, ylabel_2, color_train, color_test, alpha):
	zeros = np.zeros((336,))
	# Plot the mean and variation for each x.
	fig, axs = plt.subplots(1, 1, figsize = (12, 6))
	axs.fill_between(dates,
					zeros,
					y_1 / 1000,
	                alpha = alpha, color = color_train, label = ylabel_1)
	axs.fill_between(dates,
	                 zeros,
	                 y_2 / 1000,
	                 alpha = alpha, color = color_test, label = ylabel_2)
	axs.set_ylabel("Electricity Load Training Set, GW", size = 14)
	axs.grid(b = True, which = 'major'), axs.grid(b = True, which = 'minor', alpha = 0.2)
	axs.legend(loc = (0.2, 1.02),ncol=2)
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
	axs.set_ylim([0, 6])
	plt.show()

def plot_band_w_mean(X, y, mean, ylabel, color, alpha):
	zeros = np.zeros((336,))
	# Plot the mean and variation for each x.
	fig, axs = plt.subplots(1, 1, figsize = (12, 6))
	axs.fill_between(X,
					zeros,
					y/1000,
	                alpha = alpha, color = color, label = ylabel)
	axs.plot(X, mean/1000, color = color, label = "Mean of all projected errors")
	axs.set_ylabel("Electricity Load Training Set, GW", size = 14)
	axs.grid(b = True, which = 'major'), axs.grid(b = True, which = 'minor', alpha = 0.2)
	axs.legend(fontsize = 12)
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
def plot_prediction_w_band(dates, prediction, true_load, errors, stddev):
	zeros = np.zeros((336,))
	# Plot the result with the truth in blue/black and the predictions in orange.
	fig, axs = plt.subplots(2, 1, figsize = (12, 6))
	axs[0].grid(True)
	axs[0].plot(dates, prediction, label = "Naive prediction", color = "orange")

	# Use the orange band from Thursday 14:00 to Sunday 23:30 (start at SP 173)
	axs[0].fill_between(dates.iloc[:163],
	                     prediction[:163].values + stddev[173:].values,
	                     prediction[:163].values - stddev[173:].values,
	                     alpha = 0.2, color = "orange")

	# Use the orange band from Monday 00:00 (SP = 1) to Thursday 13:30 (SP=173)
	axs[0].fill_between(dates.iloc[163:],
	                     prediction[163:].values + stddev[:173].values,
	                     prediction[163:].values - stddev[:173].values,
	                     label = "+-1 x\nStandard Deviation", alpha = 0.2, color = "orange")
	axs[0].plot(dates,
	            true_load,
	            label = "Test set", color = "black")
	axs[0].set_ylabel("Load, GW", size = 14)
	loc = plticker.MultipleLocator(base = 47)  # Puts ticks at regular intervals
	axs[0].xaxis.set_major_locator(loc)
	axs[0].plot(30, 30, label = "Error", color = "red")

	# plot the errors
	axs[1].grid(True)
	axs[1].plot(dates,
	            abs(errors),
	            label = "Absolute error", alpha = 1, color = "red")
	axs[1].set_xlabel('2019', size = 14)
	axs[1].set_ylabel('Error, GW', size = 14)

	# Use the orange band from Thursday 14:00 to Sunday 23:30 (start at SP 173)
	axs[1].fill_between(dates.iloc[:163],
	                     zeros[:163] + stddev[173:].values,
	                     alpha = 0.2, color = "orange")

	# Use the orange band from Monday 00:00 (SP = 1) to Thursday 13:30 (SP=173)
	axs[1].fill_between(dates.iloc[163:],
	                     zeros[163:] + stddev[:173].values,
	                     label = "1 x\nStandard Deviation", alpha = 0.2, color = "orange")

	# Include additional details such as tick intervals, rotation, legend positioning and grid on.
	axs[0].grid(True), axs[1].grid(True)
	loc = plticker.MultipleLocator(base = 48)  # Puts ticks at regular intervals
	axs[0].xaxis.set_major_locator(loc), axs[1].xaxis.set_major_locator(loc)
	fig.autofmt_xdate(rotation = 0)
	axs[0].legend(loc = (0.2, 1.09),ncol=4)
	axs[0].set_axisbelow(True), axs[1].set_axisbelow(True)
	plt.xticks(np.arange(1, 338, 48), ["14:00\n07/25", "14:00\n07/26", "14:00\n07/27",
	                                   "14:00\n07/28", "14:00\n07/29", "14:00\n07/30",
	                                   "14:00\n07/31", "14:00\n08/01"])
	plt.show()