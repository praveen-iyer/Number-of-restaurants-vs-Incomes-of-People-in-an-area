# Importing all required modules/libraries
import requests
from bs4 import BeautifulSoup
import re
import json
import os
import sys
import pandas as pd

# Scrape all standard ZIP codes in Los Angeles which have a population greater than 0.
def get_inhabited_zip_codes_in_LA():
	url = "https://www.zip-codes.com/city/ca-los-angeles.asp"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	table = soup.find('table')
	table_body = table.find('tbody')
	rows = table.find_all('tr')
	data = []
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    data.append([ele for ele in cols if ele])
	zips = []
	for r in data:
		try:
			if r[0][:9] == 'ZIP Code ':
				if r[1] == 'Standard' and r[3]!='0':
					zips.append(r[0][9:])
		except:
			pass
	return zips

# Scrape median, average and per capita incomes corresponding to a given ZIP code.
def get_incomes_by_zip_code(zi):
	link = 'https://www.incomebyzipcode.com/california/' + str(zi)
	page = requests.get(link)
	soup = BeautifulSoup(page.content, "html.parser")
	tables = soup.find_all('table', {'class':'table my-3 mb-5'})
	try:
		med_income = tables[0]
		av_income = tables[1]
		per_capita_income = tables[2]
		
		med_income = med_income.find('tr').find('td',{'class':'text-right'}).text
		med_income = re.sub("[^0-9]", "", med_income)
		med_income = int(med_income)

		av_income = av_income.find('tr').find('td',{'class':'text-right'}).text
		av_income = re.sub("[^0-9]", "", av_income)
		av_income = int(av_income)
		
		per_capita_income = per_capita_income.find('tr').find('td',{'class':'text-right'}).text
		per_capita_income = re.sub("[^0-9]", "", per_capita_income)
		per_capita_income = int(per_capita_income)
	except:
		print("Zip:",zi)
		print("Tables:",tables)
	
	return med_income, av_income, per_capita_income

# Get the number of restaurants corresponding to a given ZIP code using a free API (It has a daily free limit of 50 calls/day)
def get_restaurants_by_zip_code(zi, xapi_key, xrapidapi_key):
	fname = "./API_Responses/response_{}.json".format(zi)
	if not os.path.exists(fname):
		url = "https://documenu.p.rapidapi.com/restaurants/zip_code/" + str(zi)
		headers = {'x-api-key': xapi_key,'x-rapidapi-key': xrapidapi_key ,'x-rapidapi-host': "documenu.p.rapidapi.com"}
		response = requests.request("GET", url, headers=headers)
		json_string = response.text
		json_ob = json.loads(json_string)
		with open(fname , 'w') as f:
			json.dump(json_ob,f)
		print("Saved JSON response for zip code {}".format(zi))
	else:
		with open(fname,"r") as f:
			json_ob = json.load(f)
	total_restaurants_for_zi = json_ob['totalResults']
	return total_restaurants_for_zi

# Combining all three sources of data into a single dataframe.
def get_dataset(zips, op = None):
	dataset = {"zips":[],"median_incomes":[],"average_incomes":[],"per_capita_incomes":[],"number_of_restaurants":[]}

	for zi in zips:
		med_income_zi, av_income_zi, per_capita_income_zi = get_incomes_by_zip_code(zi)
		total_restaurants_for_zi = get_restaurants_by_zip_code(zi,"","") ## Put your API keys here in the order (xapi_key,xrapidapi_key)
		
		curr_zips = dataset["zips"]
		curr_median = dataset["median_incomes"]
		curr_av = dataset["average_incomes"]
		curr_per_capita = dataset["per_capita_incomes"]
		curr_rest = dataset["number_of_restaurants"]

		curr_zips.append(int(zi))
		curr_median.append(int(med_income_zi))
		curr_av.append(int(av_income_zi))
		curr_per_capita.append(int(per_capita_income_zi))
		curr_rest.append(int(total_restaurants_for_zi))

		dataset["zips"] = curr_zips
		dataset["median_incomes"] = curr_median
		dataset["average_incomes"] = curr_av
		dataset["per_capita_incomes"] = curr_per_capita
		dataset["number_of_restaurants"] = curr_rest
		print("Fetched data for {}".format(zi))
	df = pd.DataFrame.from_dict(dataset)
	if op==None:
		return df
	df.to_csv(op)

if __name__ == "__main__":
	
	l = list(sys.argv)
	
	if len(l)==2 and l[1]=='--scrape': # Print the first five rows of the dataset
		zips = get_inhabited_zip_codes_in_LA()[:5]
		print("Number of zip codes is",len(zips))
		df = get_dataset(zips)
		print(df)
	
	elif len(l)==3 and l[1]=='--static': # Print all the rows of the dataset (by loading from the stored CSV file) along with some statistics
		path = l[2]
		df = pd.read_csv(path,index_col=0)
		print("\nSample data (first 5 rows):\n")
		print(df.head())
		print("\nColumn wise statistics:\n")
		print(df.describe())
	
	elif len(l)==1: # Print all the rows of the dataset (by scraping and the API) along with some statistics
		zips = get_inhabited_zip_codes_in_LA()
		print("Number of zip codes is",len(zips))
		df = get_dataset(zips)
		op = "./dataset.csv"
		df.to_csv(op)
		print("\nSample data (first 5 rows):\n")
		print(df.head())
		print("\nColumn wise statistics:\n")
		print(df.describe())
	
	else: # Print a statement for the wrong/unrecognized arguments input
		print("The arguments do not match the requirements. Please refer README.md for understanding the requirements")