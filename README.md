# Number of restaurants vs Incomes of People in an area 

## Motivation for this Project:-

It is generally considered that the more spending power of the people the more
the products that are offered. This leads to the vague conclusion that higher the
income (which in turn means more spending power of the people), more the
number of restaurants (more products in which people can spend their money
on). However if the world were to run based on such vague conclusions it would
be a different ball game altogether. Hence in this project I embark on a mission to
try and prove this hypothesis.

## 1. Installing Requirements

Install all the required python modules using the requirements.txt file using the below command: <br/>

	pip install -r requirements.txt

## 2. Setting up an API account to get the required API keys

[DocumenuAPI Login Link](https://documenuapi.us.auth0.com/login?state=hKFo2SBlM0cwSTA3NUh6bmJvMGFhNm5iZDNEc1NocWRHbnNkV6FupWxvZ2luo3RpZNkgWTVxWC1UZko4UEEzR2hKVHpNRTlXemVyUmNGSHVLYy2jY2lk2SByZnQ0VUFHaUQ4a3BwUFVHMFROdTMwcDBWczljdXZCdw&client=rft4UAGiD8kppPUG0TNu30p0Vs9cuvBw&protocol=oauth2&redirect_uri=https%3A%2F%2Fdocumenu.com%2Fdashboard&scope=openid%20profile%20email&response_type=code&response_mode=query&nonce=NG92dmtGWXNfcC1XWmtHU2dGa3hLY2lyWWE4bVRUa1dJSjloSmVjUEVZUQ%3D%3D&code_challenge=_WFvc2Hv8ZqOq6yxkW9GRsS52AENfyh_nACXot_pe60&code_challenge_method=S256&auth0Client=eyJuYW1lIjoiYXV0aDAtcmVhY3QiLCJ2ZXJzaW9uIjoiMS4yLjAifQ%3D%3D)	
By signing up in the above link you will get the free x-api-key.

[RapidAPI Login Link](https://rapidapi.com/auth/sign-up?referral=/restaurantmenus/api/documenu/) <br/>
By signing up in the above link you will get the free x-RapidAPI-Key.

Note that both x-api-key and x-RapidAPI-Key are not the same.

The API is used to get the number of restaurants corresponding to a ZIP code. However, the free API has a limit of 50 calls per day and in my project I'm using more than 50 zip codes. Hence I'm saving the API response JSON in the directory "./API_Responses". So when running the code if the JSON object exists, we directly get the required data by reading the JSON instead of calling the API again. If there is no JSON corresponding to the ZIP code, then the API is called and the JSON is saved for future use along with fetching the required data.

## 3. Running the files (and its different modes)
    
   **For get_dataset.py (For Homework 4):**

	Mode 1: python get_dataset.py --scrape
In this mode, we scrape the ZIP codes and select 5 of them. Then we get the corresponding values of median income, average income, per capita income and number of restaurants. We print these 5 samples.

	Mode 2: python get_dataset.py --static ./dataset.csv
In this mode we load our dataset from the file path mentioned (Here, './dataset.csv'). We then print the first five rows and some statistics corresponding to the dataset.

	Mode 3: python get_dataset.py
In this mode we scrape the list of ZIP codes and then get all the corresponding information and save them to the file './dataset.csv'. We also print the first five rows and some statistics corresponding to the dataset.

**For use_dataset.py (For Homework 5):**

	Mode 1: python use_dataset.py --static ./dataset.csv
In this mode we load our dataset from the file path mentioned (Here, './dataset.csv'). We then perform the analysis of the dataset and display the results.

	Mode 2: python use_dataset.py
In this mode we scrape the list of ZIP codes and then get all the corresponding information and save them to a dataframe. We then pass the dataframe to perform analysis of the dataset and display the results.