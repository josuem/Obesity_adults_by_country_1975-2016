# %% 
import lib

if __name__ == "__main__":
	csv_file = './dataset/obesity-cleaned.csv'
	country = "Chile"
	
	# To see the dataset
	data = lib.load_dataset(csv_file, country)

	# To create plots
	lib.plot_data(csv_file, country=country, sex="Female")
	lib.plot_data(csv_file, country=country, sex="Male")
	lib.plot_data(csv_file, country=country, sex="all")

# %% 
