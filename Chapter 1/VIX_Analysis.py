# Importing the required library
import matplotlib.pyplot as plt
import pandas as pd

# Setting the beginning and end of the historical data
# start_date = '1990-01-01'
# end_date = '2023-01-23'
# vix = pdr.DataReader('VIXCLS', 'fred', start_date, end_date)
# vix.to_pickle("data/vix.pickle")

vix = pd.read_pickle("data/vix.pickle")
count_nan = vix['VIXCLS'].isnull().sum()
vix = vix.dropna()
vix = vix.diff(periods=1, axis=0)
vix = vix.iloc[1:, :]

# Calculating the mean of the dataset
mean = vix["VIXCLS"].mean()
# Printing the result
print('The mean of the dataset = ' + str(mean))

plt.plot(vix[-250:], color='black', linewidth=1.5, label='Change in VIX')
# Plotting a red dashed horizontal line that is equal to mean
plt.axhline(y=mean, color='red', linestyle='dashed')
# Calling a grid to facilitate the visual component
plt.grid()
# Calling the legend function so it appears with the chart
plt.legend()
# Calling the plot
plt.savefig("pngs/ch01_01_vix.png")
plt.close()

print(vix)
