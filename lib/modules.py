# %% 
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science', 'notebook'])
import csv

def load_dataset(csv_file, country):
	"""
	Loads a dataset from a CSV file and returns the data for a specific country.

	Parameters:
	- country (str): The name of the country to load the data for.

	Returns:
	- data (list): A list of rows from the dataset that match the specified country.
	"""
	# dataset from https://www.kaggle.com/datasets/amanarora/obesity-among-adults-by-country-19752016/code

	with open(csv_file, 'r') as f:
		reader = csv.reader(f)
		header = next(reader)

		data = list(filter(lambda data: data[1] == country, reader))
	return data

def extract_sexes(data, sex="Both sexes"):
	"""
	Extracts data based on the specified sex.

	Parameters:
	- data (list): A list of data to filter.
	- sex (str, optional): The sex to filter by. Defaults to "Both sexes". Other values are: "Female", "Male"

	Returns:
	- list: A list of filtered data.

	"""
	sex = sex.capitalize()

	if sex == "Both sexes":
		return list(filter(lambda data: data[-1] == "Both sexes", data))
	elif sex == "Female":
		return list(filter(lambda data: data[-1] == "Female", data))
	elif sex == "Male":
		return 	list(filter(lambda data: data[-1] == "Male", data))


def statistical_string_to_list(statistical_string):
	"""
	Get the percentage value from a string.

	Parameters:
	- statistical_string (str): A string with the format "12, [1, 2]"

	Returns:
	- list: A list with the percentage value and the confidence interval"
	"""
	statistical_string = statistical_string.split(' ')
	mean = float(statistical_string[0])
	std = statistical_string[1][1:-1].split('-')
	std = [float(std[0]), float(std[1])]

	return	[mean, std]


def data_to_plot(data_to_process):
	"""
	Converts the data to a plotable format.

	Parameters:
	- data_to_process (list): A list of data to process.

	Returns:
	- list: A list with the year, mean and uncertainty
	"""
	year = [int(data[2]) for data in data_to_process]
	mean = np.array([statistical_string_to_list(data[3])[0] for data in data_to_process])
	confidence_interval = np.array([statistical_string_to_list(data[3])[1] for data in data_to_process])

	uncertainty = np.array([mean - confidence_interval[:,0], confidence_interval[:, 1] - mean])

	return year, mean, uncertainty


def plot_data(csv_file, country, sex="all"):
	"""
	Plots data from a CSV file for a specified country and sex.

	Parameters:
	- csv_file (str): The path to the CSV file containing the data.
	- country (str): The country for which the data will be plotted.
	- sex (str, optional): The sex for which the data will be plotted. Defaults to "all".

	Returns:
	None
	"""

	data = load_dataset(csv_file, country)

	sex = sex.capitalize()

	fig, ax = plt.subplots(figsize=(10, 6))

	plt.title(f"Prevalence of obesity among adults, BMI $\geq$ 30, {country}")
	plt.grid(linestyle='--')
	plt.xlabel('Year')
	plt.ylabel('Percentage %')

	if sex == "All":
		data_both = extract_sexes(data, sex="Both sexes")
		data_female = extract_sexes(data, sex="Female")
		data_male = extract_sexes(data, sex="Male")

		year, mean_both, uncertainty_both = data_to_plot(data_both)
		_, mean_female, uncertainty_female = data_to_plot(data_female)
		_, mean_male, uncertainty_male = data_to_plot(data_male)

		ax.errorbar(year, mean_both, yerr=uncertainty_both, linewidth=1, capsize=5)
		ax.errorbar(year, mean_female, yerr=uncertainty_female, linewidth=1, capsize=5)
		ax.errorbar(year, mean_male, yerr=uncertainty_male, linewidth=1, capsize=5)

		plt.legend(['Both sexes', 'Female', 'Male'])
		plt.savefig(f'{country} - all.png', dpi=400)

	elif sex in ["Female", "Male", "Both sexes"]:
		data_selected = extract_sexes(data, sex=sex)
		year, mean, uncertainty = data_to_plot(data_selected)
		ax.errorbar(year, mean, yerr=uncertainty, linewidth=1, capsize=5, label=sex)
		
		plt.legend()
		plt.savefig(f'{country} - {sex}.png', dpi=400)
	plt.show()

# %% 
if __name__ == '__main__':
	csv_file = '../dataset/obesity-cleaned.csv'
	country = "Chile"
	plot_data(csv_file, country=country, sex="all")

# %% 